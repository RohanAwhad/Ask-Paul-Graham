import json
from functools import cache
from loguru import logger

import data_transformer
import encoder
import qa

# load data
with open('data/raw.json') as f:
    data = json.load(f)
logger.info('Data loaded')


# Getting chunks from all articles
chunk_to_uid = dict()  # {uid: [chunk1, chunk2, ...]}
try:
    for uid, article in data.items():
        chunks = data_transformer.get_chunks(text=article['text'], max_len_chars = 360)
        for chunk in chunks:
            chunk_to_uid[chunk] = uid
except Exception as e:
    logger.exception(e)
logger.info('Chunks extracted')


chunk_list = list(chunk_to_uid.keys())
idx_2_chunk = dict((i, chunk) for i, chunk in enumerate(chunk_list))  # {idx: chunk}
chunk_to_idx = dict((chunk, i) for i, chunk in idx_2_chunk.items())  # {chunk: idx}

chunk_embeddings = encoder.encode(chunk_list)
logger.info('Embeddings calculated for chunks')
index = encoder.build_index(chunk_embeddings)
logger.info('Chunk index built')

# Querying
@cache
def run(question):
    question_emb = encoder.encode(question)
    k = 3
    _, idx_mat = index.search(question_emb, k)
    documents = [idx_2_chunk[idx] for idx in idx_mat[0]]
    return qa.get_answer(question, documents)
