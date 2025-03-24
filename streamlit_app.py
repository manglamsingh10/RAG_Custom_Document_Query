import os
import streamlit as st
import streamlit.components.v1 as components
from dotenv import load_dotenv
from rag import index_folder_and_store_embeddings
from rag import clear_indexes
from dataoperation.hdbclinet import check_if_documents_exist
import time


def is_valid_path(folder_path):
    if os.path.isdir(folder_path):
        return True
    else:
        return False


# Function to index the content of the folder
def index_folder(folder_path):
    if is_valid_path(folder_path):
        st.write(f"Indexing folder: {folder_path}")
        index_folder_and_store_embeddings(folder_path)
        st.write(f"Folder: {folder_path} indexed successfully.")
        return "Indexing completed."
    else:
        return "Indexing failed due to invalid path."


# Function to clear indexes
def clear_all_indexes():
    clear_indexes()


# Streamlit UI
st.title("Document Indexing and Query Interface")

# Sidebar for user input
with st.sidebar:
    # Input for folder path
    folder_path = st.text_input("Enter the path of the folder to be indexed:")
    st.markdown("<small>This will index all the PDF files in the given directory and its subdirectories.</small>",
                unsafe_allow_html=True)

    # Submit button for indexing
    if st.button("Submit"):
        success = False
        with st.spinner("Indexing in progress..."):
            if folder_path:
                if is_valid_path(folder_path):
                    index_message = index_folder(folder_path)
                    st.session_state.indexing_completed = True
                    success = True
                else:
                    success = False
                    index_message = "The entered path is not a valid directory. Please enter a valid folder path."
            else:
                success = False
                index_message = "Please enter a valid folder path."
        message_placeholder = st.empty()
        if success:
            message_placeholder.success(index_message)
        else:
            message_placeholder.error(index_message)
        time.sleep(5)
        message_placeholder.empty()

    # Button to clear indexes
    if st.button("Clear Indexes"):
        with st.spinner("Indexing cleaning in progress..."):
            clear_all_indexes()
        message_placeholder = st.empty()
        message_placeholder.success("Indexes cleared successfully.")
        time.sleep(5)
        message_placeholder.empty()

# Main content for chat interface
try:
    if check_if_documents_exist() or st.session_state.indexing_completed:
        print("Documents are indexed. Loading gradio chat interface.")
        load_dotenv()
        gradio_app_url = f"{os.getenv('GRADIO_APP_HOST')}:{os.getenv('GRADIO_APP_PORT')}"
        components.iframe(gradio_app_url, width=1200, height=600)
        print("Gradio app loaded in iframe successfully.")
    else:
        print("Documents are not indexed. Please index the folder documents to enable the chat interface.")
        st.write("Index the folder documents to enable the chat interface.")
except Exception as e:
    print(f"Error launching Gradio app: {e}")
