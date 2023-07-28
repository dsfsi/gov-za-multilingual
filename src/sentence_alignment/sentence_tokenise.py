
import re, nltk
from urlextract import URLExtract

def remove_urls(input_text): 
  extractor = URLExtract()
  urls = extractor.find_urls(input_text)
  for url in urls:
    input_text = re.sub(url, 'WEBTOKEN', input_text) 
  return input_text

def fix_person_titles(lang, input_text): 
  if lang == "afr":
    input_text = re.sub(r'Mnr.', 'Mnr', input_text)
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
  input_text = re.sub(r'\s{2,}', ' ', input_text) 
  input_text = re.sub(r'(\d{4})(\d)', r'\1.\2', input_text) 
  input_text = re.sub(r'\.\d{1,2}\.\d{1,2}\.', '.', input_text) 
  input_text = re.sub(r'\s\d{1,2}\.\d\s', ' ', input_text)
  input_text = re.sub(r'\s\d{1,2}\.\d{1,2}\.\s', ' ', input_text)
  input_text = re.sub(r'\d{1,2}\.\d{1,2}\.', ' ', input_text)
  input_text = re.sub(r'\.\d{1,2}\.', '.', input_text)
  input_text = remove_urls(input_text)
  input_text = re.sub(r'[\w.+-]+@[\w-]+\.[\w.-]+', 'EMAILTOKEN', input_text) # Remove Email
  input_text = re.sub(r'\s\d{1,2}\.\s', '.', input_text)
  input_text = re.sub(r'([A-z]{2,})(\d{1,2}\.)', r'\1.', input_text)
  input_text = re.sub(r'[A-Z]\.\s', '', input_text)
  input_text = re.sub(r'([A-z]\.)([A-z]){2,}', r'\1 \2', input_text)
  input_text = re.sub(r'<}0{>', ' ', input_text)
  input_text = fix_person_titles(lang,  input_text)
    
  return input_text

def tokenise(lang, text): # -> str
  output_array = []
  text = pre_process_text(lang, text) # clean data
  text = nltk.tokenize.sent_tokenize(text) #tokenise data
  for i in text:
    text = re.split('\s{2,}',i)
    for j in text:
      text = re.split('#n#',j)
      for k in text:
        output_array.append(k)

  return output_array

