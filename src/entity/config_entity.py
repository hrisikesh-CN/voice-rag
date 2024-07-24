from src.constant import *
from dataclasses import dataclass
from datetime import datetime
import os 

TIMESTAMP: str = datetime.now().strftime("%m_%d_%Y_%H_%M_%S")


@dataclass
class BaseArtifactConfig:
    artifact_dir: str = os.path.join(ARTIFACT_DIR, TIMESTAMP)
    timestamp: str = TIMESTAMP

base_artifact_config: BaseArtifactConfig = BaseArtifactConfig()

@dataclass
class FileHandlerConfig:
    artifact_dir: str = base_artifact_config.artifact_dir
    file_storage_dir: str = os.path.join(
        artifact_dir,
        FILE_STORAGE_ARTIFACT_DIR_NAME
    )
    
    
@dataclass
class DataTransformationConfig:
    pass