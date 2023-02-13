import re
import os
import pandas as pd
import numpy as np
from config import LoadConfig
from nltk import tokenize
from sklearn.metrics.pairwise import cosine_similarity
from datetime import datetime
from itertools import combinations


SENTENCE_ALIGN_OUTPUT_PATH = "./../../data/sentence_align_output/"


def align_files(source_file, target_file, source_lang, target_lang, f, g):
    #   Create Paths to use to output the aligned files to
    csv_path = SENTENCE_ALIGN_OUTPUT_PATH

    if not os.path.exists(csv_path):
        os.mkdir(csv_path)

    used_sentences = []  # This is used keep record of indexes used as target sentences
    df = pd.DataFrame(columns=["src_text", "trg_text", "cosine_score"])
    loop_iter = min([len(source_file), len(target_file), len(f), len(g)])

    for i in range(loop_iter):                          # range(len(source_file)):
        similarity_array = {}

        for j in range(loop_iter):                      # range(len(target_file)):
            if j not in used_sentences:
                source_sent = source_file[i]
                target_sent = target_file[j]

                # Calculate the similarity between sentences
                sim_score = cosine_similarity(source_sent.reshape(1, -1), target_sent.reshape(1, -1))
                similarity_array[j] = sim_score[0][0]

        max_similar = max(similarity_array, key=similarity_array.get, default=0)
        used_sentences.append(max_similar)

        # Create dataframe to store sentences
        df = df.append({'src_text': f['text'][i], 'trg_text': g['text'][max_similar], 'cosine_score': similarity_array[max_similar]}, ignore_index=True)

    # Output full dataframe to a csv file
    out_put_file = "aligned_" + source_lang + "_" + target_lang
    df.columns= df.columns.str.lower()


    if os.path.exists(csv_path + out_put_file + ".csv"):
        df.to_csv(csv_path + out_put_file + ".csv", sep=',', index=False, mode='a', header=False)
    else:
        df.to_csv(csv_path + out_put_file + ".csv", sep=',', index=False)


def get_embeddings(f, g, source_embeddings, target_embeddings, source_model, target_model):
    embed_file_path = "LASER/tasks/embed/embed.sh"
    os.system(f"bash {embed_file_path} {f.name} {source_embeddings} {source_model}")
    os.system(f"bash {embed_file_path} {g.name} {target_embeddings} {target_model}")

    k = os.path.realpath(f"{source_embeddings}")
    y = os.path.realpath(f"{target_embeddings}")
    dim = 1024

    source_file_arr = np.fromfile(k, dtype=np.float32, count=-1)
    source_file_arr.resize(source_file_arr.shape[0] // dim, dim)

    target_file_arr = np.fromfile(y, dtype=np.float32, count=-1)
    target_file_arr.resize(target_file_arr.shape[0] // dim, dim)

    return source_file_arr, target_file_arr


def pre_process_text(input_text):
    input_text = re.sub(r'^[. ]?[\d]+[. ]', '', input_text)                     #   Remove a single/multi digit starting a line e.g. 7.
    input_text = re.sub(r'[.\] ]?[\d]+[.][\d]+[.]', '. ', input_text)           #   Replace Numbers e.g. .2.2. with period
    input_text = re.sub(r'[.\] ]?[\d]+[.]', '. ', input_text)                   #   Replace Numbers e.g. .2. with period
    input_text = re.sub(r'^[.]+', ' ', input_text)                              #   Remove any dots starting a line'
    input_text = re.sub(r'[.:;,\( ]+?[a-zA-Z][.\) ]', ' ', input_text)          #   Replace a period / colon / semi-colon followed by a letter with a period
    
    return input_text


def split_sentences_characters(input_text):
    output_array = []
    text = tokenize.sent_tokenize(pre_process_text(input_text))
    for s in text:
        text = re.split('\s{2,}', s)  # Finds 2 or more white spaces
        for j in text:
            text = re.split('#n#', j)
            for k in text:
                output_array.append(k)

    return output_array


def create_embeddings(source_lang, target_lang, lang, data, last_date):
    #   Get corresponding models for the languages
    source_model = lang[source_lang]
    target_model = lang[target_lang]

    last_date = last_date.replace("_", "-")
    last_date = datetime.strptime(last_date, '%Y-%m-%d')
    last_date = last_date.strftime('%Y_%m_%d')

    date_key = last_date

    for i in range(0, len(data)):
        current_date = data["date_key"][i]
        if datetime(int(current_date[0:4]), int(current_date[5:7]), int(current_date[8:10])) > datetime(int(last_date[0:4]), int(last_date[5:7]), int(last_date[8:10])):
            dict_src = data[source_lang][i]
            dict_targ = data[target_lang][i]
            src_file = source_lang + "_" + data["date_key"][i]
            trg_file = target_lang + "_" + data["date_key"][i]

            src_sentences = split_sentences_characters(dict_src.get("text"))
            trg_sentences = split_sentences_characters(dict_targ.get("text"))

            #   Read in the file
            with open("./content/sample_data/%s.txt" % src_file, 'w') as f:
                for item in src_sentences:
                    if item.strip() and len(item) > 3:
                        f.write((str(item)))
                        f.write("\n")

            with open("%s.txt" % trg_file, 'w') as g:
                for item in trg_sentences:
                    if item.strip() and len(item) > 3:
                        g.write((str(item)))
                        g.write("\n")

            source_embeddings = source_lang + "_" + data["date_key"][i] + "_emb"
            target_embeddings = target_lang + "_" + data["date_key"][i] + "_emb"

            src_data_frame = pd.read_csv(f.name, sep="\r\n", engine="python", header=None, names=['text'])
            trg_data_frame = pd.read_csv(g.name, sep="\r\n", engine="python", header=None, names=['text'])

            source_file_arr, target_file_arr = get_embeddings(f, g, source_embeddings, target_embeddings, source_model, target_model)

            date_key = data['date_key'][i]
            align_files(source_file_arr, target_file_arr, source_lang, target_lang, src_data_frame, trg_data_frame)

    return date_key


if __name__ == "__main__":
    # Create language mappings
    language_mappings = {
        'eng': '',
        'afr': '',
        'nbl': '',
        'xho': 'xho_Latn',
        'zul': 'zul_Latn',
        'sot': '',
        'nso': 'nso_Latn',
        'tsn': 'tsn_Latn',
        'ssw': 'ssw_Latn',
        'ven': '',
        'tso': 'tso_Latn'
    }

    # Create unique 2-pairs of languages
    languages = list(language_mappings.keys())
    language_pairs = list(combinations(languages, 2))

    #   Install models and all necessary files
    config = LoadConfig()

    #   Download the models
    config.download_models(language_mappings)

    #   Get the speeches data json
    speeches_data = pd.read_json("./../../data/govza-cabinet-statements.json")

    #   Create new column with the date - replaced by _
    speeches_data['date_key'] = speeches_data['date'].astype(str).str.replace('-', '_')

    #   Rename the columns to match the language mappings
    speeches_data.rename(columns={'en':'eng'}, inplace=True)
    speeches_data.rename(columns={'af':'afr'}, inplace=True)
    speeches_data.rename(columns={'nr':'nbl'}, inplace=True)
    speeches_data.rename(columns={'xh':'xho'}, inplace=True)
    speeches_data.rename(columns={'zu':'zul'}, inplace=True)
    speeches_data.rename(columns={'st':'sot'}, inplace=True)
    speeches_data.rename(columns={'nso':'nso'}, inplace=True)
    speeches_data.rename(columns={'tn':'tsn'}, inplace=True)
    speeches_data.rename(columns={'ss':'ssw'}, inplace=True)
    speeches_data.rename(columns={'ve':'ven'}, inplace=True)
    speeches_data.rename(columns={'ts':'tso'}, inplace=True)

    #    Read in the last date that embeddings were created
    with open(f"./last_date.txt", 'r') as file:
        last_date = file.read()

    #   Create embeddings & align files
    for (first_lang, second_lang) in language_pairs:
        out_put_file = "aligned_" + first_lang + "_" + second_lang
        csv_path = SENTENCE_ALIGN_OUTPUT_PATH

        if first_lang != 'eng':
            SRC_LANG = first_lang
            TRG_LANG = second_lang
            new_date = create_embeddings(SRC_LANG, TRG_LANG, language_mappings, speeches_data, last_date)

            #   Do some cleaning
            os.system(f'rm *.txt')                              #   Remove all text files in current directory
            os.system(f'rm *_emb')                              #   Remove all embeddings files in current directory
            os.system(f'rm ./content/sample_data/*.txt')        #   Remove all csv files in current directory


    #   Write the new date to the file
    with open(f"./last_date.txt", 'w') as file:
        file.write(new_date)

    #   Create a table with the number of aligned pairs
    with open("filtered_data.txt", 'w') as filtered_file:
        csv_files = os.listdir(SENTENCE_ALIGN_OUTPUT_PATH)
        filtered_file.write("|----------|----------|-------------------|\n")
        filtered_file.write("| src_lang | trg_lang | num_aligned_pairs |\n")
        filtered_file.write("|----------|----------|-------------------|\n")

        for csv_file in csv_files:
            df = pd.read_csv(SENTENCE_ALIGN_OUTPUT_PATH + csv_file)
            df = df[df["cosine_score"] >= 0.65]
            strip_file_name = re.split("[_.]", csv_file)

            filtered_file.write("|" + " " + strip_file_name[1] +" " * 5 + " " + "|" + " " + strip_file_name[2] + " " * 5 + " " + "|" + " " + str(len(df)) + " " * (17 - len(str(len(df)))) + " " + "|\n")
    
        filtered_file.write("|----------|----------|-------------------|\n")