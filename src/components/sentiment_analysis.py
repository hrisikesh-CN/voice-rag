import os
import sys

from dotenv import load_dotenv
from langchain.agents import AgentType, initialize_agent
from langchain.tools import StructuredTool
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI
from pydantic.v1 import BaseModel, Field

from src.exception import CustomException

# Load environment variables from .env file
load_dotenv(override=True)


class SearchInput(BaseModel):
    sentiment: str = Field(
        description="""Analyse the user sentiment and enter one value out of three sentiments, 
        which are Positive, Neutral and Negative""")


class SentimentAnalyzer:
    def __init__(self):
        try:
            openai_api_key = os.getenv("OPENAI_API_KEY")
        except Exception:
            raise KeyError('OPENAI_API_KEY environment variable not found.')

        self.llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo", api_key=openai_api_key)

    @staticmethod
    def _get_sentiment(sentiment):
        print("The sentiment is ", sentiment)
        return sentiment

    def get_agent(self):
        try:
            sent = StructuredTool.from_function(
                func=self._get_sentiment,
                name="Sentiment",
                description="""Useful for Sentiment analysis, You will have to pass the values out of these, which are Positive, 
                Neutral, Negative""",
                args_schema=SearchInput,

            )

            prompt = ChatPromptTemplate.from_messages(
                [
                    (
                        "system",
                        "You are a bot who will do sentiment analysis"
                    ),
                    ("user", "{input}"),
                    MessagesPlaceholder(variable_name="agent_scratchpad"),
                ]
            )

            agent = initialize_agent(
                agent=AgentType.OPENAI_FUNCTIONS,
                tools=[sent],
                llm=self.llm,
                verbose=True,
                prompt=prompt

            )
            return agent

        except Exception as e:
            raise CustomException(e, sys)

    def analyze_sentiment(self, input: str):
        try:
            agent = self.get_agent()
            analyse = agent({
                "input": input + " Do sentiment analysis and return answer in one word, You will have to return just one word"})
            return analyse['output']

        except Exception as e:
            raise CustomException(e, sys)
