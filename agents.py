from models import *

from langchain_core.messages import HumanMessage, ToolMessage
from langchain_core.output_parsers.openai_tools import PydanticToolsParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from pydantic import ValidationError

from pydantic import BaseModel, Field


class Reflection(BaseModel):
    missing: str = Field(description="Critique of what is missing.")
    superfluous: str = Field(description="Critique of what is superfluous")


class AnswerQuestion(BaseModel):
    """Answer the question. Provide an answer, reflection, and then follow up with search queries to improve the answer."""

    answer: str = Field(description="~250 word detailed answer to the question.")
    reflection: Reflection = Field(description="Your reflection on the initial answer.")
    search_queries: list[str] = Field(
        description="1-3 search queries for researching improvements to address the critique of your current answer."
    )


class ResponderWithRetries:
    def __init__(self, runnable, validator):
        self.runnable = runnable
        self.validator = validator

    def respond(self, state: dict):
        response = []
        for attempt in range(3):
            response = self.runnable.invoke(
                {"messages": state["messages"]}, {"tags": [f"attempt:{attempt}"]}
            )
            try:
                self.validator.invoke(response)
                return {"messages": response}
            except ValidationError as e:
                error_message = f"{repr(e)}\n\nPay close attention to the function schema.\n\n"
                # Add more specific feedback for common errors, like missing citations
                if "references" in str(e) and "field required" in str(e).lower(): # new
                    error_message += "It looks like 'references' field is missing or malformed. Ensure you provide a list of URLs from the search results for citations."
                elif "answer" in str(e) and "word limit" in str(e).lower(): # new
                     error_message += "Your answer is likely exceeding the word limit. Please make sure it's around 250 words."
                
                error_message += self.validator.schema_json() + " Respond by fixing all validation errors." # new
                
                state["messages"].append(
                    ToolMessage(
                        content=error_message,
                        tool_call_id=getattr(response, 'tool_calls', [{}])[0].get("id", None),
                    )
                )
        return {"messages": response}