import llama_index
import phoenix as px
from os import environ
from dotenv import load_dotenv
from llama_index.core import (
    SimpleDirectoryReader,
    VectorStoreIndex,
    StorageContext,
    load_index_from_storage,
    PromptTemplate,
)
from llama_index.core.tools import QueryEngineTool, ToolMetadata
from llama_index.core.agent import ReActAgent
from llama_index.llms.openai import OpenAI
from llama_index.core.tools import BaseTool, FunctionTool
import json


# The flow will be like this:
# 1) user provides a link to the original article
# 2) you then extract the references from the article
# 3) you add the original article to the graph
# 4) you add the references to the graph
# 5) you repeat this process for each reference

react_system_header_str = """\
You are a news article agent. Your job is to build a knowledge graph of news articles and their references.
You can parse articles, and you have access to tools to manipulate the graph.
"""

react_system_prompt = PromptTemplate(react_system_header_str)

# Start the Phoenix server
# session = px.launch_app()
load_dotenv()

OPENAI_API_KEY = environ["OPENAI_API_KEY"]


def multiply(a: int, b: int) -> int:
    """Multiply two integers and returns the result integer"""
    return a * b


multiply_tool = FunctionTool.from_defaults(fn=multiply)


def add(a: int, b: int) -> int:
    """Add two integers and returns the result integer"""
    return a + b


add_tool = FunctionTool.from_defaults(fn=add)


def article_parser(link: str) -> dict:
    print(f"This was the link given {link}")
    # NEed to load the dummy index, then return the data for the matching article
    dummy = json.load(open("mocking/article_data.json"))
    for article in dummy["articles"]:
        if article["link"] == link:
            return article

    return "Could not find the article"


article_parser_tool = FunctionTool.from_defaults(
    fn=article_parser,
    name="article_parser",
)

original_link = "https://original.com"


GRAPH = {
    "nodes": {
        # {
        #     "node_id":
        #     "link":
        #     "children": []
        # }
    }
}


def add_node_to_index(link, node_id):
    GRAPH["nodes"]["node_id"] = {"node_id": node_id, "link": link, "children": []}


add_node_to_index_tool = FunctionTool.from_defaults(
    fn=add_node_to_index,
    name="add_node_to_index",
)


def add_child_to_node(node_id, child_id):
    GRAPH["nodes"][node_id]["children"].append(child_id)


add_child_to_node_tool = FunctionTool.from_defaults(
    fn=add_child_to_node,
    name="add_child_to_node",
)


def get_graph():
    return str(GRAPH)


get_graph_tool = FunctionTool.from_defaults(
    fn=get_graph,
    name="get_graph",
)

from openinference.instrumentation.llama_index import LlamaIndexInstrumentor
from phoenix.otel import register


def main():
    tracer_provider = register()
    LlamaIndexInstrumentor().instrument(tracer_provider=tracer_provider)
    llm = OpenAI(model="gpt-4")
    query_engine_tools = [
        multiply_tool,
        add_tool,
        article_parser_tool,
        add_node_to_index_tool,
        add_child_to_node_tool,
        get_graph_tool,
    ]
    agent = ReActAgent.from_tools(
        query_engine_tools,
        llm=llm,
        verbose=True,
        max_iterations=50,
        tracing=True,  # Enable tracing
        tracing_server_url="http://localhost:8000",  # Point to local Phoenix server
    )

    try:
        response = agent.chat(
            f"You are a news article agent. Your job is to build a knowledge graph of news articles and their references. You can parse articles, and you have access to tools to manipulate the graph. Can you build me the knowledge graph for this article: {original_link}"
        )
    except Exception as e:
        print("Error in agent chat: ", e)
    else:
        print(str(response))

    print("The graph is: ", get_graph())


if __name__ == "__main__":
    main()
