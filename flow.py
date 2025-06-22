from agents import *

import datetime

actor_prompt_template = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """You are expert researcher.
Current time: {time}

1. {first_instruction}
2. Reflect and critique your answer. Be severe to maximize improvement.
3. Recommend search queries to research information and improve your answer.
   When providing your answer, if you use information from search results, *always* include numerical citations directly after the relevant sentence or phrase.
   Add a "References" section at the bottom of your answer listing the URLs used, formatted as:
       - [1] URL
       - [2] URL
   Ensure your answer is concise, aiming for ~250 words, and directly addresses the question."""
        ),
        MessagesPlaceholder(variable_name="messages"),
        (
            "user",
            "\n\n<system>Reflect on the user's original question and the"
            " actions taken thus far. Respond using the {function_name} function.</reminder>",
        ),
    ]
).partial(
    time=lambda: datetime.datetime.now().isoformat(),
)
initial_answer_chain = actor_prompt_template.partial(
    first_instruction="Provide a detailed ~250 word answer.",
    function_name=AnswerQuestion.__name__,
) | llm.bind_tools(tools=[AnswerQuestion])
validator = PydanticToolsParser(tools=[AnswerQuestion])

first_responder = ResponderWithRetries(
    runnable=initial_answer_chain, validator=validator
)

# revision
revise_instructions = """Revise your previous answer using the new information from search results.
    - You should use the previous critique and the new information to add important, cited details to your answer.
        - You MUST include numerical citations in your revised answer to ensure it can be verified. Use the URLs from the search results as your references.
        - Add a "References" section to the bottom of your answer (which does not count towards the word limit). In form of:
            - [1] https://example.com (from search results)
            - [2] https://example.com (from search results)
    - You should use the previous critique to remove superfluous information from your answer and make SURE it is not more than 250 words.
    - Your output MUST include all required fields: 'answer', 'reflection', 'search_queries', and 'references', matching the function schema."""

# Extend the initial answer schema to include references.
# Forcing citation in the model encourages grounded responses
class ReviseAnswer(AnswerQuestion):
    """Revise your original answer to your question. Provide an answer, reflection,

    cite your reflection with references, and finally
    add search queries to improve the answer."""

    references: list[str] = Field(
        description="Citations motivating your updated answer, directly from search result URLs." # new
    )


revision_chain = actor_prompt_template.partial(
    first_instruction=revise_instructions,
    function_name=ReviseAnswer.__name__,
) | llm.bind_tools(tools=[ReviseAnswer])
revision_validator = PydanticToolsParser(tools=[ReviseAnswer])

revisor = ResponderWithRetries(runnable=revision_chain, validator=revision_validator)