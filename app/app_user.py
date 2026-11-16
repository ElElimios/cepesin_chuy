# app_user.py – Mi aporte personal (versión corregida de la interfaz Gradio)

"""Interfaz Gradio para el reto *News in 60 Seconds*.

- Carga el modelo fine‑tuned `csebuetnlp/mT5_multilingual_XLSum` si está en la carpeta
  ``app/modelo_finetuned``; de lo contrario lo descarga de Hugging‑Face.
- Implementa *Fact Guard* que verifica que las cifras del resumen aparecen en el artículo.
- Garantiza que el resumen no supere las 120 palabras (límite del reto y de Radio Cumbres).
- Muestra métricas de palabras, tiempo de inferencia y estado de la verificación.
"""

import os
import re
import time
import torch
import gradio as gr
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

# ---------------------------------------------------------------------------
# Configuración del modelo
# ---------------------------------------------------------------------------
CARPETA_LOCAL = os.path.join(os.path.dirname(__file__), "modelo_finetuned")
DEFAULT_MODEL = "csebuetnlp/mT5_multilingual_XLSum"

MODEL_PATH = CARPETA_LOCAL if os.path.isdir(CARPETA_LOCAL) else DEFAULT_MODEL
device = "cuda" if torch.cuda.is_available() else "cpu"

print(f"Cargando modelo desde: {MODEL_PATH} ({device.upper()}) ...")

tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_PATH).to(device)
model.eval()

# ---------------------------------------------------------------------------
# Utilidades
# ---------------------------------------------------------------------------
def _verificar_fact_guard(resumen: str, articulo: str) -> str:
    """Comprueba que todas las cifras del resumen aparecen en el artículo.

    Devuelve un mensaje indicando si hay cifras inventadas.
    """
    cifras_resumen = set(re.findall(r"\d+(?:[.,]\d+)?", resumen))
    cifras_articulo = set(re.findall(r"\d+(?:[.,]\d+)?", articulo))
    inventadas = cifras_resumen - cifras_articulo

    if not cifras_resumen:
        return "Verificado (sin cifras numéricas)"
    if not inventadas:
        return f"100 % fiel — cifras validadas: {', '.join(sorted(cifras_resumen))}"
    return f"Alerta Fact Guard — revisar cifras: {', '.join(sorted(inventadas))}"

# ---------------------------------------------------------------------------
# Funciones de generación
# ---------------------------------------------------------------------------
def generar_resumen(articulo: str, max_palabras: int = 110) -> tuple:
    """Genera un resumen a partir del artículo completo.

    Devuelve ``(resumen, info_palabras, info_tiempo)``.
    """
    if not articulo or not articulo.strip():
        return (
            "Por favor ingresa el texto de una noticia en español.",
            "0 palabras",
            "0.00 s",
        )

    t0 = time.time()
    inputs = tokenizer(
        articulo,
        return_tensors="pt",
        max_length=512,
        truncation=True,
    ).to(device)

    # Convertimos el límite de palabras a un número aproximado de tokens.
    # Cada palabra ~1.4 tokens en promedio para mT5.
    max_tokens = int(max_palabras * 1.4)

    with torch.no_grad():
        summary_ids = model.generate(
            inputs["input_ids"],
            attention_mask=inputs["attention_mask"],
            max_length=max_tokens,
            min_length=35,
            num_beams=4,
            length_penalty=1.2,
            no_repeat_ngram_size=3,
            early_stopping=True,
        )

    resumen = tokenizer.decode(summary_ids[0], skip_special_tokens=True).strip()

    # Enforzamos el límite estricto de 120 palabras.
    palabras = resumen.split()
    limite = min(max_palabras, 120)
    if len(palabras) > limite:
        resumen = " ".join(palabras[:limite]).rstrip(",;:") + "."
        palabras = resumen.split()

    duracion = time.time() - t0
    info_palabras = f"{len(palabras)} palabras — {'cumple' if len(palabras) <= 120 else 'excede'} límite 120"
    info_tiempo = f"{duracion:.2f} s en {device.upper()}"
    return resumen, info_palabras, info_tiempo

def resumir_noticia(articulo: str, min_palabras: int = 55, max_palabras: int = 115) -> tuple:
    """Genera el resumen y devuelve métricas adicionales.

    Retorna ``(resumen, metricas_aire, reporte_fact, metricas_tiempo)``.
    """
    if not articulo or not articulo.strip():
        return (
            "Por favor pega el texto de una noticia en español.",
            "0 palabras (0.0 s)",
            "Sin datos", "0.00 s",
        )

    # Generar resumen usando la función anterior.
    resumen, info_palabras, info_tiempo = generar_resumen(articulo, max_palabras)

    # Métricas de tiempo en aire (2 palabras / segundo).
    num_palabras = len(resumen.split())
    segundos_aire = num_palabras / 2.0
    cumple = "CUMPLE" if num_palabras <= 120 else "EXCEDE"
    metricas_aire = f"{num_palabras} palabras (~{segundos_aire:.1f}s al aire) — {cumple} límite"

    # Fact Guard.
    reporte_fact = _verificar_fact_guard(resumen, articulo)

    # Tiempo total de inferencia (ya calculado en generar_resumen).
    metricas_tiempo = info_tiempo

    return resumen, metricas_aire, reporte_fact, metricas_tiempo

# ---------------------------------------------------------------------------
# Interfaz Gradio
# ---------------------------------------------------------------------------
EJEMPLOS = [
    [
        "Autoridades de movilidad del área metropolitana de Monterrey informaron que la implementación de carriles reversibles y semáforos inteligentes redujo en un 15 por ciento los tiempos de traslado matutinos durante el primer mes de prueba. El programa operará de lunes a viernes entre las 6:30 y las 9:30 de la mañana, con apoyo de unidades de tránsito en los principales cruces viales para agilizar el flujo vehicular.",
        110,
        "El gobierno municipal de General Escobedo presentó este jueves una iniciativa de gran escala enfocada en parques solares fotovoltaicos y energía limpia, con una inversión autorizada de 560 millones de pesos provenientes de participaciones públicas y privadas. La obra modernizará la infraestructura urbana y beneficiará a más de 280,000 habitantes del área metropolitana de Nuevo León. Las labores técnicas iniciarán el próximo mes con sistemas de supervisión digital y controles ecológicos para garantizar entrega puntual.",
        55,
        115,
    ]
]

iface = gr.Interface(
    fn=resumir_noticia,
    inputs=[
        gr.Textbox(lines=9, label="Artículo Periodístico Original (Español)"),
        gr.Slider(minimum=40, maximum=90, value=55, step=5, label="Longitud mínima objetivo (palabras)"),
        gr.Slider(minimum=60, maximum=120, value=115, step=5, label="Límite máximo de palabras (<= 120)")
    ],
    outputs=[
        gr.Textbox(lines=6, label="Resumen generado (Guion de 60 segundos)"),
        gr.Textbox(label="Metricas de tiempo al aire"),
        gr.Textbox(label="Verificación Fact Guard"),
        gr.Textbox(label="Tiempo de inferencia"),
    ],
    title="Radio Cumbres — News in 60 Seconds (Interfaz v1 – Mi aporte)",
    description=f"Modelo cargado: {MODEL_PATH} | Límite estricto: <= 120 palabras.",
    examples=EJEMPLOS,
)

if __name__ == "__main__":
    iface.launch()
