# Oracle Agentic AI Foundations Associate — Practice Test A

**Exam code:** 1Z0-1157-26  
**Format:** 40 original, single-best-answer questions  
**Suggested practice time:** 60 minutes (a self-imposed pacing target, not a statement of current Oracle exam policy)  
**Scoring:** 1 point per question; calculate your raw percentage as `correct ÷ 40 × 100`.

> This is an unofficial study aid. The questions are original and are not taken from, endorsed by, or guaranteed to match Oracle's live exam. Coverage follows the six modules described in Oracle's public learning-path overview. Oracle can change its course and exam objectives; check Oracle University for current details.

**Instructions:** Choose one best answer for each question. For a clean self-test, complete this file before opening the separate answer key: [`1Z0-1157-26-answer-key.md`](1Z0-1157-26-answer-key.md).

## Answer sheet

| Q | Answer | Q | Answer | Q | Answer | Q | Answer |
|---:|:---:|---:|:---:|---:|:---:|---:|:---:|
| 1 | ____ | 11 | ____ | 21 | ____ | 31 | ____ |
| 2 | ____ | 12 | ____ | 22 | ____ | 32 | ____ |
| 3 | ____ | 13 | ____ | 23 | ____ | 33 | ____ |
| 4 | ____ | 14 | ____ | 24 | ____ | 34 | ____ |
| 5 | ____ | 15 | ____ | 25 | ____ | 35 | ____ |
| 6 | ____ | 16 | ____ | 26 | ____ | 36 | ____ |
| 7 | ____ | 17 | ____ | 27 | ____ | 37 | ____ |
| 8 | ____ | 18 | ____ | 28 | ____ | 38 | ____ |
| 9 | ____ | 19 | ____ | 29 | ____ | 39 | ____ |
| 10 | ____ | 20 | ____ | 30 | ____ | 40 | ____ |

---

## 1. Introduction to AI Agents — Questions 1–6

### 1.
A support assistant must look up a service policy, query an order system, request confirmation before issuing a refund, and then report the outcome. Which capability most clearly distinguishes an agentic solution from a response-only chatbot?

A. A longer system prompt describing the policy  
B. An LLM-guided loop that can select tools, observe results, and continue toward the goal  
C. A higher temperature setting for more varied wording  
D. A static FAQ response containing refund instructions

### 2.
Which description best matches the ReAct pattern?

A. The model produces one final answer without using tools.  
B. The application executes a fixed sequence of tools regardless of intermediate results.  
C. The model writes a plan once, then never incorporates tool results.  
D. Reasoning and actions are interleaved; tool observations can influence the next step.

### 3.
In a typical LLM-plus-tools agent architecture, what is the primary role of orchestration?

A. Manage the model/tool cycle: pass context, dispatch tool calls, return observations, and decide when the run is complete  
B. Replace the LLM with a database that writes every response  
C. Guarantee that each model-generated action is correct  
D. Store the model's parameters and train it after every tool call

### 4.
A generated answer must be checked for prohibited personal data before it is shown to a user. Which control is most directly applicable?

A. An input-length limit applied before the model call  
B. A network rate limit on the API endpoint  
C. An output guardrail that validates or filters the response before display  
D. A larger context window

### 5.
An agent's inventory tool times out. What is the safest next behavior?

A. Treat the inventory result as unknown, retry only within defined limits, and report the limitation if it remains unavailable  
B. Assume the requested item is in stock because no error data was returned  
C. Ask the LLM to invent a likely inventory count  
D. Repeat the same call indefinitely until it succeeds

### 6.
An agent can issue customer refunds. Which design best reduces risk from an incorrect or malicious tool call?

A. Give the tool administrator privileges so it never encounters authorization errors.  
B. Let the LLM decide whether authorization checks are necessary.  
C. Apply least-privilege authorization and require confirmation or approval for high-impact actions.  
D. Hide the tool's name from the prompt but leave its permissions unrestricted.

## 2. LangChain for AI Agents — Questions 7–12

### 7.
In LangChain Expression Language, what does a composition such as `prompt | model | parser` generally express?

A. Three tools execute concurrently and their outputs are discarded.  
B. The model is converted into a prompt template.  
C. The parser runs first and decides whether the prompt is needed.  
D. A runnable pipeline passes each step's output to the next step.

### 8.
When defining a LangChain tool from a Python function, what most directly helps the framework expose an understandable, validated tool interface?

A. The Python file's filename and modification date  
B. A clear description plus parameter types/schema for the callable  
C. A larger LLM context window  
D. A conversation transcript stored in a global variable

### 9.
A LangChain agent receives a model response containing a valid tool call. What is the normal next step in the agent loop?

A. Display the raw tool-call JSON as the final user answer.  
B. Retrain the model on the tool-call arguments.  
C. Validate and execute the tool, add its observation to the conversation, then let the agent continue if needed.  
D. Ignore the call and start a new conversation.

### 10.
A workflow must always run the same three approved steps in the same order, with no runtime choice of next action. Which design is usually the better fit?

A. A fixed chain or runnable sequence  
B. An open-ended agent with every available tool  
C. A multi-agent handoff graph with no constraints  
D. A vector index without an execution workflow

### 11.
Why should an agent loop have an iteration or time limit?

A. To force every answer to use exactly one tool  
B. To prevent runaway cycles and bound latency or cost  
C. To guarantee that a tool result is factually correct  
D. To make model-generated arguments bypass validation

### 12.
A model proposes a tool call with a missing required argument. What should the application do?

A. Fill the argument with a guessed value and execute the call.  
B. Disable schema validation for this tool.  
C. Send the raw argument string to a shell for interpretation.  
D. Reject or return a structured validation error, then let the workflow recover safely.

## 3. Model Context Protocol (MCP) — Questions 13–19

### 13.
Which statement correctly describes the core MCP architecture?

A. A host application contains an MCP client that connects to an MCP server exposing capabilities.  
B. An MCP server is the LLM, and the host is a vector index.  
C. A client is always a remote cloud service; a host is always a database.  
D. MCP requires every tool to be compiled into the model.

### 14.
Which mapping of MCP server primitives is correct?

A. Tools are document stores; resources are model weights; prompts are network transports.  
B. Tools are templates; resources are callable functions; prompts are databases.  
C. Tools are callable capabilities, resources provide context/data, and prompts are reusable prompt templates.  
D. Tools, resources, and prompts are three names for the same primitive.

### 15.
Which statement about MCP messages is correct?

A. MCP sends only plain text and has no request/response structure.  
B. MCP requires a separate proprietary wire format for every tool.  
C. Transport choice determines the meaning of each tool.  
D. MCP uses JSON-RPC message patterns; request identifiers correlate responses, while transports carry those messages.

### 16.
A developer wants to launch a local MCP server as a child process. A separate service must be reachable over a network. Which transport pairing is appropriate?

A. Streamable HTTP for the child process; stdio for the remote service  
B. stdio for the local child process; Streamable HTTP for the network service  
C. SQL for the child process; JSON files for the remote service  
D. A model prompt for both, because MCP does not define transports

### 17.
What is a major benefit of using MCP instead of writing a one-off connector for every host/tool pairing?

A. A compatible server can expose capabilities through a common protocol to multiple compatible clients.  
B. It removes the need to authorize tool access.  
C. It guarantees that every model will choose the right tool.  
D. It eliminates the need to validate tool inputs.

### 18.
An MCP client needs to discover and then invoke a server's `lookup_customer` tool. Which flow best describes that interaction?

A. Read a prompt template and treat it as executable code.  
B. Send a resource URI to the LLM and skip the server.  
C. Discover available tools, call the named tool with structured arguments, then handle its result.  
D. Restart the host for every tool call because MCP cannot return results.

### 19.
An MCP server exposes a database-update tool. Which security practice is strongest?

A. Trust every client because MCP standardizes the tool description.  
B. Enforce authorization and least-privilege access at the server/tool boundary, and require approval for sensitive writes when appropriate.  
C. Put database credentials in the tool description so the model can select them.  
D. Rely on the LLM to decide which rows the user is allowed to change.

## 4. OpenAI Responses API and Agents SDK — Questions 20–26

### 20.
A team wants direct control of model requests, tool dispatch, and state handling. Which option is the most direct fit?

A. A visual no-code agent builder only  
B. A database vector index without an application  
C. A managed SDK runtime that hides all orchestration choices  
D. The Responses API directly, with the application owning the surrounding loop and state it needs

### 21.
In the OpenAI Agents SDK, what is the purpose of the runner abstraction?

A. It converts an agent into a static PDF.  
B. It stores vector embeddings but never calls the model.  
C. It executes an agent run, managing the agent loop and returning run results.  
D. It replaces all tools with prompt text.

### 22.
When should an agent hand off control to a specialist rather than simply call a small function tool?

A. When the specialist agent should take responsibility for the next part of the interaction or task  
B. Whenever a deterministic arithmetic operation is needed  
C. When the system needs to avoid all model calls  
D. When the caller wants to store a document in a vector database

### 23.
A function tool has been declared for an agent. Which statement about the call is most accurate?

A. The model itself directly executes the Python function in the application process.  
B. Declaring the function automatically grants access to every system the function can reach.  
C. Tool arguments never need validation if they are generated by a model.  
D. The model can request a structured call; the runtime/application executes the function and returns its result to the agent loop.

### 24.
Which example correctly distinguishes input and output guardrails?

A. Input guardrail formats the final answer; output guardrail creates a database index.  
B. Input guardrail checks a request before agent processing; output guardrail checks the result before it is returned.  
C. Both guardrails are model parameters that cannot be inspected.  
D. Output guardrails are only useful for image generation.

### 25.
Why use the Agents SDK's tracing and observability capabilities?

A. To guarantee the model never makes a mistake  
B. To avoid defining tool input schemas  
C. To inspect and debug agent runs, including model steps, tool calls, and handoffs  
D. To make every agent run deterministic regardless of model settings

### 26.
A manager agent must remain responsible for the final answer but delegate a bounded research task to a specialist and then combine the result with its own work. Which pattern best fits?

A. A permanent handoff that ends the manager's run  
B. Replacing the manager with a database trigger  
C. Giving the specialist unrestricted access to all tools and user data  
D. Invoking the specialist as a tool so the manager can retain control and use its result

## 5. OCI Enterprise AI Agents — Questions 27–33

### 27.
A team wants an API-first agent workflow on OCI, using OCI-supported models and tools while authenticating to OCI services. Which statement best describes the OCI Responses API?

A. It is a local Python package that only reads CSV files.  
B. It is an OpenAI-compatible API surface for OCI agent workflows, used with OCI endpoints and authentication.  
C. It is a replacement for all OCI identity and access controls.  
D. It is a transport protocol for MCP servers only.

### 28.
A team has a custom agent runtime that it wants to package and run on OCI-managed infrastructure instead of owning the hosting environment. Which OCI approach is the closest fit?

A. Deploy a hosted agentic application.  
B. Use a single SQL statement with no model or tools.  
C. Use only a local Responses API client and no deployment service.  
D. Store the source code in a vector store and treat it as a running endpoint.

### 29.
An agent must retrieve relevant passages from documents that have been added to an OCI vector store. Which Responses API tool is designed for this retrieval use case?

A. Code Interpreter  
B. A conversation ID  
C. A container file upload  
D. File Search

### 30.
Which statement best distinguishes application-defined function calling from remote MCP calling in an OCI Responses API workflow?

A. Function calling cannot use structured arguments, while MCP can.  
B. MCP is only for local Python functions, while function calling is only for remote websites.  
C. Function calling can return control to the application to execute its function; MCP calling connects the workflow to tools exposed by a remote MCP server.  
D. They are identical features with different names and no runtime differences.

### 31.
A multi-turn agent needs conversation history, and an administrator wants to organize related responses, conversations, files, and settings. Which pairing is most appropriate?

A. Use conversation state for turn history and a project to organize related agent resources/settings.  
B. Put the entire conversation in a tool description and use a container as the project.  
C. Use a vector distance metric as conversation memory.  
D. Use a database index for both history and project configuration.

### 32.
An OCI Enterprise AI NL2SQL workflow generates a SQL statement. What should the application assume about execution?

A. SQL generation automatically executes the query with administrator privileges.  
B. NL2SQL produces SQL; query execution is a separate step handled through an authorized database tool/connection.  
C. The SQL is executed by the model's prompt parser.  
D. Generated SQL can never be reviewed or constrained.

### 33.
An agent needs to run code in an isolated environment as part of a workflow. Which OCI capability is designed to provide a sandboxed execution environment?

A. A conversation history record  
B. A project name  
C. Containers used with the agent workflow  
D. A vector embedding model

## 6. Agentic AI for Oracle AI Database — Questions 34–40

### 34.
What is the primary role of the `VECTOR` data type in Oracle AI Database?

A. Store MCP protocol messages as relational table names  
B. Store numerical embeddings alongside business data to support semantic vector search  
C. Replace all SQL data types with natural-language prompts  
D. Encrypt an agent's conversation history without a key

### 35.
A query uses `VECTOR_DISTANCE(embedding, :query_vector, COSINE)` and should return the closest matches first. How should results normally be ordered?

A. Order by the vector distance descending, because larger distance means closer.  
B. Sort randomly, because distance is only metadata.  
C. Order by the text length of each document.  
D. Order by vector distance ascending so the smallest distances appear first.

### 36.
A support agent may retrieve only records belonging to the signed-in customer's tenant. Which search design is safest?

A. Apply an authorized relational predicate or database security policy for the tenant, then rank eligible rows by vector distance.  
B. Run an unfiltered global vector search and ask the LLM to remove other tenants' records.  
C. Put the tenant ID in the prompt but omit database-side authorization.  
D. Use cosine distance as an access-control mechanism.

### 37.
Which statement best compares exact and approximate vector search?

A. Approximate search is always more accurate and slower than an exact full scan.  
B. Exact search can compare the query against all vectors; approximate indexes can improve speed at a possible accuracy/recall trade-off.  
C. Exact search cannot use a distance metric.  
D. Approximate search is a synonym for keyword-only filtering.

### 38.
A team wants a database-native framework for multi-step agents that can plan, use tools, reflect on observations, and maintain conversation memory. Which capability is the best fit?

A. A plain relational `SELECT` with no agent framework  
B. A static SQL view  
C. Select AI Agent framework  
D. A vector index by itself

### 39.
What is a key benefit of the Autonomous AI Database MCP Server for compatible agent clients?

A. It makes database privileges unnecessary.  
B. It converts all SQL into a public REST API without authorization.  
C. It requires every customer to build and host a separate MCP server process.  
D. It can expose configured database agent tools through MCP while integrating with database security, reducing the need to manage separate MCP-server infrastructure.

### 40.
A business team wants to visually assemble and test a workflow from model, data-source, API, and agent components with minimal code. Which Oracle capability is the closest match?

A. Oracle AI Database Private Agent Factory's visual Agent Builder/Workflow Builder  
B. `VECTOR_DISTANCE` alone  
C. A local stdio transport with no agent builder  
D. A SQL execution plan
