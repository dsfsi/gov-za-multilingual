from itertools import combinations

import config as c
import file_handler as f
import sentence_align as sa
import sentence_embed as se

lang_map = {
    "af": "afr",
    "en": "eng",
    "nr": "nbl",
    "nso": "nso",
    "ss": "ssw",
    "st": "sot",
    "tn": "tsn",
    "ts": "tso",
    "ve": "ven",
    "xh": "xho",
    "zu": "zul",
}

lang_model_map = {
    "afr": "",
    "eng": "",
    "nbl": "",
    "nso": "nso_Latn",
    "sot": "sot_Latn",
    "ssw": "ssw_Latn",
    "tsn": "tsn_Latn",
    "tso": "tso_Latn",
    "ven": "",
    "xho": "xho_Latn",
    "zul": "zul_Latn",
}

if __name__ == "__main__":
    lastdate = f.extract_latest_date()
    cab_statements = f.read_json_file()

    c.set_environ_var()
    c.setup_laser()
    c.download_laser_models(lang_model_map)
    c.download_tokeniser()

    for statement in cab_statements:
        if statement["datetime"] > lastdate:
            print(statement["datetime"] + " // " + lastdate)
            for k in lang_map.keys():
                if k in statement:
                    tokens = sa.tokenise(lang_map[k], statement[k]["text"])
                    date = statement["datetime"]
                    processed = sa.pre_process_text(lang_map[k], statement[k]["text"])
                    f.write_raw_to_file(date, lang_map[k], statement[k]["text"])
                    f.write_raw_to_file('{}_processed'.format(date), lang_map[k], processed)
                    f.write_tokens_to_file(date, lang_map[k], tokens)
                    se.encode_sentence_tokens(date, lang_map[k], lang_model_map[lang_map[k]])

    langs = lang_model_map.keys()
    lang_pairs = list(combinations(langs, 2))
    new_lastdate = lastdate
    for statement in cab_statements:
        for (src_lang, tgt_lang) in lang_pairs:
            if statement["datetime"] > lastdate and (src_lang in statement and tgt_lang in statement):
                print('We are here')
                sa.sentence_alignment(src_lang, tgt_lang, statement["datetime"])

        if statement["datetime"] > lastdate:
            new_lastdate = statement["datetime"]
            print("Aligned cab statement on {}".format(statement["datetime"]))

    f.write_latest_date(new_lastdate)
