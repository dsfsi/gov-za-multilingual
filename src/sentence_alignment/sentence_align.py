
import nltk, re

def tokenise(text): # -> str
  text = pre_process_text(text) # clean data
  return nltk.tokenize.sent_tokenize(text) #tokenise data

def pre_process_text(input_text):
    input_text = re.sub(r'^[. ]?[\d]+[. ]', '', input_text)                     #   Remove a single/multi digit starting a line e.g. 7.
    input_text = re.sub(r'[.\] ]?[\d]+[.][\d]+[.]', '. ', input_text)           #   Replace Numbers e.g. .2.2. with period
    input_text = re.sub(r'[.\] ]?[\d]+[.]', '. ', input_text)                   #   Replace Numbers e.g. .2. with period
    input_text = re.sub(r'^[.]+', ' ', input_text)                              #   Remove any dots starting a line'
    input_text = re.sub(r'[.:;,\( ]+?[a-zA-Z][.\) ]', ' ', input_text)          #   Replace a period / colon / semi-colon followed by a letter with a period
    
    return input_text
