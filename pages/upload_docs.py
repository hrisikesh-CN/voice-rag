import os
import sys 
import streamlit as st 
from datetime import datetime
from src.constant import ARTIFACT_DIR
from src.pipeline.qa_pipeline import QAPipeline
from src.utils.chatbot_utils import *
from src.utils import delete_folder
from dotenv import load_dotenv
from src.exception import CustomException

# Load environment variables
load_dotenv()

# Set page configurations
st.set_page_config(page_title="DocChat Bot", page_icon="🤖")

# Sidebar Navigation
st.sidebar.title("Navigation")
app_mode = st.sidebar.selectbox("Choose the mode", ["Upload Files", "Chat"])

# Initialize current time for logging purposes
time_now = datetime.now()

# Ensure session state has a messages list initialized
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "I am ready to use. Ask anything about the document."}]

# Function to handle file upload and document processing
def upload_files():
    st.header("📁 Upload Your Documents")

    # File uploader
    uploaded_files = st.file_uploader("Upload a file", type=["pdf", "csv", "zip"],
                                     accept_multiple_files=True)
    
    for uploaded_file in uploaded_files:

        if uploaded_file:
            if os.path.exists(ARTIFACT_DIR):
                # Delete the existing artifact folder to save space
                delete_folder(ARTIFACT_DIR)

            # Store the uploaded file name in session state
            st.session_state["uploaded_file_name"] = uploaded_file.name

            # Initialize the pipeline and process the uploaded document
            pipeline = QAPipeline(file=uploaded_file)
            pipeline.start_processing_documents()  # Ingest docs into vector store

            st.success(f"{uploaded_file.name} uploaded and processed successfully!")

            # Clear previous messages when a new file is uploaded
            st.session_state.messages = [{"role": "assistant",
                                        "content": "I am ready to use. Ask anything about the document."}]
        else:
            st.info("Please upload a file.")
        
        
if __name__ == "__main__":
    upload_files()
