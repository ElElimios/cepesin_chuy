# Dataset Documentation — Track 2: News in 60 Seconds

## Restructured Data Splits (`reestructuracion` branch)
During Phase 2, outdated sample CSVs were removed and replaced with the official Spanish news JSONL splits used across all notebooks:

* **`spanish_train_sample.jsonl`:** Training split used for the baseline and `mT5_multilingual_XLSum` fine-tuning.
* **`spanish_val.jsonl`:** Validation split used for hyperparameter tuning and checkpoint selection during training.
* **`spanish_test.jsonl`:** Held-out test split used to evaluate ROUGE-1, ROUGE-2, ROUGE-L, word count (`<= 120` words), inference time, and the 5 error cases.

> **Note:** Full multi-thousand training sets are loaded directly in Google Colab during model training to respect GitHub's 25 MB file size limit.
