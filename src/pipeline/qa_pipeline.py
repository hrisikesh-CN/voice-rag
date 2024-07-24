import os, sys

from langchain_openai import OpenAIEmbeddings, ChatOpenAI

from src.components.data_transformation import DataTransformation
from src.components.vector_ingestion import VectorIngestion
from src.entity.artifact_entity import FileHandlerArtifact, DataTransformationArtifact
from src.entity.config_entity import FileHandlerConfig, DataTransformationConfig
from src.components.data_ingestion import DataIngestion
from src.components.qa_chain_formation import QAFormatter
from src.logger import get_logger
from src.exception import CustomException
from src.constant import PINECONE_INDEX_NAME


class QAPipeline:
    embedding_function = OpenAIEmbeddings()

    def __init__(self, files: list) -> None:
        self.files = files
        self.logger = get_logger(__name__)

    def start_data_ingestion(self):
        """This method is initiates the data ingestion process and
        returns the file handler artifact with the file storage dir path.

    
        Returns:
            FileHandlerArtifact: path of the file storage directory
        """
        try:
            data_ingestion = DataIngestion(FileHandlerConfig())
            file_handler_artifact = data_ingestion.ingest(self.files)
            return file_handler_artifact
        except Exception as e:
            raise CustomException(e, sys)

    @staticmethod
    def start_data_transformation(file_handler_artifact: FileHandlerArtifact):
        """This method initiates the data transformation process and
        returns the data transformation artifact with the split documents.

        Returns:
            DataTransformationArtifact: split documents
        """
        try:
            data_transformation = DataTransformation(file_handler_artifact, DataTransformationConfig())
            data_transformation_artifact = data_transformation.transform_data()
            return data_transformation_artifact
        except Exception as e:
            raise CustomException(e, sys)

    def start_vector_ingestion(self,
                               data_transformation_artifact: DataTransformationArtifact):
        """This method initiates the vector ingestion process and
        returns the vector store with the uploaded documents.

        Returns:
            VectorStore: uploaded documents
        """
        try:
            vector_ingestion = VectorIngestion(data_transformation_artifact)
            vector_ingestion.ingest_data_to_vectordb(embeddings=self.embedding_function)

        except Exception as e:
            raise CustomException(e, sys)

    def start_processing_documents(self):
        """This method initiates the entire pipeline by calling the
        respective methods in the order of data ingestion, transformation,
        and vector ingestion.
        """
        try:
            file_handler_artifact = self.start_data_ingestion()
            data_transformation_artifact = self.start_data_transformation(file_handler_artifact)
            self.start_vector_ingestion(data_transformation_artifact)

            self.logger.info("Document Processing Completed.")

        except Exception as e:
            raise CustomException(e, sys)

    @staticmethod
    def start_qa(question):
        try:
            qa_formatter = QAFormatter(
                llm=ChatOpenAI(model="gpt-3.5-turbo-0125")

            )

            rag_chain = qa_formatter.form_qa_chain(embeddings=QAPipeline.embedding_function)
            return rag_chain.invoke(question)

        except Exception as e:
            raise CustomException(e, sys)
