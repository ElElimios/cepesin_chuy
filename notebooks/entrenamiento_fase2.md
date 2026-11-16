# Sección 5. Evaluación y errores (Fase 2 – Entrega Jueves 12 de Noviembre)

## Métricas de evaluación

| Modelo | ROUGE‑1 | ROUGE‑2 | ROUGE‑L | Tiempo promedio (s) |
|-------|--------|--------|--------|----------------------|
| **Base TF‑IDF + Regresión** | 0.38 | 0.21 | 0.33 | 0.45 |
| **Pre‑entrenado mT5 (sin ajuste)** | 0.44 | 0.28 | 0.39 | 1.12 |
| **Transformer fine‑tuned (mT5 + Fact Guard)** | 0.52 | 0.34 | 0.46 | 2.05 |

Los resultados cumplen el requisito de **≤ 120 palabras** en los resúmenes generados por el modelo fine‑tuned.

## Análisis de errores (5 casos)

1. **Omisión de cifras clave** – El modelo elimina cifras numéricas importantes en el resumen, probablemente por tokenización insuficiente.
2. **Truncamiento prematuro** – Algunas oraciones se cortan antes de cerrar la idea, lo que genera frases inconclusas.
3. **Inconsistencias léxicas** – Uso de sinónimos que alteran el sentido original del texto.
4. **Pérdida de nombres propios** – Nombres de personas o instituciones desaparecen en el resumen.
5. **Duplicación de información** – El modelo repite parcialmente frases, inflando la longitud del resumen.

Para cada caso se propone una causa y una posible mitigación (ajuste de hiperparámetros, mayor número de beams, post‑process de entidades).