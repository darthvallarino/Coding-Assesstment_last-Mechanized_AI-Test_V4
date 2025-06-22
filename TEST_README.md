# Senior GenAI Engineer – 30‑Minute **Refactor & Improve** Coding Test

## Objective
Assess how quickly you can **read, diagnose, and meaningfully improve** an existing LangGraph multi‑agent workflow, specifically boosting **answer accuracy, performance (defined as quality & completeness of the answer itself to the question), or robustness** for the question the workflow is asked to solve. We want to see thoughtful refactors, not green‑field code.

* Read this entire document completely before starting.
* Feel free to add more eval steps 
* We do not care about code quality or craftmanship in this test.

---
## Baseline Code (already in repo)
The starter repo now ships with a refactored multi-agent LangGraph workflow:
- `agents.py` – defines agent logic, including validation and error handling for responses.
- `tools.py` – defines all available tools and the `ToolNode` for tool execution.
- `models.py` – LLM and model configuration.
- `flow.py` – (if present) utility functions or shared logic for agent nodes.
- `graph.py` – builds the LangGraph workflow using nodes for drafting, tool execution, and revision, with loop/termination logic.
- `workflow.py` – entry point: runs the workflow and prints each step's output.
- `GOAL.md` – this document.
- No `prompts.py` (prompts are now inlined in agent code).
- No requirements.txt in this repo version; use your own environment.

The goal is a system that engage with Reflexion, which is an architecture designed to learn through verbal feedback and self-reflection. The agent explicitly critiques its responses for tasks to generate a higher quality final response, at the expense of longer execution time.

Running (in python3.11.11)
```bash
export OPENAI_API_KEY=your_api_key_here 
pip install -r requirements.txt
python3 workflow.py           
```
works out‑of‑the‑box (assumes dependencies installed).

---
## Your Mission (30 min max)
1. **Run the baseline** once to capture its raw console output.
2. **Identify shortcomings** – accuracy, style, performance, error‑handling, DX, etc. Focus on improving the quality of the outputs. 
3. **Implement improvements (focus on answer quality)**:
   - Your code changes must measurably increase the correctness and robustness (answer quality, reduced hallucination, clearer structure) of the answer produced by `workflow.py`.
   - Touch any file(s). Keep the total diff ≤120 LOC added/changed.
   - Code must still run via `python3 workflow.py` with no extra flags.
4. **Document** your work in `IMPROVEMENTS.md` (≤400 words):
   1. *Brainstorming* – bullet list of all improvements you considered & why, in priority order and why you choosed the change you did.
   2. *Why* – for each change, quote the baseline or intermediate output that triggered it **and** cite 1 external reference (doc, article, repo) that influenced your approach.
   3. *Impact* – one‑line benefit statement (robustness, quality, latency, etc.).
   4. *Next Steps* – what you’d tackle with another 2 hours.

> **Tips:** 
> - Prioritize fixes that demonstrate clear thinking over ambitious half‑finished features.
> - Do not prioritize evaluation improvements, unless absolutely necessary.
> - Do not prioritize adding simple obvious improvements like WebTool, simple long & short memory, simple RAG, adding ReAct, dynamic adding of tools & their descriptions, inputs, and outputs to prompts of agents. We are looking for meaningful improvements to the output quality of the workflow.
> - Do not focus on improving the baseline code quality, craftmanship, or code structure of the original baseline code we provided. You must focus on tangible improvements to the output quality of the workflow (there is evaluation already hooked into the workflow).
> - Don't hesitate to use gpt, google, windsurf, cusor, etc. to help you with your task, but your documentations should be done manually, in your own words.

---
## Deliverables
- Updated source files committed to a github repo of your own. NOTE: You must track all commits. So commit this original repo first (in a private repo), and send us the final PR.
- `IMPROVEMENTS.md` per spec above.
- Any new test script(s) if that was one of your improvements (optional).

---
## Evaluation Rubric (internal)
| Area | Max pts | Key Signals |
|------|---------|-------------|
| Correctness (code runs) | **20** | `python3 workflow.py` executes without errors |
| Quality of Improvements | **30** | Correct decision about what to focus on and thought process. Demonstrably improves answer quality/accuracy and overall robustness |
| Justification & Research | **30** | References output snippets **and** reputable external sources |
| Prioritization Clarity | **10** | Reasonable triage given 30‑min cap |
| Code Craftsmanship | **5** | Idiomatic, readable, well‑scoped diff |
| Bonus: Unit or smoke tests added | **+5** | `pytest` or inline asserts |

> **Passing bar:** ≥70/100.
> **Hard fail:** Baseline no longer runs.

---
## Timing Guidance
| Task | Target mins |
|------|-------------|
| Baseline run + triage | 5 |
| Implement top 2–3 fixes | 18 |
| Sanity run & tweaks | 4 |
| Write `IMPROVEMENTS.md` | 3 |

Stay disciplined—ship something that works **and** proves you can lift code quality fast.
