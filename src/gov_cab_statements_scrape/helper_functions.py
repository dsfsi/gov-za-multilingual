import datetime
import json, re, os
import pandas as pd
from bs4 import BeautifulSoup
from urllib.request import urlopen, Request

languages = ['en','af','nr','xh','zu','st','nso','tn','ss','ve','ts']

def read_JSON_file():
    try:
        with open('../../data/govza-cabinet-statements.json', 'r') as f:
            data = json.load(f)
        return data
    except:
        return []

def write_JSON_file(data):
    with open('../../data/govza-cabinet-statements.json', 'w') as f:
        f.write(json.dumps(data))
    return

def update_csv_file(new_data ,lang):
    items = []
    for data in new_data:
        item = {}
        item['title'] = data[lang]['title']
        item['date'] = data['date']
        item['origin_url'] = data['url']
        item['url'] = data[lang]['url']
        item['text'] = data[lang]['text']
        items.append(item)
    items = pd.DataFrame.from_dict(items)
    file_path = '../../data/interim/govza-cabinet-statements-'+lang + '.csv'
    if os.path.isfile(file_path):
        items.to_csv(file_path, mode='a', index=False, header=False) #if file exists, don't write headers
    else:
        items.to_csv(file_path, mode='a', index=False, header=True) #if file doesn't exists, write headers

def update_all_csv(new_data):
    for lang in languages:
        update_csv_file(new_data, lang)
    

def get_cabinent_statements_urls(date):
    page_no = 0
    date_found = False
    cabinent_statements = []

    while date_found == False:
        url = 'https://www.gov.za/cabinet-statements?page=' + str(page_no)
        req = Request(url)
        page = urlopen(req)
        doc = BeautifulSoup(page, 'html.parser')

        news_table = doc.tbody
        news_table_rows = news_table.contents
        i=0
        for row in news_table_rows:
            statement = {}
            statement['title'] = row.find('td').find('a').text
            statement['date'] = row.find_all('td')[1].text.strip()
            statement['url'] = 'https://www.gov.za'+row.find('a')["href"]
            if statement['date'] == date:
                date_found = True
                break
            i+=1
            cabinent_statements.append(statement)
        print("Fetched " + str(i) + " results from page " + str(page_no+1) + " of Cabinet Statements")
        page_no += 1

    return cabinent_statements


def check_translations(url): #build dictonary of translation urls
    req = Request(url)
    page = urlopen(req)
    doc = BeautifulSoup(page, 'html.parser')

    title = (doc.find('h1', class_='title').text)
    translations = doc.find('section', id="block-locale-language") 
    if translations != None:
        trans_elements = translations.find_all('li')
        trans_urls = []
        for i in range(len(languages)):
            trans_item = {}
            trans_item['lang'] = languages[i]
            trans_item['url'] = 'https://www.gov.za' + trans_elements[i].find('a')['href']
            trans_urls.append(trans_item)
        print("Translations found for " + title)
        return trans_urls 
    else:
        print("No translations available for " + title)
        return []


def extract_translations(url):
    req = Request(url)
    page = urlopen(req)
    doc = BeautifulSoup(page, 'html.parser')

    trans_urls = check_translations(url)
    if len(trans_urls) > 0:
        print("Extracting...")
        statement = {}
        statement['title'] = (doc.find('h1', class_='title').text)
        statement['date'] = doc.find('span', class_='date-display-single').text
        statement['datetime'] = doc.find('span', class_='date-display-single')['content'][0:10]
        statement['url'] = url
        for trans in trans_urls:
            req_trans = Request(trans['url'])
            page_trans = urlopen(req_trans)
            doc_trans = BeautifulSoup(page_trans, 'html.parser')
            title_trans = doc_trans.find('h1', class_='title').text
            text_trans = doc_trans.find('div',class_='field field-name-body field-type-text-with-summary field-label-hidden').text.replace('\xa0',' ')
            statement[trans['lang']] = {'text':text_trans, 'title':title_trans, 'url': trans['url']}
        print ("Extracted: " + statement['title']) 
        return statement
    