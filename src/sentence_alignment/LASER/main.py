import re
import os
import pandas as pd
import numpy as np
from config import LoadConfig
from nltk import tokenize
from sklearn.metrics.pairwise import cosine_similarity


def align_files(source_file, target_file, source_lang, target_lang, f, g, date_key):
    #   Create Paths to use to output the aligned files to
    path = f'./data/{source_lang}_{target_lang}_aligned/'
    path_csv = f'./data/{source_lang}_{target_lang}_aligned_csv/'

    if not os.path.exists(path):
        os.mkdir(path)

    if not os.path.exists(path_csv):
        os.mkdir(path_csv)

    used_sentences = []  # This is used keep record of indexes used as target sentences
    df = pd.DataFrame(columns=[source_lang, target_lang, "src_text", "trg_text", "Cosine_Score"])
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
        df = df.append({source_lang: source_file[i], target_lang: target_file[max_similar], 'src_text': f['text'][i],
                        'trg_text': g['text'][max_similar], 'Cosine_Score': similarity_array[max_similar]},
                       ignore_index=True)

    # Output full dataframe to a csv file
    out_put_file = date_key + "_" + source_lang + "_" + target_lang
    df.to_csv(path_csv + out_put_file + ".csv", sep=',', index=False)

    df['src_text'].to_csv(path + date_key + "_" + source_lang + '_aligned' + '.txt', header=None, index=None, sep='\t',
                          mode='a')
    df['trg_text'].to_csv(path + date_key + "_" + target_lang + '_aligned' + '.txt', header=None, index=None, sep='\t',
                          mode='a')

    return df


def get_embeddings(f, g, source_embeddings, target_embeddings, source_model, target_model):
    embed_file_path = "tasks/embed/embed.sh"
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
    input_text = re.sub("(;[a-z]\.)", "", input_text)           #   Replace ;a. with nothing
    input_text = re.sub('\d\.\d.', "", input_text)              #   Replace Numbers e.g. 2.2. with nothing
    input_text = re.sub('\.\d.', "", input_text)                #   Replace .1. with nothing
    input_text = re.sub('[A-Za-z]\.', "", input_text)           #   Replace A. with nothing
    input_text = re.sub('^\.', "", input_text)                  #   Remove any dots starting a line
    input_text = re.sub('^\b\d\b.+', "", input_text)            #   Remove a single digit starting a line e.g. 7.

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


def create_embeddings(source_lang, target_lang, lang, data):
    #   Get corresponding models for the languages
    source_model = lang[source_lang]
    target_model = lang[target_lang]

    df = None

    for i in range(0, len(data)):
        print("Execution")
        dict_src = data[source_lang][i]
        dict_targ = data[target_lang][i]
        src_file = source_lang + "_" + data["date_key"][i]
        trg_file = target_lang + "_" + data["date_key"][i]

        src_sentences = split_sentences_characters(dict_src.get("text"))
        trg_sentences = split_sentences_characters(dict_targ.get("text"))

        print("Opening and writing to files")
        # Read in the file
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

        source_file_arr, target_file_arr = get_embeddings(f, g, source_embeddings, target_embeddings, source_model,
                                                          target_model)

        date_key = data['date_key'][i]
        df = align_files(source_file_arr, target_file_arr, source_lang, target_lang, src_data_frame, trg_data_frame,
                           date_key)

    return df


if __name__ == "__main__":
    # Create language mappings
    language_mappings = {'en': '', 'af': '', 'nr': '', 'xh': 'xho_Latn', 'zu': 'zul_Latn', 'st': '', 'nso': 'nso_Latn', 'tn': 'tsn_Latn',
                 'ss': 'ssw_Latn', 've': '', 'ts': 'sot_Latn', 'tso': 'tso_Latn'}

    #   Install models and all necessary files
    config = LoadConfig()

    #   Download the models
    config.download_models(language_mappings)

    #   Get the speeches data json
    speeches_data = pd.read_json("../../../data/govza-cabinet-statements.json")

    #   Create new column with the date - replaced by _ as well as rename Xitsonga column
    speeches_data['date_key'] = speeches_data['date'].astype(str).str.replace('-', '_')
    speeches_data.rename(columns={'ts last': 'tso'}, inplace=True)

    #   Create embeddings & align files
    SRC_LANG = "xh"
    TRG_LANG = "en"

    data_frame = create_embeddings("xh", "en", language_mappings, speeches_data)
    
    #   Find the text files
    txt_folder = f'./data/{SRC_LANG}_{TRG_LANG}_aligned_csv'              # Change when loading different files

    txt_files = []
    for root, folder, files in os.walk(txt_folder):
        for file in files:
            if file.endswith('.csv'):
                txt_files.append(file)

    print(txt_files)
    #
    # df = pd.DataFrame(txt_files, columns=['File_Name'])
    # df["language"] = ''
    # df_files = pd.concat((pd.read_csv(txt_folder + '/' + f) for f in txt_files), ignore_index=True)
    # df_files.loc[df_files['Cosine_Score'] > 0.7].src_text.to_csv(r'20221002_tso.txt', header=None, index=None, sep=' ')
    # df_files.loc[df_files['Cosine_Score'] > 0.7].trg_text.to_csv(r'20221002_eng.txt', header=None, index=None, sep=' ')
    #
    # np.savetxt(r'20221002_tso.txt', df_files.loc[df_files['Cosine_Score'] > 0.7].src_text, fmt='%s')
    # np.savetxt(r'20221002_eng.txt', df_files.loc[df_files['Cosine_Score'] > 0.7].trg_text, fmt='%s')
