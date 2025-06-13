# A module for all file related functions
import os, re, json, pandas
from pathlib import Path

ROOT_PATH = Path(os.path.abspath(__file__)).parent.parent.parent # gov-za/

JSON_PATH = Path(ROOT_PATH / "data" / "govza-cabinet-statements.json")
TOKEN_PATH = Path(ROOT_PATH / "data" / "tokenised")
EMBED_PATH = Path(ROOT_PATH / "data" / "embed")
OUT_PATH = Path(ROOT_PATH / "data" / "opt_aligned_out")
RAW_PATH = Path(ROOT_PATH / "data" / "raw")

def extract_latest_date():
    """
    ### Reads the value stored in `last_edition_read.txt` which stores the last edition which underwent SA.
    """

    file_path =  Path(
            Path(os.path.abspath(__file__)).parent #src/sentence_alignment
            / 'last_edition_read.txt' 
        )

    if not os.path.exists(file_path):
        open(file_path , 'w')

    date = open(file_path,'r').read() #read as str

    if not re.match(r'^\d{4}-\d{2}-\d{2}$', date):
        date = '2013-05-02'
    return date

def write_latest_date(date):
    """
    Writes an edition to last_edition_read.txt
    """
    open(
        Path(
            Path(os.path.abspath(__file__)).parent #src/sentence_alignment
            / 'last_edition_read.txt'
        ),'w').write(date)

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
    
def write_raw_to_file(date, lang, text):
    if not os.path.exists(RAW_PATH / date):
        os.makedirs(RAW_PATH / date)

    path = Path(RAW_PATH / date / "{}_{}.txt".format(date, lang))

    f = open(path, "w")
    f.write("{}\n".format(text))

    
    
def write_tokens_to_file(date, lang, tokens):
    if not os.path.exists(TOKEN_PATH / date):
        os.makedirs(TOKEN_PATH / date)
    
    path = Path(TOKEN_PATH / date / "{}_{}.txt".format(date, lang))
    
    if os.path.exists(path):
        f = open(path, "a")
        for t in tokens:
            f.write("{}\n".format(t))
    else:   
        f = open(path, "w")
        for t in tokens:
            f.write("{}\n".format(t))

    print("Written {} tokens for {} to file".format(lang, date))
    f.close()

def get_tokens(date, lang):
    token_path = Path(TOKEN_PATH / date / "{}_{}.txt".format(date, lang))
    return open(token_path, 'r').readlines()
    
def append_to_csv(src,tgt,src_sentences,tgt_sentences, sim_scores):
    data = {
        "src_text" : src_sentences,
        "tgt_text" : tgt_sentences,
        "cosine_score" : sim_scores
    }

    df = pandas.DataFrame(data)
    csv_path = Path(OUT_PATH / "aligned_{}_{}.csv".format(src, tgt))

    if not os.path.exists(OUT_PATH):
        os.makedirs(OUT_PATH)

    if os.path.exists(csv_path):
        df.to_csv(csv_path, mode="a", header=False, index=False)
    else:
        df.to_csv(csv_path, mode="w", header=True, index=False)

def write_to_jsonl(src,tgt,date,data):
    file_name = "aligned-{}-{}.jsonl".format(src, tgt)
    file_path = OUT_PATH  / file_name

    if not os.path.exists(OUT_PATH):
        os.makedirs(OUT_PATH)

    if file_name in os.listdir(OUT_PATH):
        f = open(file_path, 'a')
        for d in data:
            f.write(json.dumps(d) + '\n')
    else:
        f = open(file_path, 'w')
        for d in data:
            f.write(json.dumps(d) + '\n')

    # print("Aligned {}-{} from Cab Statement on {}".format(src,tgt, date))