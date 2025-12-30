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
