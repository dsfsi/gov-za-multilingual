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
| afr      | eng      | 14549             |
| nbl      | eng      | 3616              |    
| nso      | eng      | 15257             |
| sot      | eng      | 5212              |
| ssw      | eng      | 15721             |
| tsn      | eng      | 14544             |
| tso      | eng      | 16068             |
| ven      | eng      | 3670              |
| xho      | eng      | 16537             |
| zul      | eng      | 16149             |


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
