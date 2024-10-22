import os, sys

from langchain_core.embeddings import Embeddings
from langchain_openai import OpenAIEmbeddings

from src.constant import PINECONE_INDEX_NAME
from src.entity.artifact_entity import DataTransformationArtifact
from src.logger import get_logger
from src.exception import CustomException
from src.vector_db_connection import VectorStore


class VectorIngestion:
    def __init__(self,
                 data_transformation_artifacts: list[DataTransformationArtifact]):
        self.data_transformation_artifact = data_transformation_artifacts
        self.logger = get_logger(__name__)
        self.vector_store = VectorStore(pinecone_index_name=PINECONE_INDEX_NAME,

                                        )

    def ingest_data_to_vectordb(self,
                                embeddings: Embeddings,
                                ):
        try:
            
            for artifact in self.data_transformation_artifact:
                
                self.vector_store.upload_document(
                    embeddings=embeddings,
                    documents=artifact.documents
                )

                self.logger.info(f"Data ingested successfully to Pinecone index: {PINECONE_INDEX_NAME}")

        except Exception as e:
            raise CustomException(e, sys)
