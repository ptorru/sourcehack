import streamlit as st
from main import main


st.title("SourceHack")

## Get a link from the user
link = st.text_input("Enter a link to a news article")

if st.button("Get Article"):
    article = main(link)
    if article == "Could not find the article":
        st.write("Could not find the article")
    else:
        st.write(article)
