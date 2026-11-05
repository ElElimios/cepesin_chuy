# Dataset: News in 60 Seconds (Radio Cumbres Corpus)

## Description
This dataset is curated specifically for **RNAP Hack 2026 - Track 2: News in 60 Seconds**, following the standards of the **XL-Sum (Spanish subset / BBC Mundo)** benchmark. It addresses automated news summarization in Spanish for **Radio Cumbres**, a morning radio broadcast in Nuevo León.

## Operational Constraints
- **Air Time Window**: Exactly 60 seconds per news story on air.
- **Reading Speed**: Approximately 2 words per second.
- **Strict Word Limit**: **Maximum 120 words per summary** ($\le 120$ words).
- **Factual Integrity**: Zero invented facts, names, or numbers.

## Dataset Statistics
- **Total Articles**: 120 Spanish news articles across 10 balanced categories.
- **Language**: Spanish (`es`).
- **Categories**: Economía, Movilidad, Medio Ambiente, Ciencia, Educación, Salud, Deportes, Cultura, Tecnología, Energía (12 articles each).
- **Splits**:
  - `train.csv`: 84 articles (70%)
  - `val.csv`: 18 articles (15%)
  - `test.csv`: 18 articles (15%)
- **Stratification**: Strictly stratified by news category (`stratify=category`, `random_state=42`) to prevent data leakage and guarantee balanced domain representation.

## Schema
| Column | Type | Description |
|---|---|---|
| `id` | Integer | Unique identifier for each news article |
| `title` | String | Headline of the news story |
| `category` | String | Thematic category (Economía, Movilidad, etc.) |
| `article` | String | Full journalistic text of the article |
| `reference_summary` | String | Journalist-written gold-standard reference summary ($\le 120$ words) |
| `article_word_count` | Integer | Number of words in the full article |
| `summary_word_count` | Integer | Number of words in the gold-standard summary |
| `summary_read_time_seconds` | Float | Estimated read-aloud time at 2 words/second |
