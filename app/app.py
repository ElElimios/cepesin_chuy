import os
import re
import time
import torch
import gradio as gr
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

# Carga el modelo ajustado local si existe en la carpeta; si no, descarga mT5_multilingual_XLSum
LOCAL_MODEL_DIR = os.path.join(os.path.dirname(__file__), "modelo_finetuned")
DEFAULT_MODEL = "csebuetnlp/mT5_multilingual_XLSum"

MODEL_PATH = LOCAL_MODEL_DIR if os.path.isdir(LOCAL_MODEL_DIR) else DEFAULT_MODEL
device = "cuda" if torch.cuda.is_available() else "cpu"

print(f"Cargando modelo desde {MODEL_PATH} en {device.upper()}...")
tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_PATH).to(device)
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


def resumir_noticia(articulo: str, min_palabras: int = 55, max_palabras: int = 115):
    if not articulo or not articulo.strip():
        return (
            "Por favor pega el texto de una noticia en español.",
            "0 palabras (0.0 s)",
            "Sin datos",
            "0.00 s",
        )

    t0 = time.time()
    inputs = tokenizer(
        articulo.strip(),
        return_tensors="pt",
        max_length=512,
        truncation=True,
    ).to(device)

    # Convertimos el mínimo de palabras deseado a un aproximado de sub-tokens
    min_tokens = max(35, int(min_palabras * 1.4))

    with torch.no_grad():
        output_ids = model.generate(
            inputs["input_ids"],
            attention_mask=inputs["attention_mask"],
            min_new_tokens=min_tokens,
            max_new_tokens=165,
            num_beams=4,
            length_penalty=1.2,
            no_repeat_ngram_size=3,
            early_stopping=True,
        )

    resumen = tokenizer.decode(output_ids[0], skip_special_tokens=True).strip()

    # Regla estricta de Radio Cumbres: máximo 120 palabras (60 segundos a 2 palabras/seg)
    palabras = resumen.split()
    limite = min(int(max_palabras), 120)
    if len(palabras) > limite:
        resumen = " ".join(palabras[:limite]).rstrip(",;:") + "."
        palabras = resumen.split()

    num_palabras = len(palabras)
    segundos_aire = num_palabras / 2.0
    latencia = time.time() - t0

    cumple = "CUMPLE (<= 120 pal. / <= 60s)" if num_palabras <= 120 else "EXCEDE LÍMITE"
    metrica_aire = f"{num_palabras} palabras (~{segundos_aire:.1f} s al aire) — {cumple}"
    reporte_fact = verificar_fact_guard(resumen, articulo)
    metrica_tiempo = f"{latencia:.2f} segundos ({device.upper()})"

    return resumen, metrica_aire, reporte_fact, metrica_tiempo


EJEMPLOS = [
    [
        "El gobierno municipal de General Escobedo presentó este jueves una iniciativa de gran "
        "escala enfocada en parques solares fotovoltaicos y energía limpia, con una inversión "
        "autorizada de 560 millones de pesos provenientes de participaciones públicas y privadas. "
        "La obra modernizará la infraestructura urbana y beneficiará a más de 280,000 habitantes "
        "del área metropolitana de Nuevo León. Las labores técnicas iniciarán el próximo mes con "
        "sistemas de supervisión digital y controles ecológicos para garantizar entrega puntual.",
        55,
        115,
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
    demo.launch(server_name="127.0.0.1", server_port=7860, share=False)
