import json
from db import DB, Article

from nltk.tokenize import sent_tokenize

# load the data
with open('data/raw.json') as f:
    data = json.load(f)

for uid, value in data.items():
    print(uid)
    print(value)
    with DB:
        _ = Article.create(
            uid=uid,
            content=value['text'],
            url=value['link'],
            title=value['title']
        )
    print(_)

    # need to save the data in an essay_db sqlite database with columns uid, text, url, title

    break


# Chunking text
def get_chunks(text, max_len_chars = 1800):
    curr_size = 0
    chunks = [[]]
    for sent in sent_tokenize(text):
        if curr_size < max_len_chars:
            chunks[-1].append(sent)
            curr_size += len(sent)
        else:
            chunks[-1] = ' '.join(chunks[-1])
            chunks.append([])
            curr_size = 0
            
    if curr_size: chunks[-1] = ' '.join(chunks[-1])
    return chunks