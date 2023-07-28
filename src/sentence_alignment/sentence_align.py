
from sklearn.metrics.pairwise import cosine_similarity

from file_handler import get_tokens, append_to_csv
from sentence_embed import decode_sentences

import numpy as np

def cosine_score(src, tgt):
  return cosine_similarity(src.reshape(1,-1), tgt.reshape(1,-1))[0][0]

def remove_element_at_index(arr, index):
    if index < 0 or index >= len(arr):
        raise IndexError("Index out of range")
    
    new_array = np.concatenate((arr[:index], arr[index+1:]))
    return new_array

def sentence_alignment(src, tgt, date):
  src_tokens = get_tokens(date, src)
  tgt_tokens = get_tokens(date, tgt)
  src_vectors_orig = decode_sentences(date, src)
  tgt_vectors_orig = decode_sentences(date, tgt)
  aligned_sentences = []
  unaligned_src_sentences = []

  (k,l) = (0,5)
  tgt_vectors = tgt_vectors_orig.copy()
  src_vectors = src_vectors_orig.copy()
  
  for i, vector in enumerate(src_vectors_orig):

    
    candidates = get_tgt_vector_canditates(tgt_vectors_orig, k, l)
    tgt_info = max_sentence(0.7, vector, candidates)

    if tgt_info == None:
      unaligned_src_sentences.append(src)
      continue
    else:
      tgt_i = tgt_info["index"]
      src_sentence =src_tokens[tgt_i]
      tgt_sentence =tgt_tokens[tgt_i]
      tgt_vectors = remove_element_at_index(tgt_vectors, tgt_i)
      src_vectors = remove_element_at_index(src_vectors, tgt_i)
      tgt_tokens = remove_element_at_index(tgt_tokens, tgt_i)
      src_tokens = remove_element_at_index(src_tokens, tgt_i)
      if l == len(tgt_vectors)-1:
         (k,l) = (k,l-1)
      aligned_sentences.append(  {
          "src" : src_sentence,
          "tgt" : tgt_sentence,
          "score" : tgt_info["score"]
        }
      )

  return aligned_sentences

    

def max_sentence(threshhold, src, candidates):
  max = float("-inf")

  for i,cand in enumerate(candidates):
    score=cosine_score(src, cand)
    if score >= threshhold:
      return {
        "tgt" : cand,
        "score" : score,
        "index" : i
      }
  
  return None

def get_tgt_vector_canditates(vectors, i, j):
    return vectors[i:j]
  

# def sentence_alignment(src, tgt, date):
#   src_tokens = get_tokens(date, src)
#   tgt_tokens = get_tokens(date, tgt)
#   src_vector = decode_sentences(date, src)
#   tgt_vector = decode_sentences(date, tgt)

#   used_sentences = []
#   loop_iter = min(len(src_tokens),len(src_vector), len(tgt_tokens), len(tgt_vector))
  
#   src_sentences=[]
#   tgt_sentences=[]
#   cosine_scores=[]

#   for i in range(loop_iter):
#     similarity_dict = {}
#     for j in range(loop_iter-1):
#       if j in used_sentences:
#         continue
#       else:
#         src_embed = src_vector[i]
#         tgt_embed = tgt_vector[i]
#         sim_score = cosine_score(src_embed, tgt_embed)
#         similarity_dict[j]= sim_score

#     max_similar = max(similarity_dict, key = similarity_dict.get, default=0)
#     used_sentences.append(max_similar)

#     if max_similar == 0:
#       continue
#     tgt_sentences.append(tgt_tokens[max_similar])
#     src_sentences.append(src_tokens[i])
#     cosine_scores.append(similarity_dict[max_similar])

#   print("Writing {} for {}-{} to csv...".format(date, src, tgt))
#   append_to_csv(src, tgt, src_sentences, tgt_sentences, cosine_scores)



# def align():