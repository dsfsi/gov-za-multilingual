import os
import subprocess
from pathlib import Path

import numpy

from config import LASER_PATH
from file_handler import TOKEN_PATH, EMBED_PATH


def encode_sentence_tokens(date, lang, lang_model):
    os.makedirs(EMBED_PATH / date, exist_ok=True)
    input_path = Path(TOKEN_PATH / date / f'{date}_{lang}.txt')
    output_path = Path(EMBED_PATH / date / f'{date}_{lang}.emb')
    command = f'bash {LASER_PATH}/tasks/embed/embed.sh '  # the command without params
    command += f'{input_path} {output_path} {lang_model}'  # add params which are source text, output path & lang model
    subprocess.run(command, shell=True)  # run the bash command using the shell


def decode_sentences(date, lang):
    dim = 1024
    embed_path = Path(EMBED_PATH / date / f'{date}_{lang}.emb')
    vector_list = numpy.fromfile(embed_path, dtype=numpy.float32, count=-1)
    vector_list.resize(vector_list.shape[0] // dim, dim)
    return vector_list
