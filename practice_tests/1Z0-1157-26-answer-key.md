# Oracle Agentic AI Foundations Associate — Practice Test A Answer Key

**Keep this file closed until you have completed** [`1Z0-1157-26-practice-test.md`](1Z0-1157-26-practice-test.md).

## Quick key

| Q | Answer | Q | Answer | Q | Answer | Q | Answer |
|---:|:---:|---:|:---:|---:|:---:|---:|:---:|
| 1 | B | 11 | B | 21 | C | 31 | A |
| 2 | D | 12 | D | 22 | A | 32 | B |
| 3 | A | 13 | A | 23 | D | 33 | C |
| 4 | C | 14 | C | 24 | B | 34 | B |
| 5 | A | 15 | D | 25 | C | 35 | D |
| 6 | C | 16 | B | 26 | D | 36 | A |
| 7 | D | 17 | A | 27 | B | 37 | B |
| 8 | B | 18 | C | 28 | A | 38 | C |
| 9 | C | 19 | B | 29 | D | 39 | D |
| 10 | A | 20 | D | 30 | C | 40 | A |

## Explanations

### 1. Introduction to AI Agents

1. **B** — An agent uses a model, tools, and orchestration to pursue a goal across multiple steps. It can inspect observations and choose what to do next; a response-only chatbot does not perform that tool-mediated loop.
2. **D** — ReAct interleaves reasoning with actions and observations. The result of an action can change the next step.
3. **A** — Orchestration manages the execution cycle: model request, tool dispatch, tool result, and continuation or completion. It does not make the model infallible.
4. **C** — An output guardrail checks generated content before it reaches the user. Input filters operate before model processing; rate limits address request volume.
5. **A** — A timeout is not evidence that the requested item is in stock. A bounded retry may be appropriate; otherwise report that the check could not be completed.
6. **C** — Least privilege and human approval for consequential actions reduce the impact of incorrect model decisions. Hiding a tool or relying on model judgment is not an authorization control.

### 2. LangChain for AI Agents

7. **D** — LCEL's pipe composition connects runnables so one step's output becomes the next step's input.
8. **B** — A tool needs a clear description and a parameter contract. Types/schema help constrain and validate the arguments supplied to the callable.
9. **C** — The application validates and executes the requested tool, returns its observation to the agent, and continues the loop if another model step is needed.
10. **A** — A fixed chain is a good fit when the sequence is known in advance. An agent is useful when the next action must be selected dynamically.
11. **B** — Iteration and time limits help bound cost and latency and prevent a faulty workflow from running indefinitely.
12. **D** — Invalid arguments should fail validation and be handled as a structured error or recovery step, not silently guessed or executed.

### 3. Model Context Protocol (MCP)

13. **A** — An MCP host is the application; it contains an MCP client that connects to an MCP server. The server exposes capabilities to compatible clients.
14. **C** — Tools are callable capabilities, resources provide data/context, and prompts are reusable templates. These primitives have distinct roles.
15. **D** — MCP messages use JSON-RPC patterns. A request ID associates a response with its request; the transport carries messages but does not redefine their meaning.
16. **B** — stdio is suited to a client-launched local subprocess. Streamable HTTP is a standard option for connecting to a network-accessible server.
17. **A** — MCP provides a common way for compatible hosts and servers to discover and use capabilities, reducing bespoke host-to-tool integrations. It does not remove the need for security controls.
18. **C** — The client discovers available tools, calls a selected tool with structured arguments, and handles the server's result.
19. **B** — Authorization must be enforced by the server/tool, using least privilege. Sensitive side effects may also require explicit approval; an MCP description is not an access-control policy.

### 4. OpenAI Responses API and Agents SDK

20. **D** — Direct API usage is suitable when the application wants to own its orchestration, tool dispatch, and state handling. The Agents SDK supplies a higher-level runtime.
21. **C** — The runner executes an agent run and manages the agent loop, returning the run result for the application to inspect.
22. **A** — A handoff transfers control to a specialist agent. A small function tool performs a bounded operation while the current agent remains in charge.
23. **D** — The model requests a structured tool call; the SDK or application validates and runs the function, then returns its output to the agent workflow.
24. **B** — Input guardrails evaluate requests before processing; output guardrails check the generated result before it is returned.
25. **C** — Traces make agent execution inspectable, including model steps, tool calls, and handoffs, which supports debugging and evaluation.
26. **D** — Calling a specialist as a tool lets the manager remain in control and use the specialist's response as an input to its final answer. A handoff instead transfers control.

### 5. OCI Enterprise AI Agents

27. **B** — OCI's Responses API is an OpenAI-compatible interface for OCI agent workflows, but requests use OCI endpoints and OCI authentication rather than becoming ordinary OpenAI service requests.
28. **A** — OCI documents API-first agent building and hosted agentic applications as distinct approaches. A hosted application fits packaging a custom runtime for managed deployment.
29. **D** — File Search retrieves relevant content from files attached to a vector store. Code Interpreter is for running code, not searching a document corpus.
30. **C** — With application-defined function calling, control can return to the application to execute its function. MCP calling connects the workflow to tools exposed by an MCP server.
31. **A** — Conversation state supports multi-turn context. A project organizes related agent resources and settings.
32. **B** — NL2SQL generates a SQL statement; execution is a separate authorized operation. Separating generation from execution supports review and access control.
33. **C** — OCI Containers are a workflow building block for sandboxed execution. A conversation record or vector model is not an execution sandbox.

### 6. Agentic AI for Oracle AI Database

34. **B** — Oracle's `VECTOR` type stores numerical embeddings. Keeping vectors alongside business data enables semantic search over that data.
35. **D** — With a distance metric, smaller distance means closer vectors. Ordering by `VECTOR_DISTANCE` ascending returns nearest matches first.
36. **A** — Apply tenant/authorization predicates or database security policies to limit eligible rows, then rank those rows by vector distance. Semantic similarity is not authorization.
37. **B** — Exact search can calculate distance against every vector. Approximate indexes can improve search speed at a possible recall/accuracy trade-off.
38. **C** — Select AI Agent is the database-native agent framework for multi-step planning and tool use, with reflection and memory capabilities described in Oracle documentation.
39. **D** — The managed Autonomous AI Database MCP Server exposes configured database tools to compatible clients and integrates with database security, reducing the need to operate a separate MCP-server deployment.
40. **A** — Private Agent Factory's Agent Builder and Workflow Builder provide a visual way to compose, test, and deploy agent workflows from connected components.

## Self-review

Count your correct answers by section, not just overall. A strong total can hide a gap in one module. Revisit the Oracle learning-path module for any section where you missed several questions. This score is for study planning only; it is not an Oracle score conversion or pass prediction.

## References

These sources informed the topic map and technical explanations. Product capabilities and protocol versions evolve; check the live documentation before exam day.

1. [Oracle University — Oracle Agentic AI Foundations training and certification](https://blogs.oracle.com/oracleuniversity/oracle-agentic-ai-foundations-training-certification-now-available) — official learning-path overview and six-module coverage.
2. [Oracle University — Agentic AI Foundations Associate exam listing](https://education.oracle.com/agentic-ai-foundations-associate/pexam_1Z0-1157-26) — exam name and code; Oracle's page was in maintenance when checked.
3. [LangChain — LCEL concepts](https://python.langchain.com/docs/concepts/lcel/) and [tool calling](https://python.langchain.com/docs/modules/model_io/output_parsers/).
4. [OpenAI Agents SDK documentation](https://openai.github.io/openai-agents-python/) and [OpenAI Agents guide](https://platform.openai.com/docs/guides/agents).
5. [MCP specification — transports](https://spec.modelcontextprotocol.io/specification/2025-03-26/basic/transports/).
6. [OCI Enterprise AI Agents](https://docs.oracle.com/en-us/iaas/Content/generative-ai/agents.htm), [building agents](https://docs.oracle.com/en-us/iaas/Content/generative-ai/building-agents.htm), and [Responses API](https://docs.oracle.com/en-us/iaas/Content/generative-ai/responses-api.htm).
7. [Oracle AI Database — AI Vector Search](https://docs.oracle.com/en/database/oracle/oracle-database/26/cncpt/artificial-intelligence-oracle-database.html), [Select AI Agent](https://docs.oracle.com/en/cloud/paas/autonomous-database/dedicated/adbaa/build-autonomous-agents-with-select-ai-agent.html), and [Autonomous AI Database MCP Server](https://docs.oracle.com/en-us/iaas/autonomous-database-serverless/doc/about-mcp-server.html).
8. [Oracle AI Database Private Agent Factory — Agent Builder](https://docs.oracle.com/en/database/oracle/agent-factory/26.4/paias/agent-builder.html).
