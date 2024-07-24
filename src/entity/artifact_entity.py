from dataclasses import dataclass
from typing import Union, List, Dict

from langchain_core.documents import Document


@dataclass
class FileHandlerArtifact:
    file_storage_dir: str
    
    
@dataclass
class DataTransformationArtifact:
    documents: Union[List[Document], Dict[str, Dict[str, List[Document]]]]
    