import os, sys

from langchain_text_splitters import RecursiveCharacterTextSplitter

from src.components.data_ingestion import DataIngestion
from src.components.data_transformation import DataTransformation
from src.entity.config_entity import DataTransformationConfig, FileHandlerConfig
from src.entity.artifact_entity import FileHandlerArtifact, DataTransformationArtifact
from src.logger import get_logger
from src.components.summarizer import Summarizer
from src.file_readers import ReadFiles
from src.exception import CustomException


class SummarizationPipeline:

    def __init__(self,files):
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
            data_transformation_artifact = data_transformation.transform_data(return_file_names=True)
            return data_transformation_artifact
        except Exception as e:
            raise CustomException(e, sys)

    def start_summmarization(self):
        try:
            file_handler_artifact = self.start_data_ingestion()
            data_transformation_artifact = self.start_data_transformation(file_handler_artifact)
            summarizer = Summarizer(data_transformation_artifact)
            summaries = summarizer.summarize()
            
            formed_summaries = {}
            for file_name in summaries:
                file_summary = summaries[file_name]["output_text"]
                formed_summaries[file_name] = file_summary
                
            return formed_summaries
                
        except Exception as e:
            raise CustomException(e, sys)