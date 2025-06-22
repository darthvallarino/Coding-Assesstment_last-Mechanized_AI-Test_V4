from langchain_openai import ChatOpenAI  

DEFAULT_LLM={
    "model_name": "gpt-4.1",
    "temperature": 1
}

llm = ChatOpenAI(**DEFAULT_LLM)

