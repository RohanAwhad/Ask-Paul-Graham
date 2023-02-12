import faiss
import json
import numpy as np
import os
import pandas as pd

from functools import cache
from loguru import logger

import data_transformer
import encoder
import qa

# constants
RAW_DATA_PATH = 'data/raw.json'
CHUNKS_PATH = 'data/chunks.parquet'
CHUNK_EMBEDDINGS_PATH = 'data/chunk_embeddings.npy'
CHUNK_INDEX_PATH = 'data/chunk_index.faiss'

# load data
with open(RAW_DATA_PATH, 'r') as f:
    data = json.load(f)
logger.info('Data loaded')


if os.path.exists(CHUNKS_PATH):
    chunks_df = pd.read_parquet(CHUNKS_PATH)
    logger.info('Chunks loaded')
else:
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

    chunks_df = pd.DataFrame.from_dict(chunk_to_uid, orient='index').reset_index()
    chunks_df.columns = ['chunk', 'uid']
    chunks_df.index.name = 'chunk_id'
    chunks_df.to_parquet(CHUNKS_PATH)
    logger.info('Chunks saved')


if os.path.exists(CHUNK_EMBEDDINGS_PATH):
    chunk_embeddings = np.load(CHUNK_EMBEDDINGS_PATH)
    logger.info('Chunk embeddings loaded')
else:
    chunk_list = chunks_df['chunk'].tolist()
    chunk_embeddings = encoder.encode(chunk_list)
    logger.info('Embeddings calculated for chunks')
    np.save(CHUNK_EMBEDDINGS_PATH, chunk_embeddings.numpy())
    logger.info('Chunk embeddings saved')



if os.path.exists(CHUNK_INDEX_PATH):
    index = faiss.read_index(CHUNK_INDEX_PATH)
    logger.info('Chunk index loaded')
else:
    index = encoder.build_index(chunk_embeddings)
    logger.info('Chunk index built')
    faiss.write_index(index, CHUNK_INDEX_PATH)


# Querying
@cache
def run(question):
    question_emb = encoder.encode(question)
    k = 8
    _, idx_mat = index.search(question_emb, k)
    documents = [chunks_df.loc[idx, 'chunk'] for idx in idx_mat[0]]
    return qa.get_answer(question, documents)
