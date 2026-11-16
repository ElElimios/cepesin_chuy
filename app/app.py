import os
import time
import torch
import gradio as gr
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

# Si guardas la carpeta del fine-tuning de Colab en "app/modelo_finetuned", la carga desde ahí.
# Si no existe en la laptop, carga automáticamente el modelo mT5_multilingual_XLSum en local.
CARPETA_LOCAL = os.path.join(os.path.dirname(__file__), "modelo_finetuned")
MODELO_HF = "csebuetnlp/mT5_multilingual_XLSum"

MODEL_PATH = CARPETA_LOCAL if os.path.isdir(CARPETA_LOCAL) else MODELO_HF
device = "cuda" if torch.cuda.is_available() else "cpu"

print(f"Cargando modelo en local desde: {MODEL_PATH} ({device.upper()})...")
tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_PATH).to(device)
model.eval()


def generar_resumen(noticia: str, max_palabras: int = 110):
    if not noticia or not noticia.strip():
        return "Por favor ingresa el texto de una noticia en español.", "0 palabras", "0.00 s"

    t0 = time.time()
    inputs = tokenizer(
        noticia.strip(),
        return_tensors="pt",
        max_length=512,
        truncation=True,
    ).to(device)

    with torch.no_grad():
        summary_ids = model.generate(
            inputs["input_ids"],
            attention_mask=inputs["attention_mask"],
            max_length=160,
            min_length=35,
            num_beams=4,
            length_penalty=1.1,
            no_repeat_ngram_size=3,
            early_stopping=True,
        )

    resumen = tokenizer.decode(summary_ids[0], skip_special_tokens=True).strip()

    # Regla del reto Track 2: máximo 120 palabras
    palabras = resumen.split()
    limite = min(int(max_palabras), 120)
    if len(palabras) > limite:
        resumen = " ".join(palabras[:limite]).rstrip(",;:") + "."
        palabras = resumen.split()

    duracion = time.time() - t0
    estado = "Cumple (<= 120 palabras)" if len(palabras) <= 120 else "Excede 120 palabras"
    info_palabras = f"{len(palabras)} palabras — {estado}"
    info_tiempo = f"{duracion:.2f} segundos en {device.upper()}"

    return resumen, info_palabras, info_tiempo


EJEMPLO = [
    [
        "Autoridades de movilidad del área metropolitana de Monterrey informaron que la "
        "implementación de carriles reversibles y semáforos inteligentes redujo en un 15 por "
        "ciento los tiempos de traslado matutinos durante el primer mes de prueba. El programa "
        "operará de lunes a viernes entre las 6:30 y las 9:30 de la mañana, con apoyo de "
        "unidades de tránsito en los principales cruces viales para agilizar el flujo vehicular.",
        110,
    ]
]

demo = gr.Interface(
    fn=generar_resumen,
    inputs=[
        gr.Textbox(
            lines=9,
            label="Noticia de entrada (Español)",
            placeholder="Pega aquí la noticia completa...",
        ),
        gr.Slider(
            minimum=50,
            maximum=120,
            value=110,
            step=5,
            label="Límite máximo de palabras (Reto <= 120)",
        ),
    ],
    outputs=[
        gr.Textbox(lines=6, label="Resumen generado (Guion de 60 segundos)"),
        gr.Textbox(label="Conteo de palabras (Métrica <= 120)"),
        gr.Textbox(label="Tiempo de inferencia local"),
    ],
    title="News in 60 Seconds — Interfaz v1 Local (Track 2)",
    description=f"Modelo cargado localmente: {MODEL_PATH} | Límite estricto: <= 120 palabras.",
    examples=EJEMPLO,
)

if __name__ == "__main__":
    demo.launch(server_name="127.0.0.1", server_port=7860, share=False)
