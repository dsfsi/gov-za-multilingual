import json
import re
from bs4 import BeautifulSoup
from urllib.request import urlopen, Request

def read_JSON_file():
    try:
        with open('sample.json', 'r') as f:
            data = json.load(f)
        return data
    except:
        return []

def write_JSON_file(data):
    with open("sample.json", "w") as f:
        f.write(json.dumps(data))

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

        for row in news_table_rows:
            statement = {}
            statement['title'] = row.find('td').find('a').text
            statement['date'] = row.find_all('td')[1].text.strip()
            statement['url'] = 'https://www.gov.za'+row.find('a')["href"]
            if statement['date'] == date:
                date_found = True
                break
            cabinent_statements.append(statement)
        print("Fetched page " + str(page_no+1) + " of Cabinet Statements")
        page_no += 1

    return cabinent_statements


def check_translations(url):
    languages = ['en','af','nr','xh','zu','st','nso','tn','ss','ve','ts']

    req = Request(url)
    page = urlopen(req)
    doc = BeautifulSoup(page, 'html.parser')

    translations = doc.find('section', id="block-locale-language") 
    if translations != None:
        trans_elements = translations.find_all('li')
        trans_urls = []
        for i in range(len(languages)):
            trans_item = {}
            trans_item['lang'] = languages[i]
            trans_item['url'] = 'https://www.gov.za' + trans_elements[i].find('a')['href']
            trans_urls.append(trans_item)
        return trans_urls 
    else:
        return []


def extract_translations(url):
    req = Request(url)
    page = urlopen(req)
    doc = BeautifulSoup(page, 'html.parser')

    trans_urls = check_translations(url)
    if len(trans_urls) > 0:
        statement = {}
        statement['title'] = re.sub("[^\u0000-\u007F]+", " ",(doc.find('h1', class_='title').text))
        statement['date'] = doc.find('span', class_='date-display-single').text
        statement['datetime'] = doc.find('span', class_='date-display-single')['content']
        statement['url'] = url
        for trans in trans_urls:
            req_trans = Request(trans['url'])
            page_trans = urlopen(req_trans)
            doc_trans = BeautifulSoup(page_trans, 'html.parser')
            title_trans = re.sub("[^\u0000-\u007F]+", " ", doc_trans.find('h1', class_='title').text)
            text_trans = re.sub(
                "[^\u0000-\u007F]+", 
                " ",
                doc_trans.find('div',class_='field field-name-body field-type-text-with-summary field-label-hidden').text.replace('\xa0',' '))
            statement[trans['lang']] = {'text':text_trans, 'title':title_trans, 'url': trans['url']}
        print ("Extracted Statement: " + statement['title'])
        return statement
