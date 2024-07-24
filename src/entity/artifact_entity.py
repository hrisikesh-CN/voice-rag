from dataclasses import dataclass

from langchain_core.documents import Document


@dataclass
class FileHandlerArtifact:
    file_storage_dir: str
    
    
@dataclass
class DataTransformationArtifact:
    documents: list[Document]
    