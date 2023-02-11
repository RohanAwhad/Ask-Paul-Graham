# chunk text in each article present in data
from loguru import logger
from nltk.tokenize import sent_tokenize

def get_chunks(text, max_len_chars = 1800):
    assert len(text) > 0, 'Text is empty'
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
    chunks = [c for c in chunks if len(c) > 0 and isinstance(c, str)]

    logger.info(f'Created {len(chunks)} chunks')
    return chunks