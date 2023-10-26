The South African Gov-ZA multilingual corpus
==============================

[![Automated Sentence Alignment of Cabinet Speeches CI](https://github.com/dsfsi/gov-za-multilingual/actions/workflows/sentence_alignment_build.yml/badge.svg)](https://github.com/dsfsi/gov-za-multilingual/actions/workflows/sentence_alignment_build.yml)

Github: https://github.com/dsfsi/gov-za-multilingual

Zenodo: [![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.7635167.svg)](https://doi.org/10.5281/zenodo.7635167)

Arxiv Preprint: [![arXiv](https://img.shields.io/badge/arXiv-2303.03750-b31b1b.svg)](https://arxiv.org/abs/2303.03750)

View main dataset on [Datasette](https://lite.datasette.io/?json=https%3A%2F%2Fraw.githubusercontent.com%2Fdsfsi%2Fgov-za-multilingual%2Fmaster%2Fdata%2Fgovza-cabinet-statements.json)

Give Feedback 📑: [DSFSI Resource Feedback Form](https://docs.google.com/forms/d/e/1FAIpQLSf7S36dyAUPx2egmXbFpnTBuzoRulhL5Elu-N1eoMhaO7v10w/formResponse){:target="_blank"}

About Dataset
---------------------
The data set contains cabinet statements from the South African government, maintained by the [Government Communication and Information System (GCIS)](https://www.gcis.gov.za/). Data was scraped from the governments website:
https://www.gov.za/cabinet-statements

The datasets contain government cabinet statements in 11 languages, namely:

|  Language  | Code |  Language  | Code |
|------------|------|------------|------|
| English    | (eng) | Sepedi     | (nso) |
| Afrikaans  | (afr) | Setswana   | (tsn) |
| isiNdebele | (nbl) | Siswati    | (ssw) |
| isiXhosa   | (xho) | Tshivenda  | (ven) |
| isiZulu    | (zul) | Xitstonga  | (tso) |
| Sesotho    | (sot) |


The dataset contains the full data in a JSON file (/data/govza-cabinet-statements.json), as well as CSV’s split by each language, eg: “govza-cabinet-statements-en.csv” for english.
The dataset does not contain special characters like unicode or ascii.

Please see the [data-statement.md](/data_statement.md) for full dataset information. *(TODO)*

Number of Aligned Pairs with Cosine Similarity Score >= 0.65
------------------------------------------------------------

| src_lang | trg_lang | num_aligned_pairs |
|----------|----------|-------------------|
|   nbl    | ven      | 18984             |
|   nso    | ssw      | 18697             |
|   zul    | ssw      | 18563             |
|   xho    | ssw      | 18387             |
|   xho    | zul      | 18145             |
|   xho    | nso      | 18110             |
|   xho    | tso      | 17954             |
|   ssw    | tso      | 17880             |
|   zul    | tso      | 17789             |
|   zul    | nso      | 17630             |
|   nso    | tso      | 17617             |
|   tsn    | tso      | 16681             |
|   xho    | tsn      | 16571             |
|   xho    | eng      | 16537             |
|   zul    | tsn      | 16482             |
|   tsn    | ssw      | 16386             |
|   nso    | tsn      | 16179             |
|   nbl    | sot      | 16163             |
|   zul    | eng      | 16149             |
|   tso    | eng      | 16068             |
|   afr    | xho      | 16065             |
|   ssw    | eng      | 15721             |
|   afr    | ssw      | 15610             |
|   afr    | nso      | 15388             |
|   nso    | eng      | 15257             |
|   afr    | zul      | 14998             |
|   afr    | tso      | 14936             |
|   afr    | eng      | 14549             |
|   tsn    | eng      | 14544             |
|   sot    | ven      | 14098             |
|   afr    | tsn      | 12605             |
|   afr    | sot      | 8834              |
|   sot    | nso      | 8077              |
|   xho    | sot      | 7489              |
|   afr    | nbl      | 6621              |
|   sot    | tso      | 6586              |
|   nso    | ven      | 6367              |
|   nbl    | nso      | 6342              |
|   zul    | sot      | 5975              |
|   sot    | ssw      | 5811              |
|   afr    | ven      | 5776              |
|   sot    | tsn      | 5450              |
|   nbl    | xho      | 5213              |
|   sot    | eng      | 5212              |
|   nbl    | ssw      | 4655              |
|   ssw    | ven      | 4588              |
|   ven    | tso      | 4578              |
|   xho    | ven      | 4559              |
|   nbl    | tso      | 4465              |
|   nbl    | zul      | 3868              |
|   ven    | eng      | 3670              |
|   nbl    | eng      | 3616              |
|   zul    | ven      | 3606              |
|   nbl    | tsn      | 3369              |
|   tsn    | ven      | 3267              |

Disclaimer
-------
This dataset contains machine-readable data extracted from online cabinet statements from the South African government, provided by the Government Communication Information System (GCIS). While efforts were made to ensure the accuracy and completeness of this data, there may be errors or discrepancies between the original publications and this dataset. No warranties, guarantees or representations are given in relation to the information contained in the dataset. The members of the Data Science for Societal Impact Research Group bear no responsibility and/or liability for any such errors or discrepancies in this dataset. The Government Communication Information System (GCIS) bears no responsibility and/or liability for any such errors or discrepancies in this dataset. It is recommended that users verify all information contained herein before making decisions based upon this information.

Authors
-------
- Vukosi Marivate - [@vukosi](https://twitter.com/vukosi)
- Matimba Shingange
- Richard Lastrucci
- Isheanesu Joseph Dzingirai
- Jenalea Rajab

Citation
--------
Paper

[Preparing the Vuk'uzenzele and ZA-gov-multilingual South African  multilingual corpora](https://arxiv.org/pdf/2303.03750)

> @inproceedings{lastrucci-etal-2023-preparing,
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

Dataset

Vukosi Marivate, Matimba Shingange, Richard Lastrucci, Isheanesu Joseph Dzingirai, Jenalea Rajab. **The South African Gov-ZA multilingual corpus**, 2022

> @dataset{marivate_vukosi_2023_7635168,
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


Licences
-------
* License for Data - [CC 4.0 BY](LICENSE_data.md)
* Licence for Code - [MIT License](LICENSE)
