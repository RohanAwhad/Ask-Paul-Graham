import json
from db import DB, Article, Chunk

from nltk.tokenize import sent_tokenize

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

def loader():
    # load the data
    with open('data/raw.json') as f:
        data = json.load(f)

    for uid, value in data.items():
        text = value['text'].replace('"', "'")

        with DB:
            article, _ = Article.get_or_create(
                uid=uid,
                content=text,
                url=value['link'],
                title=value['title']
            )

        chunks = get_chunks(value['text'])
        for chunk in chunks:
            with DB: Chunk.get_or_create(article=article, chunk=chunk)

if __name__ == '__main__':
    loader()