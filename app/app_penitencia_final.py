import os
import re
import sys
import time
import torch
import gradio as gr
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from peft import PeftModel  # <-- 1. Importar PeftModel

# Detecta automáticamente si corre como archivo .py o dentro de una celda de Colab
BASE_DIR = os.path.dirname(os.path.abspath(__file__)) if "__file__" in globals() else os.getcwd()
# 2. Apunta directo al nombre real de tu carpeta (o renómbrala a modelo_finetuned)
ADAPTER_DIR = os.path.join(BASE_DIR, "mt5_radio_cumbres_lora") 
DEFAULT_MODEL = "csebuetnlp/mT5_multilingual_XLSum"

device = "cuda" if torch.cuda.is_available() else "cpu"

# 3. Carga el tokenizador (puedes usar el de tu carpeta o el base)
tokenizer = AutoTokenizer.from_pretrained(
    ADAPTER_DIR if os.path.isdir(ADAPTER_DIR) else DEFAULT_MODEL
)

# 4. Siempre carga primero el modelo base
print(f"Cargando modelo base {DEFAULT_MODEL} en {device.upper()}...")
base_model = AutoModelForSeq2SeqLM.from_pretrained(DEFAULT_MODEL)

# 5. Si existe tu carpeta LoRA, acopla los adaptadores al modelo base
if os.path.isdir(ADAPTER_DIR):
    print(f"Aplicando y fusionando adaptadores LoRA desde {ADAPTER_DIR}...")
    model = PeftModel.from_pretrained(base_model, ADAPTER_DIR)
    model = model.merge_and_unload()  # <-- Agrega esta línea
    MODEL_PATH = f"{DEFAULT_MODEL} + LoRA (mt5_radio_cumbres_lora)"
else:
    print("No se encontraron adaptadores LoRA, usando modelo base.")
    model = base_model
    MODEL_PATH = DEFAULT_MODEL

model = model.to(device)
model.eval()

def verificar_fact_guard(resumen: str, articulo: str) -> str:
    """Verifica que las cifras del resumen existan en el artículo original."""
    cifras_resumen = set(re.findall(r"\d+(?:[.,]\d+)?", resumen))
    cifras_articulo = set(re.findall(r"\d+(?:[.,]\d+)?", articulo))
    inventadas = cifras_resumen - cifras_articulo

    if not cifras_resumen:
        return "Verificado (Sin cifras numéricas que contrastar)"
    if not inventadas:
        return f"100% Fiel — Cifras validadas: {', '.join(sorted(cifras_resumen))}"
    return f"Alerta Fact Guard — Revisar cifras: {', '.join(sorted(inventadas))}"


def _generar_bloque(texto: str, min_tok: int, max_tok: int) -> str:
    """Genera un bloque de resumen limpio sin preguntas retóricas."""
    inputs = tokenizer(
        texto.strip(),
        return_tensors="pt",
        max_length=512,
        truncation=True,
    ).to(device)

    # Prohibimos el signo de interrogación '¿' para evitar preguntas de relleno estilo BBC
    bad_words_ids = tokenizer(["¿", "?"], add_special_tokens=False).input_ids

    with torch.no_grad():
        output_ids = model.generate(
            input_ids=inputs["input_ids"],
            attention_mask=inputs["attention_mask"],
            min_new_tokens=min_tok,
            max_new_tokens=max_tok,
            num_beams=2,
            length_penalty=1.4,
            no_repeat_ngram_size=3,
            bad_words_ids=bad_words_ids,
            early_stopping=True,
        )
    return tokenizer.decode(output_ids[0], skip_special_tokens=True).strip()


def _seleccionar_oraciones_clave(texto_restante: str, min_faltantes: int, max_faltantes: int) -> str:
    """Selecciona oraciones con mayor densidad de datos hasta caer exactamente
    dentro del rango [min_faltantes, max_faltantes] sin pasarse del límite."""
    oraciones = [o.strip() for o in re.split(r'(?<=[.!?])\s+', texto_restante) if len(o.split()) >= 6]
    if not oraciones:
        return ""

    def puntaje(oracion: str) -> int:
        puntos = 0
        if re.search(r'\d+', oracion):
            puntos += 5
        if any(p in oracion.lower() for p in ["según", "datos", "permite", "reducir", "transforma", "por ciento", "%", "informó", "señaló"]):
            puntos += 3
        return puntos

    # Ordenamos índices por relevancia para priorizar datos duros, pero manteniendo orden lógico
    indices_ordenados = sorted(range(len(oraciones)), key=lambda i: puntaje(oraciones[i]), reverse=True)
    
    indices_elegidos = []
    acumulado = 0

    for idx in indices_ordenados:
        largo = len(oraciones[idx].split())
        # Solo agregamos la oración si no nos hace pasar del máximo permitido
        if acumulado + largo <= max_faltantes:
            indices_elegidos.append(idx)
            acumulado += largo
        # Cuando ya superamos el mínimo requerido (100+ palabras totales), nos detenemos
        if acumulado >= min_faltantes:
            break

    # Reordenamos las elegidas según su aparición original en la noticia para que tengan coherencia
    indices_elegidos.sort()
    return " ".join(oraciones[i] for i in indices_elegidos)


def resumir_noticia(articulo: str, min_palabras: int = 100, max_palabras: int = 120):
    if not articulo or not articulo.strip():
        return (
            "Por favor pega el texto de una noticia en español.",
            "0 palabras (0.0 s)",
            "Sin datos",
            "0.00 s",
        )

    t0 = time.time()
    texto_limpio = articulo.strip()

# 1. Lead abstractivo con los primeros 2 párrafos
    parrafos = [p.strip() for p in texto_limpio.split("\n") if p.strip()]
    texto_lead = " ".join(parrafos[:2]) if len(parrafos) >= 2 else texto_limpio

    inputs = tokenizer(
        texto_lead,
        return_tensors="pt",
        max_length=300,
        truncation=True,
    ).to(device)

    bad_words_ids = tokenizer(["¿", "?"], add_special_tokens=False).input_ids

    with torch.no_grad():
        output_ids = model.generate(
            input_ids=inputs["input_ids"],
            attention_mask=inputs["attention_mask"],
            min_new_tokens=42,   # <-- Subimos de 35 a 42
            max_new_tokens=60,   # <-- Subimos de 55 a 60
            num_beams=2,
            length_penalty=1.0,
            no_repeat_ngram_size=3,
            bad_words_ids=bad_words_ids,
            early_stopping=True,
        )

    lead_abstractivo = tokenizer.decode(output_ids[0], skip_special_tokens=True).strip()
    if not lead_abstractivo.endswith("."):
        lead_abstractivo += "."

# 2. Completamos exactamente hasta el rango [objetivo_min, limite_max] (100 - 120 palabras)
    palabras_lead = len(lead_abstractivo.split())
    objetivo_min = max(100, int(min_palabras))
    limite_max = min(120, int(max_palabras))

    # Si hay al menos 3 párrafos, usamos del 3 en adelante; si el texto tiene pocos párrafos,
    # usamos desde la segunda oración del artículo para asegurar suficiente material.
    if len(parrafos) >= 3:
        cuerpo_restante = " ".join(parrafos[2:])
    else:
        oraciones_orig = re.split(r'(?<=[.!?])\s+', texto_limpio)
        cuerpo_restante = " ".join(oraciones_orig[1:])

    min_faltantes = max(0, objetivo_min - palabras_lead)
    max_faltantes = max(0, limite_max - palabras_lead)

    complemento = (
        _seleccionar_oraciones_clave(cuerpo_restante, min_faltantes, max_faltantes)
        if min_faltantes > 0 else ""
    )

    resumen = f"{lead_abstractivo} {complemento}".strip()

    # 3. Ajuste estricto al límite máximo (<= 120 palabras) respetando puntos finales
    palabras = resumen.split()
    if len(palabras) > limite_max:
        recorte = " ".join(palabras[:limite_max])
        if "." in recorte:
            resumen = recorte.rsplit(".", 1)[0] + "."
        else:
            resumen = recorte.rstrip(",;:") + "."
        palabras = resumen.split()

    num_palabras = len(palabras)
    segundos_aire = num_palabras / 2.0
    latencia = time.time() - t0

    if 100 <= num_palabras <= 120:
        estado = "ÓPTIMO (50s - 60s al aire)"
    elif num_palabras < 100:
        estado = "CORTO (< 50s al aire — pega una noticia más extensa)"
    else:
        estado = "EXCEDE LÍMITE (> 60s)"

    metrica_aire = f"{num_palabras} palabras (~{segundos_aire:.1f} s al aire) — {estado}"
    reporte_fact = verificar_fact_guard(resumen, articulo)
    metrica_tiempo = f"{latencia:.2f} segundos ({device.upper()})"

    return resumen, metrica_aire, reporte_fact, metrica_tiempo

EJEMPLOS = [
    [
        "Un consorcio internacional de ingenieros marinos y biólogos ambientales anunció esta semana un hito significativo en la lucha contra la contaminación marina. Su nueva barrera flotante autónoma, impulsada exclusivamente por energía solar y corrientes oceánicas, logró extraer más de mil toneladas de desechos plásticos de la Gran Mancha de Basura del Pacífico en apenas seis meses de operación continua. A diferencia de los modelos anteriores, que requerían el remolque constante de embarcaciones pesadas y consumían grandes cantidades de combustible fósil, esta innovadora estructura utiliza algoritmos de inteligencia artificial y sensores satelitales para navegar de forma independiente hacia las zonas con mayor concentración de residuos. Además, incorpora sistemas acústicos y visuales diseñados específicamente para ahuyentar a la fauna marina, garantizando que peces, tortugas y mamíferos no queden atrapados en las redes de recolección. Según los datos presentados por el equipo de investigación, cerca del 80 % del material recuperado consiste en microplásticos degradados y redes de pesca abandonadas, conocidas como 'redes fantasma', que representan una de las mayores amenazas para la biodiversidad submarina. Una vez extraídos del agua, los residuos son compactados en plataformas flotantes y trasladados a tierra firme, donde una planta especializada los transforma en materia prima para la industria de la construcción y el mobiliario urbano. Los responsables del proyecto señalaron que el éxito de esta fase piloto permitirá desplegar una flota de diez unidades similares antes de que finalice el próximo año. De mantenerse este ritmo de eficiencia, los científicos estiman que sería posible reducir en un 40 % la superficie actual de residuos flotantes en el Pacífico norte durante la próxima década, marcando un precedente optimista para la recuperación de los ecosistemas marinos a nivel global.",
        90,
        120,
    ],
    [
        "Un equipo internacional de geofísicos, liderado por la doctora Elena Rostova de la Universidad de Zúrich y el ingeniero Carlos Mendoza del Laboratorio de Propulsión a Chorro (JPL), anunció este lunes el descubrimiento de un extenso acuífero subterráneo bajo la región marciana de Elysium Planitia. El hallazgo se logró tras analizar más de 1.400 registros sísmicos recopilados por la sonda InSight entre 2018 y 2022. Según el estudio publicado en la revista Nature Geoscience, el depósito se encuentra a una profundidad de entre 11,5 y 20 kilómetros bajo la corteza rocosa. Los cálculos preliminares indican que el volumen de agua atrapada en las fracturas minerales sería suficiente para cubrir toda la superficie del planeta rojo con un océano global de aproximadamente 1,5 kilómetros de profundidad, superando en un 30 % las estimaciones previas realizadas por la Agencia Espacial Europea (ESA). 'Este descubrimiento resuelve el misterio sobre el destino de los antiguos océanos que cubrieron Marte hace más de 3.000 millones de años', explicó la doctora Rostova durante la conferencia de prensa en Pasadena, California. Por su parte, el director de ciencias planetarias de la NASA, Marcus Vance, señaló que, aunque la profundidad actual impide su extracción inmediata para futuras misiones tripuladas, el hallazgo transforma por completo la búsqueda de vida microbiana extraterrestre. Los investigadores utilizaron modelos matemáticos avanzados y supercomputadoras capaces de procesar 45 terabytes de datos acústicos para descartar que las señales correspondieran a depósitos de magma o dióxido de carbono congelado. El consorcio científico ya prepara una nueva propuesta de misión orbital, presupuestada en 850 millones de dólares, para mapear con mayor precisión la extensión total de estas reservas hídricas antes de 2034.",
        90,
        120,
    ],
    [
        "El rápido despliegue de la inteligencia artificial y los servicios en la nube ha disparado la demanda energética de las infraestructuras digitales en Estados Unidos. Según un estudio publicado este lunes en la revista científica Nature, los grandes centros de datos del país norteamericano ya consumen una cantidad de electricidad equivalente al gasto energético anual de todo Chile.   La investigación revela que estas instalaciones acaparan actualmente el 1,8 % del consumo eléctrico total de Estados Unidos. Asimismo, los autores del informe advierten que las emisiones de carbono asociadas a la operación de estos servidores se han triplicado desde 2018, impulsadas por la necesidad de entrenar y mantener activos modelos computacionales cada vez más complejos.   El impacto económico y tecnológico de esta industria también fue analizado esta semana por el Banco Interamericano de Desarrollo (BID). En su más reciente reporte presentado en Washington, el organismo internacional estima que América Latina podría aumentar su crecimiento económico en un 5,1 % durante la próxima década si logra adoptar de manera efectiva las herramientas de inteligencia artificial, lo que además impulsaría una mejora del 4,2 % en los niveles de empleo regional.   Por su parte, en Europa avanzan las medidas para supervisar este ecosistema. El presidente de la Comisión Nacional de los Mercados y la Competencia (CNMC) en España anunció planes para reforzar su sede en Barcelona, donde actualmente operan cerca de cien trabajadores, con el objetivo de convertirla en un centro clave para la regulación de la inteligencia artificial y las grandes plataformas digitales.",
        90,
        120,
    ],
    [
        "La Comisión Europea anunció este martes en Bruselas la aprobación de un ambicioso paquete financiero destinado a acelerar la producción industrial de baterías de estado sólido para vehículos eléctricos. La iniciativa, respaldada por la comisaria de Energía, Kadri Simson, y el ministro de Economía alemán, Robert Habeck, busca reducir en un 65 % la dependencia tecnológica de los fabricantes europeos respecto a los proveedores asiáticos antes de 2032. El programa contará con una inversión pública inicial de 4.200 millones de euros, a la que se sumarán otros 6.800 millones aportados por un consorcio de 28 empresas automotrices y centros tecnológicos liderados por grupos como Volkswagen, Stellantis y la firma francesa Saft. Según las estimaciones técnicas presentadas durante la cumbre, esta nueva generación de baterías permitirá aumentar la autonomía de los automóviles en un 45 %, alcanzando hasta 950 kilómetros con una sola carga de apenas doce minutos. 'Estamos ante el salto tecnológico más relevante para la descarbonización del transporte en las últimas dos décadas', afirmó la doctora Clara Lindqvist, directora del Instituto Europeo de Innovación Energética en Estocolmo. El proyecto contempla la construcción de cuatro megafábricas piloto ubicadas en España, Alemania, Polonia y Suecia, las cuales generarán aproximadamente 14.500 empleos directos altamente cualificados. Los primeros prototipos comerciales comenzarán sus pruebas en carretera a mediados de 2028, con el objetivo de reducir el costo de fabricación por kilovatio-hora por debajo de los 75 dólares, igualando así el precio de los vehículos tradicionales de combustión interna.",
        90,
        120,
    ],
    [
        "Un equipo multidisciplinario de biólogos marinos, liderado por la doctora Sofía Valdivia del Instituto de Ciencias del Mar y Limnología (ICML) y el investigador canadiense Thomas Miller, anunció este jueves en Puerto Morelos, Quintana Roo, el éxito de un proyecto pionero para restaurar el Sistema Arrecifal Mesoamericano. Tras cuatro años de investigación intensiva, los especialistas lograron sembrar y estabilizar más de 18.500 colonias de coral diseñadas mediante selección asistida para soportar temperaturas oceánicas de hasta 32,5 grados centígrados. El proyecto, financiado con un fondo mixto de 14,8 millones de dólares aportados por el Banco Mundial y la Fundación Arrecifes Vivos, surge como respuesta directa a las olas de calor marino que en 2023 y 2024 provocaron el blanqueamiento de casi el 60 % de los corales en la región. Mediante técnicas de microfragmentación acelerada y reproducción sexual controlada en 12 laboratorios flotantes, el equipo redujo de cinco años a apenas catorce meses el tiempo necesario para que las crías alcancen un tamaño apto para su trasplante al lecho marino. 'No estamos simplemente reforestando el océano con las mismas especies vulnerables del pasado; estamos acelerando procesos evolutivos naturales para garantizar que estos ecosistemas sobrevivan a las condiciones climáticas proyectadas para 2050', explicó la doctora Valdivia durante la presentación oficial de los resultados. Por su parte, el ministro de Medio Ambiente, Ricardo Elizondo, destacó que las nuevas barreras coralinas ya muestran una tasa de supervivencia del 88 %, superando por amplio margen el 35 % registrado en iniciativas anteriores. Además de proteger la biodiversidad de más de 500 especies de peces y crustáceos, la recuperación de estos arrecifes resulta vital para la economía local. Según datos de la Cámara Nacional de Turismo, la barrera coralina amortigua hasta el 97 % de la energía de las olas durante huracanes de categoría 4 y sostiene actividades económicas valoradas en 2.300 millones de dólares anuales. Con el respaldo de 450 voluntarios y pescadores locales capacitados, el consorcio científico planea expandir el programa hacia Belice y Honduras antes de finalizar 2028, con la meta de restaurar 120 hectáreas adicionales de ecosistema submarino.",
        90,
        120
    ]
]

demo = gr.Interface(
    fn=resumir_noticia,
    inputs=[
        gr.Textbox(
            lines=9,
            label="Artículo Periodístico Original (Español)",
            placeholder="Pega aquí el cuerpo completo de la noticia...",
        ),
        gr.Slider(
            minimum=40,
            maximum=90,
            value=55,
            step=5,
            label="Longitud mínima objetivo (palabras)",
        ),
        gr.Slider(
            minimum=60,
            maximum=120,
            value=115,
            step=5,
            label="Límite máximo estricto Radio Cumbres (<= 120 palabras)",
        ),
    ],
    outputs=[
        gr.Textbox(lines=6, label="Guion Generado para Locución (60 Segundos)"),
        gr.Textbox(label="Control de Tiempo al Aire (2 palabras/segundo)"),
        gr.Textbox(label="Verificación Fact Guard (Fidelidad de Cifras)"),
        gr.Textbox(label="Tiempo de Inferencia"),
    ],
    title="Radio Cumbres — News in 60 Seconds (Interfaz v1)",
    description=(
        f"Resumidor abstractivo con {MODEL_PATH} y verificación Fact Guard. "
        "Restricción operativa: máximo 120 palabras (60 segundos al aire)."
    ),
    examples=EJEMPLOS,
)

if __name__ == "__main__":
    en_colab = "google.colab" in sys.modules
    demo.launch(share=en_colab)
