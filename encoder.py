import faiss
import numpy as np
import time
import torch

from loguru import logger
from tqdm import tqdm
from transformers import AutoTokenizer, AutoModel
from typing import Union

model_path = 'sentence-transformers/paraphrase-MiniLM-L3-v2'
tokenizer = AutoTokenizer.from_pretrained(model_path)
model = AutoModel.from_pretrained(model_path)
model.eval()
batch_size = 8


# Following function is taken from huggingface's documentation on how to use the model
#Mean Pooling - Take attention mask into account for correct averaging
def mean_pooling(model_output, attention_mask):
    token_embeddings = model_output[0] #First element of model_output contains all token embeddings
    input_mask_expanded = attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()
    return torch.sum(token_embeddings * input_mask_expanded, 1) / torch.clamp(input_mask_expanded.sum(1), min=1e-9)

def _encode(text):
    encoded_input = tokenizer(text, padding=True, truncation=False, max_length=128, return_tensors='pt')
    with torch.no_grad(): model_output = model(**encoded_input)
    return mean_pooling(model_output, encoded_input['attention_mask'])

def _encode_batch(list_of_text: list[str]) -> torch.Tensor:
    ret = []
    logger.info(f"Encoding {len(list_of_text)} sentences")
    start = time.monotonic()
    for i in tqdm(range(0, len(list_of_text), batch_size), total=len(list_of_text)//batch_size, leave=False):
        ret.append(_encode(list_of_text[i:i+batch_size]))

    logger.info(f"Encoding took {time.monotonic() - start:.2f} seconds")
    return torch.cat(ret, dim=0).detach().cpu()

def encode(text: Union[str, list[str]]) -> torch.Tensor:
    """
    Encode a list of text into a tensor of embeddings
    """
    if isinstance(text, str): return _encode(text)
    else: return _encode_batch(text)

def build_index(chunk_embeddings: np.ndarray):
    """Index embeddings using Faiss.

    Args:
        chunk_embeddings (np.ndarray): Embeddings to index.

    Returns:
        index (faiss.IndexFlatIP): Index of embeddings.
    """
    dim_size = chunk_embeddings.shape[1]
    index = faiss.IndexFlatIP(dim_size)  # build the index
    index.add(chunk_embeddings)  # add vectors to the index
    return index