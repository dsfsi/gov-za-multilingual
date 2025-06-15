from itertools import combinations

import config
import file_handler
import sentence_align
import sentence_embed

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
    last_date = file_handler.extract_latest_date()
    cab_statements = file_handler.read_json_file()

    config.set_environ_var()
    config.setup_laser()
    config.download_laser_models(lang_model_map)
    config.download_tokeniser()

    langs = list(lang_model_map.keys())
    lang_pairs = list(combinations(langs, 2))
    new_last_date = last_date

    for statement in cab_statements:
        statement_date = statement["datetime"]
        if statement_date <= last_date:
            continue

        print(f"{statement_date} // {last_date}")

        for lang_key, lang_code in lang_map.items():
            if lang_key in statement:
                text = statement[lang_key]["text"]
                tokens = sentence_align.tokenise(lang_code, text)
                processed = sentence_align.pre_process_text(lang_code, text)

                file_handler.write_raw_to_file(statement_date, lang_code, text)
                file_handler.write_raw_to_file(f'{statement_date}_processed', lang_code, processed)
                file_handler.write_tokens_to_file(statement_date, lang_code, tokens)
                sentence_embed.encode_sentence_tokens(statement_date, lang_code, lang_model_map[lang_code])

        for src_lang, tgt_lang in lang_pairs:
            if src_lang in statement and tgt_lang in statement:
                sentence_align.sentence_alignment(src_lang, tgt_lang, statement_date)

        new_last_date = statement_date
        print(f"Aligned cab statement on {statement_date}")

    file_handler.write_latest_date(new_last_date)
