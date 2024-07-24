import os

from dotenv import load_dotenv
from langchain.agents import AgentType, initialize_agent
from langchain.tools import StructuredTool
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI
from pydantic.v1 import BaseModel, Field

# Load environment variables from .env file
load_dotenv(override=True)

# Retrieve the API key
openai_api_key = os.getenv("OPENAI_API_KEY")
if openai_api_key is None:
    raise ValueError("OPENAI_API_KEY not found in environment variables")

llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo")


def bookf(sentiment):
    print("Book time is ", sentiment)
    return sentiment


class SearchInput(BaseModel):
    # bookdate: str = Field(description="Convert the date into DD-MM-YY so if users writes 15 July 2024 you should give 15-07-2024")
    sentiment: str = Field(
        description="Analyse the user sentiment and enter one value out of three sentiments, which are Positive, Neutral and Negative")


sent = StructuredTool.from_function(
    func=bookf,
    name="Sentiment",
    description="Useful for Sentiment analysis, You will have to pass the values out of these, which are Positive, Neutral, Negative",
    args_schema=SearchInput,

    # coroutine= ... <- you can specify an async method if desired as well
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
    llm=llm,
    verbose=True,
    prompt=prompt

)


def sentanalyse(input):
    analyse = agent({
        "input": input + " Do sentiment analysis and return answer in one word, You will have to return just one word"})
    return analyse['output']
