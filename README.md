The South African gov-za-multilingual corpus
==============================
About Dataset
---------------------
The data set contains cabinet statements from the South African government. Data was scraped from the governments website:
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
| nso      | ven      | 6367              |
| xho      | ssw      | 18387             |
| tsn      | ssw      | 16386             |
| tsn      | tso      | 16681             |
| afr      | tso      | 14936             |
| xho      | ven      | 4559              |
| nso      | ssw      | 18697             |
| zul      | ven      | 3606              |
| sot      | ven      | 14098             |
| nbl      | nso      | 6342              |
| xho      | eng      | 16537             |
| nbl      | tso      | 4465              |
| nbl      | sot      | 16163             |
| afr      | eng      | 14549             |
| xho      | tsn      | 16571             |
| tso      | eng      | 16068             |
| zul      | ssw      | 18563             |
| nbl      | ven      | 18984             |
| sot      | nso      | 8077              |
| sot      | tsn      | 5450              |
| nso      | eng      | 15257             |
| zul      | tso      | 17789             |
| ven      | tso      | 4578              |
| afr      | sot      | 8834              |
| ssw      | eng      | 15721             |
| afr      | zul      | 14998             |
| afr      | xho      | 16065             |
| afr      | nso      | 15388             |
| nbl      | xho      | 5213              |
| zul      | sot      | 5975              |
| afr      | ssw      | 15610             |
| sot      | ssw      | 5811              |
| nbl      | eng      | 3616              |
| xho      | nso      | 18110             |
| nbl      | ssw      | 4655              |
| nbl      | tsn      | 3369              |
| nbl      | zul      | 3868              |
| nso      | tso      | 17617             |
| nso      | tsn      | 16179             |
| ssw      | tso      | 17880             |
| ven      | eng      | 3670              |
| zul      | nso      | 17630             |
| xho      | zul      | 18145             |
| tsn      | ven      | 3267              |
| afr      | tsn      | 12605             |
| sot      | eng      | 5212              |
| zul      | tsn      | 16482             |
| ssw      | ven      | 4588              |
| afr      | ven      | 5776              |
| afr      | nbl      | 6621              |
| sot      | tso      | 6586              |
| xho      | sot      | 7489              |
| xho      | tso      | 17954             |
| zul      | eng      | 16149             |
| tsn      | eng      | 14544             |


Authors
-------
- Vukosi Marivate - [@vukosi](https://twitter.com/vukosi)
- Matimba Shingange
- Richard Lastrucci
- Isheanesu Joseph Dzingirai

Citation
--------
Vukosi Marivate, Matimba Shingange, Richard Lastrucci, Isheanesu Joseph Dzingirai. **Cabinet statements from the SA governemnt in multiple languages - gov-za-multilingual**, 2022

Licences
-------
* License for Data - [CC 4.0 BY SA](LICENSE_data.md)
* Licence for Code - [MIT License](LICENSE)
