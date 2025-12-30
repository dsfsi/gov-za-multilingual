from itertools import combinations

from tqdm import tqdm

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
    import sys
    import traceback

    print("=" * 60)
    print("Gov-ZA Multilingual Sentence Alignment")
    print("=" * 60)

    try:
        last_date = file_handler.extract_latest_date()
        print(f"Last processed date: {last_date}")

        cab_statements = file_handler.read_json_file()
        print(f"Total statements in database: {len(cab_statements)}")

        # Filter new statements
        new_statements = [s for s in cab_statements if s["datetime"] > last_date]
        print(f"New statements to process: {len(new_statements)}")

        if len(new_statements) == 0:
            print("\nNo new statements to process. Exiting.")
            sys.exit(0)

        print("\nSetting up LASER...")
        config.set_environ_var()
        config.setup_laser()
        config.download_laser_models(lang_model_map)
        config.download_tokeniser()
        print("✓ LASER setup complete\n")

        reversed_lang_map = {value: key for key, value in lang_map.items()}
        langs = list(lang_model_map.keys())
        lang_pairs = list(combinations(langs, 2))
        new_last_date = last_date

        print(f"Processing {len(new_statements)} statements...")
        for statement in tqdm(new_statements, desc="Statements", unit="stmt"):
            statement_date = statement["datetime"]
            statement_keys = list(statement.keys())

            try:
                # Tokenize and embed all languages
                available_langs = [(k, v) for k, v in lang_map.items() if k in statement]
                for lang_key, lang_code in tqdm(available_langs, desc=f"  Languages ({statement_date})", leave=False, unit="lang"):
                    text = statement[lang_key]["text"]
                    tokens = sentence_align.tokenise(lang_code, text)
                    processed = sentence_align.pre_process_text(lang_code, text)

                    file_handler.write_raw_to_file(statement_date, lang_code, text)
                    file_handler.write_raw_to_file(f'{statement_date}_processed', lang_code, processed)
                    file_handler.write_tokens_to_file(statement_date, lang_code, tokens)
                    sentence_embed.encode_sentence_tokens(statement_date, lang_code, lang_model_map[lang_code])

                # Align all language pairs
                relevant_pairs = [
                    (src, tgt) for src, tgt in lang_pairs
                    if reversed_lang_map[src] in statement_keys and reversed_lang_map[tgt] in statement_keys
                ]

                for src_lang, tgt_lang in tqdm(relevant_pairs, desc=f"  Aligning pairs", leave=False, unit="pair"):
                    sentence_align.sentence_alignment(src_lang, tgt_lang, statement_date)

                new_last_date = statement_date

            except Exception as e:
                print(f"\n⚠️  Error processing statement {statement_date}: {e}")
                print("Continuing with next statement...")
                continue

        file_handler.write_latest_date(new_last_date)

        print("\n" + "=" * 60)
        print("✓ Sentence alignment complete!")
        print(f"Processed {len(new_statements)} statements")
        print(f"Last processed date: {new_last_date}")
        print("=" * 60)

    except FileNotFoundError as e:
        print(f"\n❌ ERROR: File not found")
        print(f"   {e}")
        print("\nPlease ensure:")
        print("  1. You're running from src/sentence_alignment/ directory")
        print("  2. The data/govza-cabinet-statements.json file exists")
        print("  3. LASER submodule is properly initialized")
        sys.exit(1)

    except RuntimeError as e:
        print(f"\n❌ ERROR: {e}")
        sys.exit(1)

    except KeyboardInterrupt:
        print("\n\n⚠️  Interrupted by user")
        print(f"Progress saved up to: {new_last_date if 'new_last_date' in locals() else last_date}")
        sys.exit(130)

    except Exception as e:
        print(f"\n❌ UNEXPECTED ERROR: {e}")
        print("\nFull traceback:")
        traceback.print_exc()
        sys.exit(1)
