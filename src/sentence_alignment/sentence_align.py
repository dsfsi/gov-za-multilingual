import re

import nltk
from sklearn.metrics.pairwise import cosine_similarity
from urlextract import URLExtract

from file_handler import get_tokens, write_to_jsonl
from sentence_embed import decode_sentences


def tokenise(lang, text):  # -> str
    output_array = []
    text = pre_process_text(lang, text)  # clean data
    text = nltk.tokenize.sent_tokenize(text)  # tokenise data
    for i in text:
        text = re.split(r'\s{2,}', i)
        for j in text:
            text = re.split(r'#n#', j)
            for k in text:
                output_array.append(k)

    return output_array


def remove_urls(input_text):
    extractor = URLExtract()
    urls = extractor.find_urls(input_text)
    for url in urls:
        input_text = re.sub(url, 'WEBTOKEN', input_text)
    return input_text


def fix_person_titles(lang, input_text):
    if lang == "afr":
        input_text = re.sub(r'Mnr.', 'Mnr', input_text)
        input_text = re.sub(r'Me.', 'Me', input_text)
        input_text = re.sub(r'Adv.', 'Adv', input_text)
        input_text = re.sub(r'mnr.', 'mnr', input_text)
        input_text = re.sub(r'Meneer.', 'Meneer', input_text)
        input_text = re.sub(r'Prof.', 'Prof', input_text)
        input_text = re.sub(r'Wetnr.', 'Wetnr', input_text)
    elif lang == "eng":
        input_text = re.sub(r'Mnr.', 'Mnr', input_text)
        input_text = re.sub(r'Meneer.', 'Meneer', input_text)
        input_text = re.sub(r'Prof.', 'Prof', input_text)
    elif lang == "nbl":
        input_text = re.sub(r'kuNom.', 'KuNom.', input_text)
        input_text = re.sub(r'KuNom.', 'KuNom', input_text)
        input_text = re.sub(r'UDorh.', 'UDorh', input_text)
        input_text = re.sub(r'UMm.', 'UMm', input_text)
        input_text = re.sub(r'UNom.', 'UNom', input_text)
        input_text = re.sub(r'noPhrof.', 'noPhrof', input_text)
    elif lang == "nso":
        pass
    elif lang == "ssw":
        input_text = re.sub(r'Umnu.', 'Umnu', input_text)
        input_text = re.sub(r'Mk.', 'Mk', input_text)
        input_text = re.sub(r'KuMnu.', 'KuMnu', input_text)
        input_text = re.sub(r'Mnu.', 'Mnu', input_text)
        input_text = re.sub(r'noPhrof.', 'noPhrof', input_text)
    elif lang == "sot":
        pass
    elif lang == "tsn":
        pass
    elif lang == "tso":
        pass
    elif lang == "ven":
        pass
    elif lang == "xho":
        pass
    elif lang == "zul":
        pass
    return input_text


def pre_process_text(lang, input_text):
    input_text = re.sub(r'\s{2,}', ' ', input_text)  # Replace more than 2 spaces with a single space
    input_text = re.sub(r'(\d{4})(\d)', r'\1.\2',
                        input_text)  # Adds a full stop in between a year and a section number 20237.1 > 2023.7.1
    input_text = re.sub(r'\.\d{1,2}\.\d{1,2}\.', '.', input_text)
    input_text = re.sub(r'\s\d{1,2}\.\d\s', ' ', input_text)
    input_text = re.sub(r'\s\d{1,2}\.\d{1,2}\.\s', ' ', input_text)
    input_text = re.sub(r'\d{1,2}\.\d{1,2}\.', '.', input_text)
    input_text = re.sub(r'\.\d{1,2}\.', '.', input_text)
    input_text = remove_urls(input_text)
    input_text = re.sub(r'[\w.+-]+@[\w-]+\.[\w.-]+', 'EMAILTOKEN', input_text)  # Remove Email
    input_text = re.sub(r'\s\d{1,2}\.\s', ' ', input_text)
    input_text = re.sub(r'([A-z])(\d{1,2}\.)', r'\1.', input_text)
    input_text = re.sub(r'[A-Z]\.\s', '', input_text)
    input_text = re.sub(r'([A-z]\.)([A-z])', r'\1 \2', input_text)
    input_text = re.sub(r'<}0{>', ' ', input_text)
    input_text = re.sub(r'\([a-z]\)', '', input_text)
    input_text = re.sub(r';', '', input_text)
    input_text = fix_person_titles(lang, input_text)

    return input_text


def cosine_score(src, tgt):
    return cosine_similarity(src.reshape(1, -1), tgt.reshape(1, -1))[0][0]


def align(vectors, tokens):
    (i, j) = (0, 0)
    src_vect, tgt_vect = vectors
    src_tokens, tgt_tokens = tokens
    sentences = []
    while i < len(src_vect) and j < len(tgt_vect):
        score = cosine_score(src_vect[i], tgt_vect[j])
        if i == 0 and score < 0.7:
            return None
        elif score < 0.6:
            return sentences
        else:
            sentence = {
                "src": src_tokens[i],
                "tgt": tgt_tokens[j],
                "score": str(score),
            }
            sentences.append(sentence)
        (i, j) = (i + 1, j + 1)
    return sentences


def update_indices(indexes, vectors):
    (i, j) = indexes
    (best_i, best_j) = (-1, -1)
    src_vect, tgt_vect = vectors
    threshold = 0.7

    for x in range(0, 3):
        for y in range(0, 3):
            i_temp, j_temp = i + y, j + x

            if i_temp < len(src_vect) and j_temp < len(tgt_vect):
                score = cosine_score(src_vect[i_temp], tgt_vect[j_temp])

                if score > threshold:
                    (best_i, best_j) = (i_temp, j_temp)
                    break

        if best_i != -1 and best_j != -1:
            break

    if best_i != -1 and best_j != -1:
        return best_i, best_j
    else:
        return i + 1, j + 1


def sentence_alignment(src, tgt, date):
    src_tokens = get_tokens(date, src)
    tgt_tokens = get_tokens(date, tgt)
    src_vectors = decode_sentences(date, src)
    tgt_vectors = decode_sentences(date, tgt)

    aligned_sentences = []
    (i, j) = (0, 0)
    factor = 5

    while i + factor < len(src_tokens) and j + factor < len(tgt_tokens):
        some_sentences = align(
            (src_vectors[i:i + factor], tgt_vectors[j:j + factor]),
            (src_tokens[i:i + factor], tgt_tokens[j:j + factor])
        )

        if some_sentences is not None and len(some_sentences) > 0:
            aligned_sentences.extend(some_sentences)
            length = len(some_sentences)
            (i, j) = (i + length, j + length)
        else:
            (last_i, last_j) = (i, j)
            (i, j) = update_indices((i, j), (src_vectors, tgt_vectors))

            if (last_i, last_j) == (i, j):
                print("failed to realign indexes, exiting...")
                break

    write_to_jsonl(src, tgt, aligned_sentences)
