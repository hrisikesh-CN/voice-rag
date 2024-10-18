import streamlit as st 
import statistics
from datetime import datetime
# from src.pipeline.docchat_pipeline import DocChatPipeline
from src.pipeline.qa_pipeline import QAPipeline

from src.utils.chatbot_utils import *
from langchain.chains import RetrievalQA
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="Chatbot", page_icon="💬")
st.header('🤖 The DocChat Bot')

time_now = datetime.now()


# st.markdown(DEFAULT_BOT_PAGE_DOC)


@chatbot
def form_bot(doc_chain):
    # if "uploaded_doc_name" in st.session_state.keys()
    if query := st.chat_input(placeholder="Ask anything about the document"):  # disabled=not (hf_email and hf_pass)):
        st.session_state.messages.append({"role": "user", "content": query})
        with st.chat_message("user"):
            st.markdown(query)

        if st.session_state.messages[-1]["role"] != "assistant":
            with st.spinner("Thinking..."):
                with st.chat_message("assistant"):
                    response = doc_chain.invoke(query)
                    st.markdown(response)
            response_message = {"role": "assistant", "content": response}
            st.session_state.messages.append(response_message)
    # with st.chat_message("assistant"):
    #
    #     response = doc_chain(user_query)
    #     st.session_state.messages.append({"role": "assistant", "content": response["result"]})


class ChatWithDocs:

    def __init__(self):
        self.chain = None
        self.uploaded_file = None

    def form_the_page(self):
        with st.sidebar:
            st.header("Upload Files")

            # Add a file uploader widget to the sidebar
            self.uploaded_file = st.file_uploader("Upload a file", type=["pdf", "csv", "zip"])

            # if st.session_state.message:
            #     st.session_state.message = DEFAULT_SESSION_MESSAGE

            if self.uploaded_file:
                st.session_state["uploaded_file_name"] = self.uploaded_file.name
            else:
                if "uploaded_file_name" in st.session_state.keys():
                    st.cache_resource.clear()

                    # Optionally, you can also reset the session state
                    st.session_state.messages.clear()

        if self.uploaded_file is not None:
            pipeline = QAPipeline(file=self.uploaded_file)
            pipeline.start_processing_documents() #ingest docs in vector stor
            
            

            self.chain = True
            return QAPipeline.get_doc_chain()


# Call the function to display the uploaded file content
if __name__ == "__main__":

    obj = ChatWithDocs()
    chain = obj.form_the_page()

    if "uploaded_file_name" in st.session_state.keys() and \
        obj.uploaded_file and \
            obj.uploaded_file.name == st.session_state.uploaded_file_name:
        print(time_now, "\n", obj.uploaded_file.name)

        if not chain:
            # del st.session_state["uploaded_file_name"]
            st.session_state["chain_formed"] = False


        else:

            st.session_state["chain_formed"] = True
            form_bot(chain)
    else:
        if "uploaded_file_name" not in st.session_state.keys():

            st.markdown(page_markdown_default)