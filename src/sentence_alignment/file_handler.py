# A module for all file related functions
import json
import os
from pathlib import Path
import re
import subprocess

from config import laser_path as LASER_PATH
ROOT_PATH = Path(os.path.abspath(__file__)).parent.parent.parent # gov-za/

JSON_PATH = Path(ROOT_PATH / "data" / "govza-cabinet-statements.json")
TOKEN_PATH = Path(ROOT_PATH / "data" / "tokenised")
EMBED_PATH = Path(ROOT_PATH / "data" / "embed")



def extract_latest_edition():
    """
    ### Reads the value stored in `last_edition_read.txt` which stores the last edition which underwent SA.
    """

    file_path =  Path(
            Path(os.path.abspath(__file__)).parent #src/sentence_alignment
            / 'last_edition_read.txt' 
        )

    if not os.path.exists(file_path):
        open(file_path , 'w')

    edition = open(file_path,'r').read() #read as str

    if not re.match('^\d{4}-\d{2}-\d{2}$', edition): 
        edition = '2013-05-02'
    return edition

def read_JSON_file():
    """
    ### Reads in govza-cabinet-statements.json
    """
    try:
        with open(JSON_PATH, 'r') as f:
            data = json.load(f)
        return data
    except:
        return []
    
def write_tokens_to_file(date, lang, tokens):
    if not os.path.exists(TOKEN_PATH / date):
        os.makedirs(TOKEN_PATH / date)
    
    path = Path(TOKEN_PATH / date / "{}_{}.txt".format(date, lang))
    
    if os.path.exists(path):
        f = open(path, "a");
        for t in tokens:
            f.write("{}\n".format(t))
    else:   
        f = open(path, "w");
        for t in tokens:
            f.write("{}\n".format(t))

    print("Written {} tokens for {} to file".format(lang, date))
    f.close()
    
def encode_sentence_tokens(date, lang, lang_model): 
    if not os.path.exists(EMBED_PATH / date):
        os.makedirs(EMBED_PATH / date)
    
    input_path = Path(TOKEN_PATH / date / "{}_{}.txt".format(date, lang))
    output_path = Path(EMBED_PATH / date / "{}_{}.emb".format(date, lang))
    
    command = f'bash {LASER_PATH}/tasks/embed/embed.sh ' # the command without params
    command += "{} {} {}".format(input_path, output_path, lang_model) # add params which are source text, output path & lang model
    subprocess.run(command, shell=True) # run the bash command using the shell