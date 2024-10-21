# a decorator to handle streamlit chatbot ui
import streamlit as st
from streamlit.runtime.uploaded_file_manager import UploadedFile


def chatbot(func):
    # Initialize chat messages if not present in session state
    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "assistant",
                                      "content": "I am ready to use. Ask anything about the document."}]

    # Display chat messages in sequence (preserve history)
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Call the decorated function
    def execute(*args, **kwargs):
        func(*args, **kwargs)

    return execute



page_markdown_default = """
📁 **Welcome to the Chat with Docs App!** 📁

Before we dive into processing your documents, let's make sure you're all set up. We've designed this app to make your document management a breeze. Here's how it works:

1. **Upload Your Document** 📤
   - In the sidebar on the left, you'll find an option to upload your documents. You can select PDFs, CSV files, or ZIP archives.

2. **Processing Starts After Upload** ⏳
   - As soon as you upload your document, our app will begin processing it. This may take a moment, depending on the size and complexity of your file.

3. **Chat Window Activation** 💬
   - Once the document processing is complete, the chat window will open, and you can interact with our chatbot for any questions or assistance.

4. **Real-time Assistance** 🤖
   - Feel free to ask the chatbot any questions you have about your processed document or anything else you need help with.

This streamlined process ensures that your experience is efficient and seamless. So, go ahead and upload your document to get started! We're here to assist you. 😊👍
"""

DEFAULT_SESSION_MESSAGE = [{"role": "assistant",
                            "content": "I am ready to use. Ask anything about the document."}]


def set_no_of_uploaded_file_in_session(uploaded_file:UploadedFile):
    if "uploaded_file_name" in st.session_state.keys():
        if uploaded_file.name != st.session_state["uploaded_file_name"]:

            if "no_of_file_uploads" not in st.session_state.keys():
                st.session_state.no_of_file_uploads = [{"files": 1}]

            else:
                no_of_total_uploaded_files = st.session_state.no_of_file_uploads[-1]["files"]

                st.session_state.no_of_file_uploads.append(
                    {"files": no_of_total_uploaded_files + 1}
                )