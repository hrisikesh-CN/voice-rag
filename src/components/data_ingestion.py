import os, sys
from src.logger import get_logger
from src.exception import CustomException
from src.entity.config_entity import FileHandlerConfig
from src.entity.artifact_entity import FileHandlerArtifact


class DataIngestion:
    def __init__(self, file_handler_config: FileHandlerConfig):
        self.file_handler_config = file_handler_config
        self.logger = get_logger(__name__)

    def ingest(self,
               files: list):
        try:
            for file in files:
                file_name = file.filename.lower().replace(" ", "-").strip()
                file_full_path = os.path.join(self.file_handler_config.file_storage_dir, file_name)
                os.makedirs(os.path.dirname(file_full_path), exist_ok=True)
                with open(file_full_path, "wb") as file_handler:
                    file_handler.write(file.read())

            file_handler_artifact = FileHandlerArtifact(
                file_storage_dir=self.file_handler_config.file_storage_dir
            )
            return file_handler_artifact


        except Exception as e:
            self.logger.error(f"Error occurred during data ingestion: {str(e)}")
            raise CustomException(e, sys)
