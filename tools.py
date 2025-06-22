from langchain_core.tools import StructuredTool

from langgraph.prebuilt import ToolNode
from agents import *
from models import *
from flow import *

def run_queries(search_queries: list[str], **kwargs):
    """Run the generated queries."""
    # Directly pass the queries to the LLM, not the literal '{query}'
    return llm.invoke(search_queries) # this passes all queries at once, should probably be one by one. 


tool_node = ToolNode(
    [
        StructuredTool.from_function(run_queries, name=AnswerQuestion.__name__),
        StructuredTool.from_function(run_queries, name=ReviseAnswer.__name__),
    ]
)