import sys 
import streamlit as st 
from datetime import datetime
from src.constant import ARTIFACT_DIR
from src.pipeline.qa_pipeline import QAPipeline
from src.utils.chatbot_utils import *
from src.utils import delete_folder
from dotenv import load_dotenv
from src.exception import CustomException


st.header("💬 Chat with DocChat Bot")
@chatbot
def form_bot(doc_chain):
    try:
        # Input query from user
        if query := st.chat_input(placeholder="Ask anything about the document"):
            # Append user query to session state messages
            st.session_state.messages.append({"role": "user", "content": query})
            with st.chat_message("user"):
                st.markdown(query)

            # Process query and append assistant's response
            with st.spinner("Thinking..."):
                response = doc_chain.invoke(query)  # Process the query

                # Append assistant's response to session state messages
                st.session_state.messages.append({"role": "assistant", "content": response})
                with st.chat_message("assistant"):
                    st.markdown(response)
    except Exception as e:
        raise CustomException(e, sys)


def load_chat():

    # Check if a file has been uploaded and processed
    doc_chain = QAPipeline.get_doc_chain()  # Create the doc chain only when chatting

    # Call the chatbot to interact with the user
    form_bot(doc_chain)
    
    
if __name__=='__main__':
    # st.markdown("# 💬 Chat with DocChat Bot")
    load_chat()