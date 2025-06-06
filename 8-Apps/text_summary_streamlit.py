import streamlit as st
from langchain.chains.summarize import load_summarize_chain
from langchain_openai import ChatOpenAI
from langchain_community.docstore.document import Document
from langchain_text_splitters import CharacterTextSplitter

# Streamlit app
st.subheader('Summarize Text')

# Get OpenAI API key and source text input
with st.sidebar:
    openai_api_key = st.text_input("OpenAI API key", value="", type="password")
source_text = st.text_area("Source Text", label_visibility="collapsed", height=250)

# If the 'Summarize' button is clicked
if st.button("Summarize"):
    # Validate inputs
    if not openai_api_key.strip() or not source_text.strip():
        st.error(f"Please provide the missing fields.")
    else:
        try:
            with st.spinner('Please wait...'):
              # Split the source text
              text_splitter = CharacterTextSplitter()
              texts = text_splitter.split_text(source_text)

              # Create Document objects for the texts (max 3 pages)
              docs = [Document(page_content=t) for t in texts[:3]]

              # Initialize the OpenAI module, load and run the summarize chain
              llm = ChatOpenAI(temperature=0, openai_api_key=openai_api_key)
              chain = load_summarize_chain(llm, chain_type="map_reduce")
              summary = chain.run(docs)

              st.success(summary)
        except Exception as e:
            st.exception(f"An error occurred: {e}")