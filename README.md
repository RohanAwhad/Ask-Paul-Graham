# Ask Paul Graham

This is a fun implementation of long form qa on Paul Graham's essays.

## Data

- Have raw data in `data/raw.json()` currently.
- Data will be loaded in sqlite essay_db, text will be chunked in  and then indexed in Faiss.

## Retrieving

There are multiple steps in retrieving. 
1. Extracting the essays from the website
2. Encoding the essays
3. Indexing the essays
4. Encoding the question
5. And finally retrieving the essays based on dot product of the question and the essays embeddings

### Todos:
[x] Scrape essays from paulgraham.com
[ ] Filter to not req page that is already in the db
[ ] Save them in a DB
[x] Transform text into a vector space
[x] Save the vector space in a Faiss index
[x] Build a retriever to take a question and return the top 5 essays
[x] Build a model to answer the question in an abstractive fashion based on the retrieved essays
[x] Build a web app to take a question and return the answer
[ ] Persist the chunks on disk
[ ] Persist the index on disk
[ ] Based on the distances between the question and chunks retrieved, eliminate chunks that are too far away and return an answer: "I don't know about that"