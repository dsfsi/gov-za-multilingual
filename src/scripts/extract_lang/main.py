import os, re
from pathlib import Path

from pprint import pprint



ROOT_PATH = Path(os.path.abspath(__file__)).parent.parent.parent.parent
TOKEN_PATH = Path(ROOT_PATH / 'data' / 'tokenised')

def extract_lang(lang):
    out_path = Path(ROOT_PATH / 'data' / 'processed' / 'gov_za_tsn.txt')
    statement_folders = os.listdir(TOKEN_PATH)
    out_file = open(out_path, 'w')
    for folder in statement_folders:
        statement_path = Path(TOKEN_PATH / folder)
        statements = os.listdir(statement_path)
        for path in statements:
            if re.search(lang, path):
                txt_path = Path(statement_path / path) 
                txt_file = open(txt_path, 'r')
                txt = txt_file.read()
                out_file.write(txt)
    

if __name__ == '__main__':
    extract_lang('tsn')