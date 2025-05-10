import datetime
import json, re, os
import time
import pandas as pd
from bs4 import BeautifulSoup
from urllib.request import urlopen, Request
import logging
from urllib.error import URLError, HTTPError

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("scraper.log"),
        logging.StreamHandler()
    ]
)

# List of languages to process
languages = ['en','af','nr','xh','zu','st','nso','tn','ss','ve','ts']

def read_JSON_file():
    """
    Read the JSON file containing cabinet statements.
    Returns an empty list if file doesn't exist or is invalid.
    """
    try:
        with open('../../data/govza-cabinet-statements.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data
    except FileNotFoundError:
        logging.warning("JSON file not found, starting with empty dataset")
        return []
    except json.JSONDecodeError:
        logging.error("Invalid JSON in file, starting with empty dataset")
        return []
    except Exception as e:
        logging.error(f"Unexpected error reading JSON file: {str(e)}")
        return []

def write_JSON_file(data):
    """Write data to JSON file with error handling"""
    try:
        os.makedirs(os.path.dirname('../../data/govza-cabinet-statements.json'), exist_ok=True)
        with open('../../data/govza-cabinet-statements.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        logging.info(f"Successfully wrote {len(data)} items to JSON file")
        return True
    except Exception as e:
        logging.error(f"Error writing JSON file: {str(e)}")
        return False

def update_csv_file(new_data, lang):
    """Update CSV file for a specific language"""
    if not new_data:
        logging.info(f"No new data to write for language: {lang}")
        return

    try:
        items = []
        for data in new_data:
            if lang not in data:
                logging.warning(f"Language {lang} not found in item with title: {data.get('title', 'Unknown')}")
                continue
                
            item = {
                'title': data[lang]['title'],
                'date': data['date'],
                'origin_url': data['url'],
                'url': data[lang]['url'],
                'text': data[lang]['text']
            }
            items.append(item)
            
        if not items:
            logging.info(f"No valid items for language: {lang}")
            return
            
        items_df = pd.DataFrame.from_dict(items)
        file_path = f'../../data/interim/govza-cabinet-statements-{lang}.csv'
        
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        if os.path.isfile(file_path):
            items_df.to_csv(file_path, mode='a', index=False, header=False)
        else:
            items_df.to_csv(file_path, mode='w', index=False, header=True)
            
        logging.info(f"Successfully updated CSV for language {lang} with {len(items)} items")
    except Exception as e:
        logging.error(f"Error updating CSV for language {lang}: {str(e)}")

def update_all_csv(new_data):
    """Update all CSV files for all languages"""
    for lang in languages:
        update_csv_file(new_data, lang)

def get_cabinent_statements_urls(last_date):
    """
    Get cabinet statement URLs until reaching a specific date
    with improved error handling and robustness
    """
    page_no = 0
    date_found = False
    cabinent_statements = []
    max_pages = 100  # Safety limit
    
    # Format date consistently
    try:
        last_date = last_date.strip().zfill(11) if isinstance(last_date, str) else last_date
        logging.info(f"Searching for cabinet statements newer than: {last_date}")
    except Exception as e:
        logging.error(f"Error formatting date: {str(e)}. Using default.")
        last_date = "14 Mar 2013"
    
    while not date_found and page_no < max_pages:
        try:
            url = f'https://www.gov.za/cabinet-statements?page={page_no}'
            headers = {'User-Agent': 'Mozilla/5.0 (compatible; GovZA Data Collector; +https://github.com/yourusername)'}
            
            # Add retry mechanism
            max_retries = 3
            for attempt in range(max_retries):
                try:
                    req = Request(url, headers=headers)
                    page = urlopen(req, timeout=30)
                    break
                except (URLError, HTTPError) as e:
                    if attempt < max_retries - 1:
                        logging.warning(f"Attempt {attempt+1} failed for page {page_no}: {str(e)}. Retrying...")
                        time.sleep(5)  # Exponential backoff could be implemented here
                    else:
                        raise
            
            doc = BeautifulSoup(page, 'html.parser')
            
            news_table = doc.find('tbody')
            if not news_table:
                logging.error(f"No table body found on page {page_no}")
                break
                
            news_table_rows = [row for row in news_table.contents if row != '\n']
            
            if not news_table_rows:
                logging.info(f"No rows found on page {page_no}, stopping")
                break
                
            items_on_page = 0
            for row in news_table_rows:
                try:
                    title_element = row.find('td')
                    if not title_element or not title_element.find('a'):
                        continue
                        
                    date_element = row.find_all('td')
                    if len(date_element) < 2:
                        continue
                        
                    statement = {
                        'title': title_element.find('a').text.strip(),
                        'date': date_element[1].text.strip(),
                        'url': 'https://www.gov.za' + row.find('a')["href"]
                    }
                    
                    if statement['date'] == last_date:
                        logging.info(f"Found target date: {last_date}")
                        date_found = True
                        break
                        
                    items_on_page += 1
                    cabinent_statements.append(statement)
                except Exception as e:
                    logging.warning(f"Error processing row on page {page_no}: {str(e)}")
                    continue
                    
            logging.info(f"Fetched {items_on_page} results from page {page_no+1} of Cabinet Statements")
            
            if items_on_page == 0:
                logging.warning("No items found on page, may indicate end of results")
                break
                
            # Be nice to the server
            time.sleep(2)
            page_no += 1
            
        except Exception as e:
            logging.error(f"Error fetching page {page_no}: {str(e)}")
            # More aggressive backoff on general error
            time.sleep(5)
            page_no += 1

    logging.info(f"Total statements collected: {len(cabinent_statements)}")
    return cabinent_statements

def check_translations(url):
    """Check for available translations with error handling"""
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (compatible; GovZA Data Collector; +https://github.com/yourusername)'}
        req = Request(url, headers=headers)
        page = urlopen(req, timeout=30)
        doc = BeautifulSoup(page, 'html.parser')
        
        title_element = doc.find('h1', class_='page-title')
        if not title_element:
            logging.warning(f"No title found for {url}")
            return []
            
        title = title_element.text.strip()
        
        translations = doc.find('div', id="block-languageswitcher")
        if not translations:
            logging.info(f"No translation block found for: {title}")
            return []
            
        trans_elements = translations.find_all('li')
        if len(trans_elements) < 2:  # Need at least 2 languages to consider it translated
            logging.info(f"Insufficient translations for: {title}")
            return []
            
        trans_urls = []
        for elem in trans_elements:
            try:
                if not elem.get('hreflang') or not elem.find('a'):
                    continue
                    
                trans_item = {
                    'lang': elem['hreflang'],
                    'url': 'https://www.gov.za' + elem.find('a')['href']
                }
                trans_urls.append(trans_item)
            except Exception as e:
                logging.warning(f"Error processing translation element: {str(e)}")
                
        if len(trans_urls) >= 2:  # At least 2 translations
            logging.info(f"Found {len(trans_urls)} translations for: {title}")
            return trans_urls
        else:
            logging.info(f"Insufficient valid translations for: {title}")
            return []
            
    except Exception as e:
        logging.error(f"Error checking translations for {url}: {str(e)}")
        return []

def extract_translations(url):
    """Extract translations with error handling and validation"""
    # Be nice to the server
    time.sleep(3)
    
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (compatible; GovZA Data Collector; +https://github.com/yourusername)'}
        req = Request(url, headers=headers)
        page = urlopen(req, timeout=30)
        doc = BeautifulSoup(page, 'html.parser')

        trans_urls = check_translations(url)
        if not trans_urls:
            return None
            
        logging.info(f"Extracting content from {url} and {len(trans_urls)} translations")
        
        statement = {}
        
        title_element = doc.find('h1', class_='page-title')
        if not title_element:
            logging.warning(f"No title found for {url}")
            return None
            
        time_element = doc.find('time')
        if not time_element:
            logging.warning(f"No time element found for {url}")
            return None
            
        statement['title'] = title_element.text.strip()
        statement['date'] = time_element.text.strip()
        statement['datetime'] = time_element.get('datetime', '')[0:10] if time_element.get('datetime') else ''
        statement['url'] = url
        
        # Process each translation
        for trans in trans_urls:
            try:
                time.sleep(2)  # Be nice to the server
                req_trans = Request(trans['url'], headers=headers)
                page_trans = urlopen(req_trans, timeout=30)
                doc_trans = BeautifulSoup(page_trans, 'html.parser')
                
                title_trans = doc_trans.find('h1', class_='page-title')
                if not title_trans:
                    logging.warning(f"No title found for translation {trans['lang']}")
                    continue
                    
                text_trans = doc_trans.find('div', class_='field field--name-body field--type-text-with-summary field--label-hidden field__item')
                if not text_trans:
                    logging.warning(f"No content found for translation {trans['lang']}")
                    continue
                    
                statement[trans['lang']] = {
                    'text': text_trans.text.replace('\xa0', ' ').strip(),
                    'title': title_trans.text.strip(),
                    'url': trans['url']
                }
                
            except Exception as e:
                logging.error(f"Error processing translation {trans['lang']} for {url}: {str(e)}")
                
        # Ensure English translation exists (primary language)
        if 'en' not in statement:
            logging.warning(f"No English translation for {url}, skipping")
            return None
            
        # Check if any translations exist
        translation_langs = [lang for lang in languages if lang in statement and lang != 'en']
        if not translation_langs:
            logging.info(f"No translations found for {url}, skipping")
            return None
            
        # Check if translations are actually different (not just copied English text)
        has_real_translation = False
        en_text = statement.get('en', {}).get('text', '')
        
        for lang in translation_langs:
            if lang in statement and statement[lang]['text'] != en_text:
                has_real_translation = True
                break
                
        if not has_real_translation:
            logging.info(f"No genuine translations for {url}, English text repeated in all languages")
            return None

        logging.info(f"Successfully extracted: {statement['title']}")
        return statement
        
    except Exception as e:
        logging.error(f"Error extracting translations for {url}: {str(e)}")
        return None