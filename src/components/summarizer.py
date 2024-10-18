import sys

from langchain.chains.summarize import load_summarize_chain
from langchain_openai import ChatOpenAI

from src.entity.artifact_entity import DataTransformationArtifact
from src.exception import CustomException
from src.logger import get_logger


class Summarizer:
    def __init__(self,
                 data_transformation_artifact: DataTransformationArtifact):

        self.data_transformation_artifact = data_transformation_artifact
        self.logger = get_logger(__name__)

    def summarize(self):
        try:
            llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo-1106")
            summarizer_chain = load_summarize_chain(llm=llm, chain_type="stuff")
            summaries = {}
            files = self.data_transformation_artifact.documents
            # documents =
            for file_name in files:
                docs = files[file_name]["documents"]
                summary = summarizer_chain.invoke(docs)
                summaries[file_name] = summary
                self.logger.info(f"Summarized {file_name}")

            return summaries

        except Exception as e:
            raise CustomException(e, sys)

