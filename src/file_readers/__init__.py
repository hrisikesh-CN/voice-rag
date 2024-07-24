import mimetypes
import os, sys
from typing import List

from langchain_text_splitters import TextSplitter

from src.utils.convert_docx import convert_docx_to_pdf
from src.entity.artifact_entity import FileHandlerArtifact
from src.logger import get_logger
from src.exception import CustomException
from dataclasses import dataclass
from .readers import Readers


@dataclass
class FileDetails:
    file_name: str
    file_full_path: str
    file_type: str


class ReadFiles(Readers):
    def __init__(self, file_handler_artifact: FileHandlerArtifact,
                 text_splitter: TextSplitter):
        self.file_handler_artifact = file_handler_artifact
        self.logger = get_logger(__name__)
        self.text_splitter = text_splitter
        super(ReadFiles, self).__init__()

    def get_file_reader(self, file_type):
        try:
            # map readers as per the file type
            read_functions = {
                'PDF': self.read_pdf_pypdf,
                'PPT': self.read_ppt,
                'PPTX': self.read_ppt,
                'DOCX': self.read_docx,
                'PNG': self.read_with_aws,
                'JPG': self.read_with_aws,
                'XLS': self.read_excel,
                'XLSX': self.read_excel,
                'CSV': self.read_csv,
                'MD': self.read_markdown,
                'HTML': self.read_html,
                'TXT': self.read_txt
            }

            # Get the reader function for the specified file type
            reader_function = read_functions.get(file_type)

            if reader_function:
                return reader_function
            else:
                raise ValueError(f"Unsupported file type: {file_type}")
        except Exception as e:
            raise CustomException(e, sys)

    @staticmethod
    def check_file_type(file_path):
        # Define the allowed file types
        allowed_file_types = {
            'application/pdf': 'PDF',
            'application/vnd.ms-powerpoint': 'PPT',
            'application/vnd.openxmlformats-officedocument.presentationml.presentation': 'PPTX',
            'application/msword': 'DOC',
            'application/vnd.openxmlformats-officedocument.wordprocessingml.document': 'DOCX',
            'image/png': 'PNG',
            'image/jpeg': 'JPG',
            'application/vnd.ms-excel': 'XLS',
            'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet': 'XLSX',
            'text/csv': 'CSV',
            'text/markdown': 'MD',
            'text/html': 'HTML',
            'text/plain': "TXT"
        }

        # Get the MIME type of the file
        mime_type, _ = mimetypes.guess_type(file_path)

        # Check if the MIME type is in the allowed file types
        if mime_type in allowed_file_types:
            return allowed_file_types[mime_type]
        else:
            return None

    def get_file_names_and_types(self) -> List[FileDetails]:
        """
        This function retrieves the names, full paths, and types of all files in the specified directory.

        Parameters:
        self (ReadFiles): The instance of the class.

        Returns:
        List[FileDetails]: A list of FileDetails objects, each containing the file name, full path, and type.

        Raises:
        CustomException: If an error occurs during the file retrieval process.
        """
        try:
            file_details = []
            for file in os.listdir(self.file_handler_artifact.file_storage_dir):
                file_full_path = os.path.join(self.file_handler_artifact.file_storage_dir,
                                              file)
                if os.path.isfile(file_full_path):
                    file_details.append(FileDetails(
                        file_name=file,
                        file_full_path=file_full_path,
                        file_type=ReadFiles.check_file_type(file_full_path)
                    ))

            return file_details
        except Exception as e:
            raise CustomException(e, sys)

    def read_all_files(self):
        """
           This function reads all files in the specified directory, splits them into smaller documents using the provided text splitter,
           and returns a dictionary containing the file names as keys and the splitted documents as values.

           Parameters:
           self (ReadFiles): The instance of the class.

           Returns:
           dict: A dictionary containing the file names as keys and the splitted documents as values.

           Raises:
           CustomException: If an error occurs during the file retrieval, reading, or splitting process.
           """
        try:
            # documents = {}
            documents = []
            file_details = self.get_file_names_and_types()
            for file in file_details:
                reader = self.get_file_reader(file.file_type)
                self.logger.info(
                    f"{file.file_name} is a {file.file_type} file. {reader.__name__} method is called. "
                )
                splitted_docs = reader(file_path=file.file_full_path,
                                       splitter=self.text_splitter)

                # documents[file.file_name] = {
                #     "documents": splitted_docs,
                #     "file_type": file.file_type
                # }
                documents.append(splitted_docs)

            return documents

        except Exception as e:
            raise CustomException(e, sys)
