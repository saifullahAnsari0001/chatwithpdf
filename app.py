import time
import os
import asyncio
import streamlit as st
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_pinecone import PineconeEmbeddings
from pinecone.grpc import PineconeGRPC as Pinecone
from langchain_pinecone import PineconeVectorStore
from pinecone import Pinecone, ServerlessSpec
from langchain_cohere import ChatCohere
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from htmlTemplates import css, bot_template, user_template


load_dotenv()
# Initialize Pinecone and Cohere API keys
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
COHERE_API_KEY = os.getenv("COHERE_API_KEY")

# Fix for the event loop issue
def get_or_create_eventloop():
    try:
        return asyncio.get_event_loop()
    except RuntimeError as ex:
        if "There is no current event loop in thread" in str(ex):
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            return loop


# Asynchronous function to handle vector store setup
async def get_vector_store_async(text_chunks):
    model_name = 'multilingual-e5-large'
    embeddings = PineconeEmbeddings(
        model=model_name,
        pinecone_api_key=PINECONE_API_KEY
    )

    # Initialize Pinecone
    pc = Pinecone(api_key=PINECONE_API_KEY)

    index_name = "chat-with-pdf"
    if index_name not in pc.list_indexes().names():
        pc.create_index(
            name=index_name,
            dimension=embeddings.dimension,  # Replace with your model dimensions
            metric="cosine",  # Replace with your model metric
            spec=ServerlessSpec(cloud="aws", region="us-east-1")
        )
        # Wait for index to be ready
        while not pc.describe_index(index_name).status['ready']:
            time.sleep(1)

    # Set up the vector store with Pinecone
    namespace = "wondervector5000"
    vectorstore = PineconeVectorStore.from_texts(
        texts=text_chunks,
        index_name=index_name,
        embedding=embeddings,
        namespace=namespace
    )

    return vectorstore


def get_vectorstore(text_chunks):
    loop = get_or_create_eventloop()
    return loop.run_until_complete(get_vector_store_async(text_chunks))

def get_pdf_text(pdf_docs):
    text = ""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text


def get_text_chunks(text):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=10000, chunk_overlap=200)
    chunks = text_splitter.split_text(text)
    return chunks


def get_conversation_chain(vectorstore):
    # Define the Cohere LLM
    llm = ChatCohere(cohere_api_key=COHERE_API_KEY, model="command-r-plus-08-2024")

    memory = ConversationBufferMemory(
        memory_key='chat_history', return_messages=True)
    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vectorstore.as_retriever(),
        memory=memory
    )
    return conversation_chain


def handle_userinput(user_question):
    response = st.session_state.conversation({'question': user_question})
    st.session_state.chat_history = response['chat_history']

    for i, message in enumerate(st.session_state.chat_history):
        if i % 2 == 0:
            st.write(user_template.replace(
                "{{MSG}}", message.content), unsafe_allow_html=True)
        else:
            st.write(bot_template.replace(
                "{{MSG}}", message.content), unsafe_allow_html=True)


def main():
    load_dotenv()
    st.set_page_config(page_title="Chat with multiple PDFs",
                       page_icon=":books:")
    st.write(css, unsafe_allow_html=True)

    if "conversation" not in st.session_state:
        st.session_state.conversation = None
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = None

    st.header("Chat with multiple PDFs :books:")
    user_question = st.text_input("Ask a question about your documents:")
    if user_question:
        handle_userinput(user_question)

    with st.sidebar:
        st.subheader("Your documents")
        pdf_docs = st.file_uploader(
            "Upload your PDFs here and click on 'Process'", accept_multiple_files=True)
        if st.button("Process"):
            with st.spinner("Processing"):
                # get pdf text
                raw_text = get_pdf_text(pdf_docs)

                # get the text chunks
                text_chunks = get_text_chunks(raw_text)

                # create vector store
                vectorstore = get_vectorstore(text_chunks)

                # create conversation chain
                st.session_state.conversation = get_conversation_chain(
                    vectorstore)


if __name__ == '__main__':
    main()