import sys

from langchain import hub
from langchain_core.embeddings import Embeddings
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_pinecone import PineconeVectorStore
from langchain.prompts import PromptTemplate

from src.constant import PINECONE_INDEX_NAME
from src.exception import CustomException
from src.logger import get_logger
from src.vector_db_connection import VectorStore


class QAFormatter:
    def __init__(self, llm):
        """
        Initialize a QAFormatter instance.
    
        This class is responsible for formatting and answering questions using a Retrieval Augmented Generation (RAG) approach.
        It retrieves relevant documents from a vector store based on the input embeddings, formats the documents, and uses a language model to answer questions.
    
        Parameters:
        llm (LLM): The language model to be used for question answering.
    
        Attributes:
        llm (LLM): The language model to be used for question answering.
        logger (Logger): The logger instance for logging errors and information.
        """
        self.llm = llm
        self.logger = get_logger(__name__)

    def get_vector_store(self, embeddings: Embeddings) -> PineconeVectorStore:
        """
        Retrieves a vector store instance using the provided embeddings.

        This method attempts to create a VectorStore instance using the specified embeddings.
        If an error occurs during the process, it logs the error and raises a CustomException.

        Parameters:
        embeddings (Embeddings): The embeddings to be used for vector store creation.

        Returns:
        VectorStore: The created vector store instance.

        Raises:
        CustomException: If an error occurs during the process.
        """
        try:
            vector_store = VectorStore(PINECONE_INDEX_NAME)
            return vector_store.get_vectorstore(embeddings=embeddings)
        except Exception as e:
            raise CustomException(e, sys)

    def form_qa_chain(self, embeddings: Embeddings) -> RunnablePassthrough:
        """
        This function forms a QA chain using a Retrieval Augmented Generation (RAG) approach.
        It retrieves relevant documents from a vector store based on the input embeddings,
        formats the documents, and uses a language model to answer questions.
    
        Parameters:
        embeddings (Embeddings): The embeddings to be used for document retrieval.
    
        Returns:
        RunnablePassthrough: The final QA chain, which can be used to answer questions.
    
        Raises:
        CustomException: If an error occurs during the process.
        """
        try:
            vector_store = self.get_vector_store(embeddings)
            retriever = vector_store.as_retriever(search_type="mmr")

            # prompt = hub.pull("rlm/rag-prompt")
            # print(prompt)

            template = """
            You are an assistant for question-answering tasks. 
            The information in the context might be scattered or unstructured. 
            Reorganize the context as needed to provide a clear and direct answer to the question. 
            If the necessary information is not available, say that you don't know. 
            Focus on accuracy and do not summarize unnecessarily.

            Question: {question}

            Context: {context}

            Answer:
            """

            # Create a LangChain PromptTemplate
            prompt = PromptTemplate(
                input_variables=["question", "context"],
                template=template
            )
            
            
            def format_docs(docs):
                """
                Helper function to format retrieved documents.
    
                Parameters:
                docs (List[Document]): The retrieved documents.
    
                Returns:
                str: The formatted documents, separated by newlines.
                """
                return "\n\n".join(doc.page_content for doc in docs)

            rag_chain = (
                    {"context": retriever | format_docs, "question": RunnablePassthrough()}
                    | prompt
                    | self.llm
                    | StrOutputParser()
            )
            return rag_chain

        except Exception as e:
            raise CustomException(e, sys)
