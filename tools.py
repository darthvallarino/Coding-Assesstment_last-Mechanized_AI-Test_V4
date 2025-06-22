from langchain_core.tools import StructuredTool

from langgraph.prebuilt import ToolNode
# from agents import No longer needed
# from models import No longer needed
# from flow import No longer needed

from langchain_community.tools.tavily_search import TavilySearchResults # new

# Initialize the Tavily search tool
tavily_tool = TavilySearchResults(max_results=5) # new

def run_queries(search_queries: list[str], **kwargs): # Removed llm from signature, as it's not directly used here
    """Run the generated search queries and return summarized results."""
    all_results = []
    for query in search_queries:
        try:
            # Execute each query individually using Tavily
            results = tavily_tool.invoke({"query": query}) # new
            # Extract relevant content and append a simplified representation to all_results
            for result in results: # new
                all_results.append(f"Source: {result['url']}\nContent: {result['content']}") # new
        except Exception as e:
            all_results.append(f"Error running query '{query}': {e}")
    
    # Return a single string that summarizes all search results
    if not all_results:
        return "No search results found for the queries."
    
    # Concatenate results with clear separators for the LLM
    return "\n\n--- SEARCH RESULT START ---\n\n" + "\n\n".join(all_results) + "\n\n--- SEARCH RESULT END ---\n"


# Update ToolNode to use the actual search tool
tool_node = ToolNode(
    [
        StructuredTool.from_function(
            func=run_queries,
            name="run_search_queries",
            description="Executes search queries to find external information and returns the results."
        )
    ]
)