import os, sys
import time

from langchain_core.documents import Document
from langchain_core.embeddings import Embeddings

from src.logger import get_logger
from src.exception import CustomException
from langchain_pinecone import PineconeVectorStore
from langchain.indexes import SQLRecordManager, index
from pinecone import Pinecone, ServerlessSpec


class VectorStore:
    def __init__(self,
                 pinecone_index_name: str):
        self.pinecone_index_name = pinecone_index_name

        self.logger = get_logger(__name__)
        try:
            self.pinecone_api_key = os.getenv('PINECONE_API_KEY')

        except KeyError:
            raise CustomException('PINECONE_API_KEY environment variable not found.')

        self.pinecone_connection = Pinecone(api_key=self.pinecone_api_key)

    def create_index(self):
        try:
            existing_indexes = [index_info["name"] for index_info in self.pinecone_connection.list_indexes()]

            if self.pinecone_index_name not in existing_indexes:
                self.pinecone_connection.create_index(
                    name=self.pinecone_index_name,
                    dimension=1536,
                    metric="cosine",
                    spec=ServerlessSpec(cloud="aws", region="us-east-1"),
                )
                while not self.pinecone_connection.describe_index(self.pinecone_index_name).status["ready"]:
                    time.sleep(1)

            pinecone_index = self.pinecone_connection.Index(self.pinecone_index_name)
            return pinecone_index

        except Exception as e:
            raise CustomException(e, sys)

    @staticmethod
    def upload_docs_to_pinecone(docs: list,
                                record_manager=None,
                                vectorstore=None):
        try:
            # Upload documents to pinecome
            index(docs, record_manager, vectorstore,
                  cleanup="incremental", source_id_key="source")

        except Exception as e:
            raise CustomException(e, sys)

    def get_vectorstore(self, embeddings: Embeddings,
                        namespace: str=None) -> PineconeVectorStore:
        """
        This function creates a PineconeVectorStore instance using the provided embeddings and namespace.

        Parameters:
        - embeddings (Embeddings): The embeddings to be used for vectorizing the documents.
        - namespace (str): The namespace for the vector store.

        Returns:
        - PineconeVectorStore: An instance of PineconeVectorStore with the given embeddings and namespace.

        Raises:
        - CustomException: If an error occurs while creating the vector store.
        """
        try:
            # Create a Pinecone vector store with the given embeddings and namespace
            pinecone_index = self.create_index()
            pinecone_vector_store = PineconeVectorStore(pinecone_index,
                                                        embeddings,
                                                        namespace=namespace)
            return pinecone_vector_store

        except Exception as e:
            raise CustomException(e, sys)

    def upload_document(self, embeddings: Embeddings,
                        documents: list[list[Document]],
                        namespace: str = None):
        try:
            pinecone_vector_store = self.get_vectorstore(embeddings,
                                                         namespace=namespace)

            if not namespace:
                namespace = f"pinecone/{self.pinecone_index_name}"
                
            record_manager = SQLRecordManager(
                namespace, db_url="sqlite:///record_manager_cache.sql"
            )

            record_manager.create_schema()

            # upload docs
            
            self.upload_docs_to_pinecone(docs=documents,
                                             record_manager=record_manager,
                                             vectorstore=pinecone_vector_store)
                
                

            self.logger.info(f"Documents uploaded successfully to Pinecone index: {self.pinecone_index_name}")

        except Exception as e:
            raise CustomException(e, sys)
