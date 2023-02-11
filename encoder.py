import torch
from transformers import AutoTokenizer, AutoModel

model_path = 'sentence-transformers/paraphrase-MiniLM-L3-v2'
tokenizer = AutoTokenizer.from_pretrained(model_path)
model = AutoModel.from_pretrained(model_path)


# Following function is taken from huggingface's documentation on how to use the model
#Mean Pooling - Take attention mask into account for correct averaging
def mean_pooling(model_output, attention_mask):
    token_embeddings = model_output[0] #First element of model_output contains all token embeddings
    input_mask_expanded = attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()
    return torch.sum(token_embeddings * input_mask_expanded, 1) / torch.clamp(input_mask_expanded.sum(1), min=1e-9)

def encode(list_of_text: list[str]) -> torch.Tensor:
    """
    Encode a list of text into a tensor of embeddings
    """
    encoded_input = tokenizer(list_of_text, padding=True, truncation=False, max_length=128, return_tensors='pt')
    assert encoded_input['input_ids'].size(1) <= 128, 'Input length is greater 128'
    with torch.no_grad():
        model_output = model(**encoded_input)
    sentence_embeddings = mean_pooling(model_output, encoded_input['attention_mask'])
    return sentence_embeddings