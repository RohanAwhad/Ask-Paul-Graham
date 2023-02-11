import streamlit as st
import main
from loguru import logger
logger.add("app.log", format="{time} {level} {message}", level="INFO", rotation="10 MB")

st.title("Ask Paul Graham")
# subtitle
st.write("This is an AI agent trained to answer questions in a generative fashion based on Paul Graham's essays. Ask away!")

# text input
question = st.text_input("Ask a question")

# button
if st.button("Ask"):
    # generate answer
    answer = main.run(question)
    # display answer in a text box
    st.text_area("Answer", answer)