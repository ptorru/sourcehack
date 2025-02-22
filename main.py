import llama_index
import phoenix as px
from os import environ
from dotenv import load_dotenv
from llama_index.core import (
    SimpleDirectoryReader,
    VectorStoreIndex,
    StorageContext,
    load_index_from_storage,
)
from llama_index.core.tools import QueryEngineTool, ToolMetadata
from llama_index.core.agent import ReActAgent
from llama_index.llms.openai import OpenAI

session = px.launch_app()
load_dotenv()

OPENAI_API_KEY = environ["OPENAI_API_KEY"]


def main():
    llm = OpenAI(model="gpt-4")
    query_engine_tools = []
    agent = ReActAgent.from_tools(
        query_engine_tools,
        llm=llm,
        verbose=True,
        max_turns=10,
    )

    response = agent.chat("Who had more profit in 2021, Lyft or Uber?")
    print(str(response))


if __name__ == "__main__":
    main()
