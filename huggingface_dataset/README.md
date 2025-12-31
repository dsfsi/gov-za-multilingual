---
language:
- af
- en
- nr
- nso
- st
- ss
- tn
- ts
- ve
- xh
- zu
license: cc-by-4.0
task_categories:
- translation
- sentence-similarity
tags:
- multilingual
- parallel-corpus
- sentence-alignment
- south-african-languages
- low-resource
pretty_name: Gov-ZA Cabinet Statements (Sentence-Aligned)
size_categories:
- 100K<n<1M
configs:
- config_name: afr-eng
  data_files:
  - split: train
    path: afr-eng/train/*.parquet
  - split: test
    path: afr-eng/test/*.parquet
  - split: validation
    path: afr-eng/eval/*.parquet
- config_name: afr-nbl
  data_files:
  - split: train
    path: afr-nbl/train/*.parquet
  - split: test
    path: afr-nbl/test/*.parquet
  - split: validation
    path: afr-nbl/eval/*.parquet
- config_name: afr-nso
  data_files:
  - split: train
    path: afr-nso/train/*.parquet
  - split: test
    path: afr-nso/test/*.parquet
  - split: validation
    path: afr-nso/eval/*.parquet
- config_name: afr-sot
  data_files:
  - split: train
    path: afr-sot/train/*.parquet
  - split: test
    path: afr-sot/test/*.parquet
  - split: validation
    path: afr-sot/eval/*.parquet
- config_name: afr-ssw
  data_files:
  - split: train
    path: afr-ssw/train/*.parquet
  - split: test
    path: afr-ssw/test/*.parquet
  - split: validation
    path: afr-ssw/eval/*.parquet
- config_name: afr-tsn
  data_files:
  - split: train
    path: afr-tsn/train/*.parquet
  - split: test
    path: afr-tsn/test/*.parquet
  - split: validation
    path: afr-tsn/eval/*.parquet
- config_name: afr-tso
  data_files:
  - split: train
    path: afr-tso/train/*.parquet
  - split: test
    path: afr-tso/test/*.parquet
  - split: validation
    path: afr-tso/eval/*.parquet
- config_name: afr-ven
  data_files:
  - split: train
    path: afr-ven/train/*.parquet
  - split: test
    path: afr-ven/test/*.parquet
  - split: validation
    path: afr-ven/eval/*.parquet
- config_name: afr-xho
  data_files:
  - split: train
    path: afr-xho/train/*.parquet
  - split: test
    path: afr-xho/test/*.parquet
  - split: validation
    path: afr-xho/eval/*.parquet
- config_name: afr-zul
  data_files:
  - split: train
    path: afr-zul/train/*.parquet
  - split: test
    path: afr-zul/test/*.parquet
  - split: validation
    path: afr-zul/eval/*.parquet
- config_name: eng-nbl
  data_files:
  - split: train
    path: eng-nbl/train/*.parquet
  - split: test
    path: eng-nbl/test/*.parquet
  - split: validation
    path: eng-nbl/eval/*.parquet
- config_name: eng-nso
  data_files:
  - split: train
    path: eng-nso/train/*.parquet
  - split: test
    path: eng-nso/test/*.parquet
  - split: validation
    path: eng-nso/eval/*.parquet
- config_name: eng-sot
  data_files:
  - split: train
    path: eng-sot/train/*.parquet
  - split: test
    path: eng-sot/test/*.parquet
  - split: validation
    path: eng-sot/eval/*.parquet
- config_name: eng-ssw
  data_files:
  - split: train
    path: eng-ssw/train/*.parquet
  - split: test
    path: eng-ssw/test/*.parquet
  - split: validation
    path: eng-ssw/eval/*.parquet
- config_name: eng-tsn
  data_files:
  - split: train
    path: eng-tsn/train/*.parquet
  - split: test
    path: eng-tsn/test/*.parquet
  - split: validation
    path: eng-tsn/eval/*.parquet
- config_name: eng-tso
  data_files:
  - split: train
    path: eng-tso/train/*.parquet
  - split: test
    path: eng-tso/test/*.parquet
  - split: validation
    path: eng-tso/eval/*.parquet
- config_name: eng-ven
  data_files:
  - split: train
    path: eng-ven/train/*.parquet
  - split: test
    path: eng-ven/test/*.parquet
  - split: validation
    path: eng-ven/eval/*.parquet
- config_name: eng-xho
  data_files:
  - split: train
    path: eng-xho/train/*.parquet
  - split: test
    path: eng-xho/test/*.parquet
  - split: validation
    path: eng-xho/eval/*.parquet
- config_name: eng-zul
  data_files:
  - split: train
    path: eng-zul/train/*.parquet
  - split: test
    path: eng-zul/test/*.parquet
  - split: validation
    path: eng-zul/eval/*.parquet
- config_name: nbl-nso
  data_files:
  - split: train
    path: nbl-nso/train/*.parquet
  - split: test
    path: nbl-nso/test/*.parquet
  - split: validation
    path: nbl-nso/eval/*.parquet
- config_name: nbl-sot
  data_files:
  - split: train
    path: nbl-sot/train/*.parquet
  - split: test
    path: nbl-sot/test/*.parquet
  - split: validation
    path: nbl-sot/eval/*.parquet
- config_name: nbl-ssw
  data_files:
  - split: train
    path: nbl-ssw/train/*.parquet
  - split: test
    path: nbl-ssw/test/*.parquet
  - split: validation
    path: nbl-ssw/eval/*.parquet
- config_name: nbl-tsn
  data_files:
  - split: train
    path: nbl-tsn/train/*.parquet
  - split: test
    path: nbl-tsn/test/*.parquet
  - split: validation
    path: nbl-tsn/eval/*.parquet
- config_name: nbl-tso
  data_files:
  - split: train
    path: nbl-tso/train/*.parquet
  - split: test
    path: nbl-tso/test/*.parquet
  - split: validation
    path: nbl-tso/eval/*.parquet
- config_name: nbl-ven
  data_files:
  - split: train
    path: nbl-ven/train/*.parquet
  - split: test
    path: nbl-ven/test/*.parquet
  - split: validation
    path: nbl-ven/eval/*.parquet
- config_name: nbl-xho
  data_files:
  - split: train
    path: nbl-xho/train/*.parquet
  - split: test
    path: nbl-xho/test/*.parquet
  - split: validation
    path: nbl-xho/eval/*.parquet
- config_name: nbl-zul
  data_files:
  - split: train
    path: nbl-zul/train/*.parquet
  - split: test
    path: nbl-zul/test/*.parquet
  - split: validation
    path: nbl-zul/eval/*.parquet
- config_name: nso-sot
  data_files:
  - split: train
    path: nso-sot/train/*.parquet
  - split: test
    path: nso-sot/test/*.parquet
  - split: validation
    path: nso-sot/eval/*.parquet
- config_name: nso-ssw
  data_files:
  - split: train
    path: nso-ssw/train/*.parquet
  - split: test
    path: nso-ssw/test/*.parquet
  - split: validation
    path: nso-ssw/eval/*.parquet
- config_name: nso-tsn
  data_files:
  - split: train
    path: nso-tsn/train/*.parquet
  - split: test
    path: nso-tsn/test/*.parquet
  - split: validation
    path: nso-tsn/eval/*.parquet
- config_name: nso-tso
  data_files:
  - split: train
    path: nso-tso/train/*.parquet
  - split: test
    path: nso-tso/test/*.parquet
  - split: validation
    path: nso-tso/eval/*.parquet
- config_name: nso-ven
  data_files:
  - split: train
    path: nso-ven/train/*.parquet
  - split: test
    path: nso-ven/test/*.parquet
  - split: validation
    path: nso-ven/eval/*.parquet
- config_name: nso-xho
  data_files:
  - split: train
    path: nso-xho/train/*.parquet
  - split: test
    path: nso-xho/test/*.parquet
  - split: validation
    path: nso-xho/eval/*.parquet
- config_name: nso-zul
  data_files:
  - split: train
    path: nso-zul/train/*.parquet
  - split: test
    path: nso-zul/test/*.parquet
  - split: validation
    path: nso-zul/eval/*.parquet
- config_name: sot-ssw
  data_files:
  - split: train
    path: sot-ssw/train/*.parquet
  - split: test
    path: sot-ssw/test/*.parquet
  - split: validation
    path: sot-ssw/eval/*.parquet
- config_name: sot-tsn
  data_files:
  - split: train
    path: sot-tsn/train/*.parquet
  - split: test
    path: sot-tsn/test/*.parquet
  - split: validation
    path: sot-tsn/eval/*.parquet
- config_name: sot-tso
  data_files:
  - split: train
    path: sot-tso/train/*.parquet
  - split: test
    path: sot-tso/test/*.parquet
  - split: validation
    path: sot-tso/eval/*.parquet
- config_name: sot-ven
  data_files:
  - split: train
    path: sot-ven/train/*.parquet
  - split: test
    path: sot-ven/test/*.parquet
  - split: validation
    path: sot-ven/eval/*.parquet
- config_name: sot-xho
  data_files:
  - split: train
    path: sot-xho/train/*.parquet
  - split: test
    path: sot-xho/test/*.parquet
  - split: validation
    path: sot-xho/eval/*.parquet
- config_name: sot-zul
  data_files:
  - split: train
    path: sot-zul/train/*.parquet
  - split: test
    path: sot-zul/test/*.parquet
  - split: validation
    path: sot-zul/eval/*.parquet
- config_name: ssw-tsn
  data_files:
  - split: train
    path: ssw-tsn/train/*.parquet
  - split: test
    path: ssw-tsn/test/*.parquet
  - split: validation
    path: ssw-tsn/eval/*.parquet
- config_name: ssw-tso
  data_files:
  - split: train
    path: ssw-tso/train/*.parquet
  - split: test
    path: ssw-tso/test/*.parquet
  - split: validation
    path: ssw-tso/eval/*.parquet
- config_name: ssw-ven
  data_files:
  - split: train
    path: ssw-ven/train/*.parquet
  - split: test
    path: ssw-ven/test/*.parquet
  - split: validation
    path: ssw-ven/eval/*.parquet
- config_name: ssw-xho
  data_files:
  - split: train
    path: ssw-xho/train/*.parquet
  - split: test
    path: ssw-xho/test/*.parquet
  - split: validation
    path: ssw-xho/eval/*.parquet
- config_name: ssw-zul
  data_files:
  - split: train
    path: ssw-zul/train/*.parquet
  - split: test
    path: ssw-zul/test/*.parquet
  - split: validation
    path: ssw-zul/eval/*.parquet
- config_name: tsn-tso
  data_files:
  - split: train
    path: tsn-tso/train/*.parquet
  - split: test
    path: tsn-tso/test/*.parquet
  - split: validation
    path: tsn-tso/eval/*.parquet
- config_name: tsn-ven
  data_files:
  - split: train
    path: tsn-ven/train/*.parquet
  - split: test
    path: tsn-ven/test/*.parquet
  - split: validation
    path: tsn-ven/eval/*.parquet
- config_name: tsn-xho
  data_files:
  - split: train
    path: tsn-xho/train/*.parquet
  - split: test
    path: tsn-xho/test/*.parquet
  - split: validation
    path: tsn-xho/eval/*.parquet
- config_name: tsn-zul
  data_files:
  - split: train
    path: tsn-zul/train/*.parquet
  - split: test
    path: tsn-zul/test/*.parquet
  - split: validation
    path: tsn-zul/eval/*.parquet
- config_name: tso-ven
  data_files:
  - split: train
    path: tso-ven/train/*.parquet
  - split: test
    path: tso-ven/test/*.parquet
  - split: validation
    path: tso-ven/eval/*.parquet
- config_name: tso-xho
  data_files:
  - split: train
    path: tso-xho/train/*.parquet
  - split: test
    path: tso-xho/test/*.parquet
  - split: validation
    path: tso-xho/eval/*.parquet
- config_name: tso-zul
  data_files:
  - split: train
    path: tso-zul/train/*.parquet
  - split: test
    path: tso-zul/test/*.parquet
  - split: validation
    path: tso-zul/eval/*.parquet
- config_name: ven-xho
  data_files:
  - split: train
    path: ven-xho/train/*.parquet
  - split: test
    path: ven-xho/test/*.parquet
  - split: validation
    path: ven-xho/eval/*.parquet
- config_name: ven-zul
  data_files:
  - split: train
    path: ven-zul/train/*.parquet
  - split: test
    path: ven-zul/test/*.parquet
  - split: validation
    path: ven-zul/eval/*.parquet
- config_name: xho-zul
  data_files:
  - split: train
    path: xho-zul/train/*.parquet
  - split: test
    path: xho-zul/test/*.parquet
  - split: validation
    path: xho-zul/eval/*.parquet
---

# Gov-ZA Multilingual Cabinet Statements (Sentence-Aligned)

## Dataset Description

This dataset contains sentence-aligned parallel text from South African government cabinet statements in 11 official languages. The data is sourced from the [Government Communication and Information System (GCIS)](https://www.gcis.gov.za/) and scraped from [www.gov.za/cabinet-statements](https://www.gov.za/cabinet-statements).

**Key Features:**
- 📊 **55 language pair combinations** covering 11 South African languages
- 🔗 **Sentence-level alignment** using LASER embeddings
- 📈 **Alignment confidence scores** (cosine similarity)
- 🎯 **Train/Test/Eval splits** for each language pair
- 🌍 **Low-resource African languages** represented

### Supported Languages

| Language | Code | Language | Code |
|----------|------|----------|------|
| Afrikaans | `afr` | Sepedi (Northern Sotho) | `nso` |
| English | `eng` | Setswana | `tsn` |
| isiNdebele | `nbl` | Siswati | `ssw` |
| isiXhosa | `xho` | Tshivenda | `ven` |
| isiZulu | `zul` | Xitstonga | `tso` |
| Sesotho | `sot` |

## Dataset Structure

### Data Instances

Each instance contains a pair of aligned sentences with an alignment confidence score:

```json
{
  "afr": "Die Kabinet het sy kommer uitgespreek oor die onlangse arbeidsonrus...",
  "eng": "Cabinet expressed concern at recent labour unrest at Lonmin's Marikana Mine...",
  "score": 0.8649104,
  "__index_level_0__": 2
}
```

### Data Fields

- **`{lang1}`** (string): Source language sentence
- **`{lang2}`** (string): Target language sentence (aligned translation)
- **`score`** (float): Alignment confidence score (0.0 to 1.0) based on cosine similarity of LASER embeddings
- **`__index_level_0__`** (int): Original index in the full dataset

### Data Splits

Each language pair configuration has three splits:

| Split | Purpose | Size |
|-------|---------|------|
| `train` | Training | ~70% |
| `test` | Testing | ~15% |
| `eval` | Evaluation | ~15% |

## Dataset Creation

### Source Data

The dataset is created from South African government cabinet statements published on the official government website. These statements are professionally translated into all 11 official languages, making them a high-quality source for parallel text.

### Sentence Alignment Process

1. **Scraping**: Cabinet statements scraped from gov.za
2. **Tokenization**: Sentence tokenization using NLTK
3. **Preprocessing**: Language-specific text cleaning (URLs, titles, special characters)
4. **Embedding**: Sentence embeddings generated using LASER (Language-Agnostic SEntence Representations)
5. **Alignment**: Sentences aligned using cosine similarity of embeddings
6. **Filtering**: Alignment pairs filtered by confidence score threshold (>= 0.65)

## Usage

### Loading the Dataset

```python
from datasets import load_dataset

# Load specific language pair
dataset = load_dataset("dsfsi/govza-sa-cabinet-statements-sentence-aligned", "afr-eng")

# Access splits
train_data = dataset["train"]
test_data = dataset["test"]
eval_data = dataset["eval"]

# Iterate through examples
for example in train_data:
    source = example["afr"]
    target = example["eng"]
    confidence = example["score"]
    print(f"Score: {confidence:.2f}")
    print(f"AFR: {source}")
    print(f"ENG: {target}\n")
```

### Available Language Pair Configurations

The dataset includes the following configurations (language pairs):

<details>
<summary>Click to see all 55 language pair combinations</summary>

**Afrikaans pairs:** afr-eng, afr-nbl, afr-nso, afr-sot, afr-ssw, afr-tsn, afr-tso, afr-ven, afr-xho, afr-zul

**English pairs:** eng-nbl, eng-nso, eng-sot, eng-ssw, eng-tsn, eng-tso, eng-ven, eng-xho, eng-zul

**isiNdebele pairs:** nbl-nso, nbl-sot, nbl-ssw, nbl-tsn, nbl-tso, nbl-ven, nbl-xho, nbl-zul

**Sepedi pairs:** nso-sot, nso-ssw, nso-tsn, nso-tso, nso-ven, nso-xho, nso-zul

**Sesotho pairs:** sot-ssw, sot-tsn, sot-tso, sot-ven, sot-xho, sot-zul

**Siswati pairs:** ssw-tsn, ssw-tso, ssw-ven, ssw-xho, ssw-zul

**Setswana pairs:** tsn-tso, tsn-ven, tsn-xho, tsn-zul

**Xitstonga pairs:** tso-ven, tso-xho, tso-zul

**Tshivenda pairs:** ven-xho, ven-zul

**isiXhosa-isiZulu:** xho-zul

</details>

### Example: Training a Translation Model

```python
from datasets import load_dataset
from transformers import MarianMTModel, MarianTokenizer

# Load data
dataset = load_dataset("dsfsi/govza-sa-cabinet-statements-sentence-aligned", "afr-eng", split="train")

# Your training code here
# ...
```

## Alignment Quality

Alignment pairs are filtered by cosine similarity score >= 0.65. The distribution of alignment scores varies by language pair:

- **High-resource pairs** (e.g., eng-afr): Typically higher alignment scores (0.75-0.95)
- **Low-resource pairs** (e.g., ven-nbl): More varied scores (0.65-0.85)

Higher scores indicate stronger semantic similarity between aligned sentences.

## Considerations for Using the Data

### Social Impact of Dataset

This dataset supports:
- ✅ Development of translation systems for South African languages
- ✅ Research on low-resource language NLP
- ✅ Preservation and promotion of linguistic diversity
- ✅ Improved access to government information across language communities

### Limitations

- **Domain-specific**: Government/political domain - may not generalize to other domains
- **Formal register**: Professional translations in formal style
- **Alignment quality varies**: Some language pairs have fewer high-quality alignments
- **Historical context**: Statements reflect specific time periods and political contexts

## Additional Information

### Dataset Curators

- **Organization**: Data Science for Social Impact (DSFSI) Research Group
- **Institution**: University of Pretoria
- **Lead**: Vukosi Marivate ([@vukosi](https://twitter.com/vukosi))

### Licensing Information

- **Data License**: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)
- **Code License**: [MIT License](https://opensource.org/licenses/MIT)

### Citation Information

**Paper:**
```bibtex
@inproceedings{lastrucci-etal-2023-preparing,
    title = "Preparing the Vuk{'}uzenzele and {ZA}-gov-multilingual {S}outh {A}frican multilingual corpora",
    author = "Richard Lastrucci and Isheanesu Dzingirai and Jenalea Rajab and Andani Madodonga and Matimba Shingange and Daniel Njini and Vukosi Marivate",
    booktitle = "Proceedings of the Fourth workshop on Resources for African Indigenous Languages (RAIL 2023)",
    month = may,
    year = "2023",
    address = "Dubrovnik, Croatia",
    publisher = "Association for Computational Linguistics",
    url = "https://aclanthology.org/2023.rail-1.3",
    pages = "18--25"
}
```

**Dataset:**
```bibtex
@dataset{marivate_vukosi_2023_7635168,
  author       = {Marivate, Vukosi and
                  Shingange, Matimba and
                  Lastrucci, Richard and
                  Dzingirai, Isheanesu and
                  Rajab, Jenalea},
  title        = {The South African Gov-ZA multilingual corpus},
  month        = feb,
  year         = 2023,
  publisher    = {Zenodo},
  version      = {1.0},
  doi          = {10.5281/zenodo.7635168},
  url          = {https://doi.org/10.5281/zenodo.7635168}
}
```

### Disclaimer

This dataset contains machine-readable data extracted from online cabinet statements from the South African government, provided by the Government Communication Information System (GCIS). While efforts were made to ensure the accuracy and completeness of this data, there may be errors or discrepancies between the original publications and this dataset. No warranties, guarantees or representations are given in relation to the information contained in the dataset.

### Contributions

Thanks to [@vukosi](https://github.com/vukosi), [@MatimbaGitHub](https://github.com/MatimbaGitHub), and the DSFSI team for creating this dataset.

### Links

- 🏠 **Homepage**: https://github.com/dsfsi/gov-za-multilingual
- 📄 **Paper**: https://arxiv.org/abs/2303.03750
- 🗂️ **Source Code**: https://github.com/dsfsi/gov-za-multilingual
- 📊 **Zenodo**: https://doi.org/10.5281/zenodo.7635168
