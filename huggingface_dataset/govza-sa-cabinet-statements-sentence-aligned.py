"""Gov-ZA Cabinet Statements Sentence-Aligned Dataset Loading Script"""

import datasets
import pandas as pd


_DESCRIPTION = """\
This dataset contains sentence-aligned parallel text from South African government cabinet statements
in 11 official languages. The data is sourced from the Government Communication and Information System (GCIS).
"""

_HOMEPAGE = "https://github.com/dsfsi/gov-za-multilingual"

_LICENSE = "CC-BY-4.0"

_CITATION = """\
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
"""

# All 55 language pair configurations
_LANGUAGE_PAIRS = [
    "afr-eng", "afr-nbl", "afr-nso", "afr-sot", "afr-ssw", "afr-tsn", "afr-tso", "afr-ven", "afr-xho", "afr-zul",
    "eng-nbl", "eng-nso", "eng-sot", "eng-ssw", "eng-tsn", "eng-tso", "eng-ven", "eng-xho", "eng-zul",
    "nbl-nso", "nbl-sot", "nbl-ssw", "nbl-tsn", "nbl-tso", "nbl-ven", "nbl-xho", "nbl-zul",
    "nso-sot", "nso-ssw", "nso-tsn", "nso-tso", "nso-ven", "nso-xho", "nso-zul",
    "sot-ssw", "sot-tsn", "sot-tso", "sot-ven", "sot-xho", "sot-zul",
    "ssw-tsn", "ssw-tso", "ssw-ven", "ssw-xho", "ssw-zul",
    "tsn-tso", "tsn-ven", "tsn-xho", "tsn-zul",
    "tso-ven", "tso-xho", "tso-zul",
    "ven-xho", "ven-zul",
    "xho-zul"
]


class GovZAConfig(datasets.BuilderConfig):
    """BuilderConfig for Gov-ZA sentence-aligned dataset."""

    def __init__(self, language_pair, **kwargs):
        """
        Args:
            language_pair: Language pair in format 'src-tgt' (e.g., 'afr-eng')
            **kwargs: keyword arguments forwarded to super.
        """
        super(GovZAConfig, self).__init__(**kwargs)
        self.language_pair = language_pair
        self.lang1, self.lang2 = language_pair.split("-")


class GovZACabinetStatements(datasets.GeneratorBasedBuilder):
    """Gov-ZA Cabinet Statements Sentence-Aligned Dataset."""

    VERSION = datasets.Version("1.0.0")

    BUILDER_CONFIGS = [
        GovZAConfig(
            name=pair,
            version=VERSION,
            description=f"Sentence-aligned {pair.split('-')[0]}-{pair.split('-')[1]} parallel corpus",
            language_pair=pair,
        )
        for pair in _LANGUAGE_PAIRS
    ]

    BUILDER_CONFIG_CLASS = GovZAConfig

    def _info(self):
        lang1, lang2 = self.config.language_pair.split("-")

        features = datasets.Features(
            {
                lang1: datasets.Value("string"),
                lang2: datasets.Value("string"),
                "score": datasets.Value("float"),
                "__index_level_0__": datasets.Value("int64"),
            }
        )

        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=features,
            homepage=_HOMEPAGE,
            license=_LICENSE,
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""
        lang_pair = self.config.language_pair

        # Data files are organized as: {lang_pair}/{split}/0000.parquet
        data_dir = dl_manager.download_and_extract("")

        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={
                    "filepath": f"{lang_pair}/train/0000.parquet",
                    "split": "train",
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TEST,
                gen_kwargs={
                    "filepath": f"{lang_pair}/test/0000.parquet",
                    "split": "test",
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split.VALIDATION,
                gen_kwargs={
                    "filepath": f"{lang_pair}/eval/0000.parquet",
                    "split": "validation",
                },
            ),
        ]

    def _generate_examples(self, filepath, split):
        """Yields examples."""
        df = pd.read_parquet(filepath)

        for idx, row in df.iterrows():
            yield idx, row.to_dict()
