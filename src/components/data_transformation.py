import os, sys

from langchain_text_splitters import RecursiveCharacterTextSplitter

from src.entity.config_entity import DataTransformationConfig
from src.entity.artifact_entity import FileHandlerArtifact, DataTransformationArtifact
from src.logger import get_logger

from langchain_community.document_loaders import PyPDFLoader
from src.exception import CustomException


class DataTransformation:
    def __init__(self,
                 file_handler_artifact: FileHandlerArtifact,
                 data_transformation_config: DataTransformationConfig):

        self.data_transformation_config = data_transformation_config
        self.file_handler_artifact = file_handler_artifact

       
        
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

    def transform_data(self)->list[DataTransformationArtifact]:
        try:
            data_transformation_artifacts = [] 
            for file in os.listdir(self.file_handler_artifact.file_storage_dir):
                file_full_path = os.path.join(self.file_handler_artifact.file_storage_dir,
                                              file)
                documents = PyPDFLoader(file_full_path)
                documents = documents.load()
                
                # Splitting the documents
                splitter = self.get_splitter()
                documents = splitter.split_documents(documents)
                    
            
                                
                
                
                
                
                 # getting all the splitted documents
                artifact = DataTransformationArtifact(documents=documents)
                
                data_transformation_artifacts.append(artifact)
                
            return data_transformation_artifacts

        except Exception as e:
            raise CustomException(e, sys)
