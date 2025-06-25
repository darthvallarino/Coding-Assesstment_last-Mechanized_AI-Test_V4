# Improvements in the Research Agent

## Brainstorming and Prioritization

1.  **Integrate a real web search tool (Tavily):**
    * The most critical deficiency of the baseline was the lack of a real external information search capability. The current "search queries" merely fed back to the LLM, leading to citation hallucinations and ungrounded answers. Without access to external data, the agent cannot act as an "expert researcher." This change is fundamental to improving the accuracy and veracity of the response.

2.  **Enhance the `run_queries` function to process search results:**
    * Once a real search tool is integrated, how the results are presented to the LLM is crucial. Passing raw or inefficiently processed results could overwhelm the LLM or cause it to ignore important information. It is necessary to summarize and format the results in a useful way.

3.  **Refine prompts to reinforce the use of citations and word limit:**
    * Despite instructions, the LLM often exceeded the word limit and generated generic citations. Reinforcing the prompt with more explicit instructions on how to use and cite search information is essential.


4.  **Add response length validation in `ResponderWithRetries`:**
    * **Reason:** If the LLM consistently exceeds the word limit, length checking could be implemented in Pydantic validation or in `ResponderWithRetries` to enforce adherence to the limit.

5.  **Optimize the number of iterations or stopping logic:**
    * Evaluate whether 5 iterations are always optimal or if smarter stopping logic (e.g., when reflection no longer suggests significant improvements) could be more efficient.

## Why Changes Were Implemented

1.  **Integration of `TavilySearchResults` in `tools.py` and adjustment of `run_queries`:**
    * The baseline output consistently showed the agent hallucinating references (e.g., `[1] https://www.un.org/sustainabledevelopment/es/climate-action/`) and reflections indicated "Lack of depth... References are generic...". This was because `run_queries` did not perform a real external search.
    * Significantly increases the **robustness** and **quality** of the response by allowing the agent to access external information and incorporate it in a verifiable manner. Reduces **hallucinations**.

2.  **Refinement of `actor_prompt_template` and `revise_instructions` in `flow.py`:**
    * The agent's reflections often mentioned that references were not well-linked to the text and that the length was not respected (e.g., "the 'references' are generic and not directly linked to the precise information in the text. ... the response continues to exceed 250 words.").
    * Improves the **quality** of the response by guiding the LLM to use search sources more effectively and adhere to formatting constraints, such as the word limit.

3.  **Adjustment of `ValidationError` `ToolMessage` in `agents.py`:**
    * Pydantic validation error messages in the baseline output were technical (e.g., `ValidationError(...)`) and did not always provide clear guidance to the LLM on how to correct them contextually.
    * Improves **error handling** and **DX** for the agent, allowing it to correct its own outputs more efficiently by receiving more specific and actionable error messages. This indirectly improves response **robustness**.

## Next Steps (for another 2 hours)

1.  **Improve search result processing:** Currently, `run_queries` concatenates search results into a single string. An improvement would be:
    * Use a smaller model or a summarization function to synthesize results before passing them to the main LLM, especially if there are many results. This would reduce context pressure and improve relevance.
    * We could pass the results as a list of documents with metadata (like the source URL) to the LLM, making it easier for the LLM to reference specific sources within its response.

2.  **Implement length validation in `AnswerQuestion` / `ReviseAnswer` (Pydantic):**
    * Although feedback was added to the prompt, direct validation at the Pydantic level for the word limit (if Pydantic easily allows it with a `Field` or a custom `validator`) would be more robust. This would force the LLM to strictly adhere to the word limit or fail validation, compelling it to correct itself.

3.  **Refine `event_loop` logic:**
    * Instead of a fixed number of iterations, implement smarter stopping logic, for example, if the "reflection" indicates no more significant "missing" or "superfluous" elements, or if `search_queries` are empty, or if the change in response between iterations is minimal. This could improve **efficiency** and final **quality**.