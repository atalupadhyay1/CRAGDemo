# Agentic AI: Foundations to Production Multi-Agent Systems

A progressive master course with a runnable, dependency-free lab track. It covers the subject sequence visible in the linked Simplilearn course description and expands each topic into learning outcomes, architecture, implementation patterns, production controls, and exercises.

## Source fidelity and lesson order

The reference video is [Agentic AI Full Course in 24 Hours | Master AI Agents & Automation](https://www.youtube.com/watch?v=CW01eBY9rGk), by Simplilearn. The YouTube page exposes a broad description but did not expose a transcript or timestamped chapter list in the material available to this course build. The repository also did not contain an `AgenticAI` folder before this course was added. Therefore, this package preserves the **published topic progression**, not unverified timestamps or chapter titles:

1. Generative AI, LLMs, and agentic AI foundations
2. Prompt engineering
3. Retrieval-augmented generation (RAG)
4. Agent memory
5. Tool integration and function calling
6. Workflow automation
7. Multi-agent collaboration
8. LangGraph
9. CrewAI
10. Model Context Protocol (MCP)
11. Safety, ethics, UX, and evaluation
12. Deployment and LLMOps
13. Integrated capstone

If exact video chapters or transcript-derived timings are required, add the transcript or chapter list and the module map can be aligned to it precisely.

## Audience and prerequisites

- Beginner-to-intermediate Python developers, cloud/data practitioners, technical product leads, and architects.
- Comfortable reading Python and JSON. Familiarity with HTTP, APIs, and basic SQL is helpful, not mandatory.
- No model API key is needed for the included labs. The first and third labs use deterministic teaching doubles; they demonstrate orchestration mechanics, not a reasoning LLM. The RAG lab uses this repository's local CRAG engine and sample corpus.

## Learning outcomes

By the end, learners can:

- Distinguish chat, chains/workflows, and agents; explain the model–tools–orchestration loop.
- Design prompts, structured tool contracts, control flow, state, retrieval, and memory with explicit trust boundaries.
- Build and test a bounded tool-using agent, a grounded RAG response, and a small manager/specialist workflow.
- Compare LangGraph, CrewAI, and MCP by abstraction and operational trade-offs rather than trend.
- Design human approval, authorization, privacy, evaluation, observability, reliability, and cost controls for production.
- Present an agent system with measurable acceptance criteria and a rollback plan.

## Course map

| Module | Video-topic sequence | Main artifact |
|---|---|---|
| 1 | Foundations: generative AI, LLMs, and agentic AI | Agent use-case and risk statement |
| 2 | Prompt engineering | Versioned prompt contract and eval set |
| 3 | RAG | Retrieval/evidence scorecard |
| 4 | Agent memory | State and retention design |
| 5 | Tool integration | Validated tool registry and approval policy |
| 6 | Workflow automation | State machine and failure/recovery map |
| 7 | Multi-agent collaboration | Agent topology and message contract |
| 8 | LangGraph | Graph/state/checkpoint design |
| 9 | CrewAI | Role/task/process design and comparison |
| 10 | MCP | Host/client/server integration and trust model |
| 11 | Safety, ethics, UX, evaluation | Threat model and evaluation harness |
| 12 | Deployment and LLMOps | Production readiness checklist and SLOs |
| 13 | Capstone | Tested, observable, bounded agentic application |

The full lesson plan is in [`MASTER_COURSE.md`](MASTER_COURSE.md). Runnable labs are in [`labs/`](labs/).

## Run the baseline labs

Requires Python 3.10+; no additional packages or API keys are needed for the baseline labs. Run commands from the repository root:

```bash
python AgenticAI/labs/agent_loop_demo.py
python AgenticAI/labs/rag_demo.py
python AgenticAI/labs/multi_agent_demo.py
python -m unittest discover -s AgenticAI/labs -p 'test_*.py' -v
```

`rag_demo.py` imports the existing [`rag_engine.py`](../rag_engine.py) and reads [`data/sample_docs.json`](../data/sample_docs.json). It does not make external search calls. The examples in `labs/optional/` connect to the named frameworks:

```bash
python -m pip install langgraph
python AgenticAI/labs/optional/langgraph_workflow.py

python -m pip install crewai
export OPENAI_API_KEY='configured-out-of-band'
python AgenticAI/labs/optional/crewai_evidence_crew.py

python -m pip install 'mcp>=1.2.0'
# Configure an MCP-compatible client to launch mcp_server.py using stdio.
```

The optional LangGraph graph needs no model key. The CrewAI exercise requires a configured model provider and makes model requests. The MCP server uses stdio and should be launched by an MCP client. Pin framework/provider versions in your own lockfile before production use; never commit API keys.

## Recommended pacing

A 12–13 week cohort can spend one module per week, with 3–5 hours of reading, lab work, review, and reflection per module. A self-paced learner can move faster, but should keep the lab/evaluation checkpoints. Do not treat this proposed pacing as the video's exact runtime or schedule.

## References

The lessons link primary documentation for framework- and cloud-specific behavior. Product APIs change quickly; pin tested dependency versions and re-check the vendor docs before deployment.
