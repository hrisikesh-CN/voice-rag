import os, sys

from langchain_text_splitters import RecursiveCharacterTextSplitter

from src.entity.config_entity import DataTransformationConfig
from src.entity.artifact_entity import FileHandlerArtifact, DataTransformationArtifact
from src.logger import get_logger
from src.file_readers import ReadFiles
from src.exception import CustomException


class DataTransformation:
    def __init__(self,
                 file_handler_artifact: FileHandlerArtifact,
                 data_transformation_config: DataTransformationConfig):

        self.data_transformation_config = data_transformation_config
        self.file_handler_artifact = file_handler_artifact

        self.reader = ReadFiles(file_handler_artifact,
                                self.get_splitter())
        self.logger = get_logger(__name__)

    @staticmethod
    def get_splitter(chunk_size: int = 1000,
                     chunk_overlap: int = 200) -> RecursiveCharacterTextSplitter:
        try:
            # get splitter as per the configuration
            return RecursiveCharacterTextSplitter(chunk_size=chunk_size,
                                                  chunk_overlap=chunk_overlap,
                                                  separators=["\n\n", "\n", " ", ""])
        except Exception as e:
            raise CustomException(e, sys)

    def transform_data(self, return_file_names=False):
        try:
            if not return_file_names:
                documents = self.reader.read_all_files()  # getting all the splitted documents
            else:
                documents = self.reader.read_files_with_filenames()
            self.logger.info(f"Data transformation completed successfully.")

            return DataTransformationArtifact(documents=documents)

        except Exception as e:
            raise CustomException(e, sys)
