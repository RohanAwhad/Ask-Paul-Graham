import re
import json
import requests
import pandas as pd

from collections import defaultdict
from bs4 import BeautifulSoup
from loguru import logger

HOST = 'http://www.paulgraham.com/'

# Get a list of all articles on the home page
articles_page = BeautifulSoup(requests.get(HOST+'/articles.html').text, 'lxml')
all_articles = articles_page.table.find_all('table')[1].find_all('a')
logger.info(f'Found {len(all_articles)} articles')

data = defaultdict(dict)
for article in all_articles:
    try:
        href = article.get('href')
        if href.startswith('http'): continue
        uid = href[:-len('.html')]

        link = HOST + article.get('href')
        logger.info(f'Processing {link}...')
        res = requests.get(link)
        soup = BeautifulSoup(res.text, 'lxml')
        _tmp = ' '.join([s for s in soup.font.strings][1:])
        text = re.sub(' +', ' ', _tmp.replace('\n', ' '))
        logger.info('Processing done ...')

        data[uid]['link'] = link
        data[uid]['title'] = article.string
        data[uid]['text'] = text
    except:
        logger.error(f'Error processing {link}')

with open('data/raw.json', 'w') as f:
    json.dump(data, f)
logger.info('Data saved to data/raw.json')

# create a dataframe
df = pd.DataFrame.from_dict(data, orient='index')
print(df.head())
