# Ask Paul Graham

This is a fun implementation of long form qa on Paul Graham's essays.

## Retrieving

There are multiple steps in retrieving. 
1. Extracting the essays from the website
2. Encoding the essays
3. Indexing the essays
4. Encoding the question
5. And finally retrieving the essays based on dot product of the question and the essays embeddings


## Retriever 
For Retriever currently I am using MiniLM-L3 model from HuggingFace.


### Todos:
[ ] Scrape essays from paulgraham.com
[ ] Save them in a DB
[ ] Transform text into a vector space
[ ] Save the vector space in a Faiss index
[ ] Build a retriever to take a question and return the top 5 essays
[ ] Build a model to answer the question in an abstractive fashion based on the retrieved essays
[ ] Build a web app to take a question and return the answer