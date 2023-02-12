import torch

from loguru import logger
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

model_name = 'vblagoje/bart_lfqa'
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
model.eval()


def get_answer(question: str, documents: list[str]) -> str:
    logger.info(f'Generating answer for question: {question}')
    logger.info(f'Using documents: {documents}')
    conditioned_doc = "<P> " + " <P> ".join(documents)
    question_and_doc = f'question: {question} context: {conditioned_doc}'
    model_input = tokenizer(question_and_doc, return_tensors='pt', truncation=True)
    with torch.no_grad():
        model_output = model.generate(input_ids=model_input["input_ids"],
                                            attention_mask=model_input["attention_mask"],
                                            min_length=64,
                                            max_length=256,
                                            do_sample=True, 
                                            early_stopping=True,
                                            num_beams=3,
                                            temperature=0.9,
                                            top_k=30,
                                            top_p=0.92,
                                            eos_token_id=tokenizer.eos_token_id,
                                            no_repeat_ngram_size=3,
                                            num_return_sequences=1)

    answer = tokenizer.decode(model_output[0], skip_special_tokens=True, clean_up_tokenization_spaces=True)
    logger.info(f'Answer: {answer}')
    return answer