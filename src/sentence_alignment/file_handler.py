# A module for all file related functions
import json
import os
import re
from pathlib import Path

import pandas

ROOT_PATH = Path(os.path.abspath(__file__)).parent.parent.parent  # gov-za-multilingual/
JSON_PATH = Path(ROOT_PATH / 'data' / 'govza-cabinet-statements.json')
TOKEN_PATH = Path(ROOT_PATH / 'data' / 'tokenised')
EMBED_PATH = Path(ROOT_PATH / 'data' / 'embed')
OUT_PATH = Path(ROOT_PATH / 'data' / 'opt_aligned_out')
RAW_PATH = Path(ROOT_PATH / 'data' / 'raw')


def extract_latest_date():
    """
    ### Reads the value stored in `last_edition_read.txt` which stores the last edition which underwent SA.
    """
    path = Path(__file__).resolve().parent / 'last_edition_read.txt'
    date = (path.read_text(encoding='utf-8').strip() if path.exists() else '')
    return date if re.match(r'^\d{4}-\d{2}-\d{2}$', date) else '2013-05-02'


def write_latest_date(date):
    """
    Writes an edition to last_edition_read.txt
    """
    file_path = Path(__file__).resolve().parent / 'last_edition_read.txt'
    file_path.write_text(date, encoding='utf-8')


def read_json_file():
    """
    ### Reads in govza-cabinet-statements.json
    """
    with open(JSON_PATH, 'r', encoding='utf-8') as json_file:
        return json.load(json_file)


def write_raw_to_file(date, lang, text):
    os.makedirs(RAW_PATH / date, exist_ok=True)
    path = Path(RAW_PATH / date / f'{date}_{lang}.txt')
    with open(path, 'w', encoding='utf-8') as raw_file:
        raw_file.write(f'{text}\n')


def write_tokens_to_file(date, lang, tokens):
    os.makedirs(TOKEN_PATH / date, exist_ok=True)
    path = Path(TOKEN_PATH / date / f'{date}_{lang}.txt')
    file_mode = 'a' if os.path.exists(path) else 'w'

    with open(path, file_mode, encoding='utf-8') as token_file:
        for token in tokens:
            token_file.write(f'{token}\n')


def get_tokens(date, lang):
    token_path = Path(TOKEN_PATH / date / f'{date}_{lang}.txt')
    return open(token_path, 'r', encoding='utf-8').readlines()


def append_to_csv(src, tgt, src_sentences, tgt_sentences, sim_scores):
    data = {
        'src_text': src_sentences,
        'tgt_text': tgt_sentences,
        'cosine_score': sim_scores
    }

    df = pandas.DataFrame(data)
    csv_path = Path(OUT_PATH / f'aligned_{src}_{tgt}.csv')
    os.makedirs(OUT_PATH, exist_ok=True)
    mode, header = ('w', True) if not os.path.exists(csv_path) else ('a', False)
    df.to_csv(csv_path, mode=mode, header=header, index=False)


def write_to_jsonl(src, tgt, data):
    file_name = "aligned-{}-{}.jsonl".format(src, tgt)
    file_path = OUT_PATH / file_name
    os.makedirs(OUT_PATH, exist_ok=True)
    mode = 'a' if file_path.exists() else 'w'

    with open(file_path, mode, encoding='utf-8') as f:
        for entry in data:
            f.write(json.dumps(entry) + '\n')
