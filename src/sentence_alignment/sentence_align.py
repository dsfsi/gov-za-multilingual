
from sklearn.metrics.pairwise import cosine_similarity

from file_handler import get_tokens, append_to_csv
# from sentence_tokenise import 
from sentence_embed import decode_sentences

def cosine_score(src, tgt):
  return cosine_similarity(src.reshape(1,-1), tgt.reshape(1,-1))[0][0]

def sentence_alignment(src, tgt, date):
  src_tokens = get_tokens(date, src)
  tgt_tokens = get_tokens(date, tgt)
  src_vector = decode_sentences(date, src)
  tgt_vector = decode_sentences(date, tgt)

  used_sentences = []
  loop_iter = min(len(src_tokens),len(src_vector), len(tgt_tokens), len(tgt_vector))
  
  src_sentences=[]
  tgt_sentences=[]
  cosine_scores=[]

  for i in range(loop_iter):
    similarity_dict = {}
    for j in range(loop_iter-1):
      if j in used_sentences:
        continue
      else:
        src_embed = src_vector[i]
        tgt_embed = tgt_vector[i]
        sim_score = cosine_score(src_embed, tgt_embed)
        similarity_dict[j]= sim_score

    max_similar = max(similarity_dict, key = similarity_dict.get, default=0)
    used_sentences.append(max_similar)

    if max_similar == 0:
      continue
    tgt_sentences.append(tgt_tokens[max_similar])
    src_sentences.append(src_tokens[i])
    cosine_scores.append(similarity_dict[max_similar])

  print("Writing {} for {}-{} to csv...".format(date, src, tgt))
  append_to_csv(src, tgt, src_sentences, tgt_sentences, cosine_scores)



# def align():