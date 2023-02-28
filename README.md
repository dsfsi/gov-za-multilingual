The South African Gov-ZA multilingual corpus
==============================
Github: https://github.com/dsfsi/gov-za-multilingual
Zenodo: 

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


Authors
-------
- Vukosi Marivate - [@vukosi](https://twitter.com/vukosi)
- Matimba Shingange
- Richard Lastrucci
- Isheanesu Joseph Dzingirai
- Jenalea Rajab

Citation
--------
Vukosi Marivate, Matimba Shingange, Richard Lastrucci, Isheanesu Joseph Dzingirai, Jenalea Rajab. **The South African Gov-ZA multilingual corpus**, 2022

Licences
-------
* License for Data - [CC 4.0 BY SA](LICENSE_data.md)
* Licence for Code - [MIT License](LICENSE)
