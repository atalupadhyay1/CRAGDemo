# Master Course: Agentic AI — From Foundations to Advanced Multi-Agent Systems

**Audience:** beginner through advanced  
**Reference:** [Simplilearn — Agentic AI Full Course in 24 Hours](https://www.youtube.com/watch?v=CW01eBY9rGk)  
**Course type:** original, vendor-aware learning material; not a transcript or reproduction of the video  
**Lab baseline:** Python 3.10+, standard library; optional framework/provider integrations are identified separately

> **Lesson-structure note.** The linked YouTube page provides a broad topic sequence but no transcript or timestamped chapter list in the retrieved page. This course preserves the progression explicitly stated in its description—foundations, prompt engineering, RAG, memory, tools, workflow automation, multi-agent systems, LangGraph, CrewAI, MCP, then deployment/LLMOps—and expands it into teachable lessons. It does not invent video timestamps or claim to reproduce unobserved chapters. Exact timestamp alignment requires the video's transcript or chapter list.

---

## How to learn from this course

Agentic AI can feel like a collection of fashionable names. Resist the urge to memorize frameworks first. Start with a user problem, decide what the system may do, and then choose the smallest reliable loop that can do it.

Every module follows the same learner-centered rhythm:

1. **Picture it:** connect the idea to a familiar human or software process.
2. **Name it:** define the terms and their limits.
3. **Build it:** run or inspect a small implementation.
4. **Break it:** test failure, ambiguity, misuse, and edge cases.
5. **Prove it:** measure whether the behavior is useful and safe.
6. **Reflect:** explain what should remain deterministic and where a person must stay in control.

The offline labs are deliberately deterministic. A scripted planner lets learners see the control flow without paying for an API or confusing a demo with a real reasoning model. In a production integration, replace that adapter with a provider/model interface; keep the authorization, validation, evaluation, and observability around it.

### Learning outcomes

By the end, learners can:

- Explain the difference between a generative model, a workflow, an agent, and a multi-agent system.
- Design a bounded model–tool–orchestrator loop with typed inputs, limits, recoverable errors, and human approval.
- Build a retrieval-augmented response that can identify its evidence and abstain when evidence is weak.
- Choose between short-term context, persistent memory, a knowledge base, and an ordinary application database.
- Compare LangGraph, CrewAI, MCP, and workflow-automation tools without treating them as interchangeable.
- Establish an evaluation set and monitor quality, safety, latency, availability, and cost.
- Present a production design with explicit trust boundaries, rollback, and owner responsibilities.

### Baseline architecture

```text
User / calling application
          │ authenticated request
          ▼
Policy + input validation ──► Orchestrator / state machine
                                      │
                 ┌────────────────────┼───────────────────┐
                 ▼                    ▼                   ▼
            Model adapter       Retrieval service    Tool gateway
                 │                    │                   │
                 └──────────────► Evidence / results ◄────┘
                                      │
                       output checks + approval gates
                                      │
                                      ▼
                         Answer / action / escalation
                                      │
                         traces, metrics, audit records
```

The model is not the authorization system, the database, or the source of truth. It proposes language and actions. The application decides which actions are allowed, validates inputs, executes approved operations, and records what happened.

---

# Part I — Foundations

## Module 1 — Generative AI, LLMs, and agentic AI

**Lesson question:** What makes a system agentic, and what does not?

### Learning objectives

- Distinguish a language model's generation from an application's control loop.
- Describe autonomy as bounded decision-making, not unrestricted permission.
- Identify the model, tools, state, orchestrator, policies, and user as separate components.
- Decide whether a prompt, deterministic workflow, or agent is the smallest fit.

### Teach the mental model

A generative model predicts or produces content from context. An agentic application adds a goal, a choice of actions, observations from the outside world, and a control loop that decides whether to continue. A useful first approximation is:

```text
agentic application = model + tools + state + orchestration + policy
```

This is a design model, not a claim that every product implements these parts the same way. The model can recommend a tool call; the surrounding application validates, authorizes, and runs it. An agent can also decide not to act, ask a clarifying question, or hand the task back to a person.

Use this ladder:

| System | Who decides the next step? | Example |
|---|---|---|
| Prompt/model call | The application calls once | Draft a response from supplied text |
| Deterministic workflow | Code follows an authored path | Validate an order, then create an invoice |
| Tool-using agent | A model proposes actions inside bounded policy | Search policy, inspect a ticket, draft a recommendation |
| Multi-agent workflow | Several bounded components coordinate | Researcher gathers evidence; reviewer checks it |

Do not choose an agent just because a task is complex. If a fixed state machine solves it, that is often easier to test and govern.

### Core terms

- **Goal:** desired outcome, expressed in language and translated into explicit acceptance criteria.
- **Tool:** a callable capability with a name, description, schema, authorization rules, and result contract.
- **Observation:** a tool result or system event returned to the controller; it is evidence, not automatically truth.
- **Orchestrator:** the component that manages turns, tool dispatch, retries, state, and termination.
- **Autonomy boundary:** the decisions an agent may make without a person, and the actions it may not take.
- **Human-in-the-loop:** a person supplies clarification, approval, review, or escalation at a defined point.

### Design exercise: should this be an agent?

For each task, identify whether a prompt, a deterministic workflow, or an agent is appropriate:

1. Convert a known CSV schema to a fixed JSON schema.
2. Decide which of three tools to use after inspecting a support ticket.
3. Send a wire transfer.
4. Summarize a policy paragraph.

For every agent candidate, write: `goal`, `allowed actions`, `forbidden actions`, `evidence needed`, `stop condition`, and `human escalation condition`.

### Common misconception

“An agent can act without human involvement” is not a product requirement. The production question is: **which decisions are safe to delegate, under which controls, with what recourse?**

### Exit check

Explain the difference between an LLM proposing `issue_refund(amount=...)` and the application authorizing and executing a refund.

---

## Module 2 — Prompt engineering for agentic systems

**Lesson question:** How do instructions shape a system without pretending to be security controls?

### Learning objectives

- Write prompts with a goal, context, constraints, tool guidance, and completion criteria.
- Separate trusted instructions from user data and retrieved/tool content.
- Use examples and structured output only where they improve measurable behavior.
- Version prompts and test changes against a fixed evaluation set.

### A practical prompt contract

```text
Role and task:
  What job is the system responsible for?

Success criteria:
  What facts or outputs must be present?

Boundaries:
  What must it not do? When must it abstain or ask?

Evidence policy:
  Which sources may support claims? How are sources cited?

Tool policy:
  Which tool is suitable for which operation? Which actions require approval?

Output contract:
  What schema or user-facing shape is required?
```

For an agent, the prompt is one input to a larger policy system. A sentence such as “never access another tenant's data” does not replace tenant-scoped database authorization. Prompt instructions are helpful for behavior; access control must be enforced where the data or action is reached.

### Prompt-injection boundary

Treat user text, retrieved documents, emails, web pages, and tool outputs as **untrusted data**. A document can contain instructions that appear to address the model. That does not make it a trusted system instruction. Keep the trust boundary explicit in the prompt and enforce it in code:

- Give tools only the data and operations needed for the current task.
- Do not let retrieved text grant new privileges or rewrite policy.
- Validate structured output and tool arguments.
- Prevent the model from choosing arbitrary URLs, SQL, shell commands, or file paths without a constrained gateway.
- Add a human gate for irreversible or high-impact actions.

### Prompt test matrix

For each prompt version, test at least:

- Normal request, vague request, and conflicting request.
- Empty or oversized input.
- Malicious instructions inside a retrieved passage.
- No evidence, contradictory evidence, and stale evidence.
- Tool timeout, malformed arguments, and tool permission denial.
- Output schema violation and sensitive data in the proposed answer.

### Exercise

Write a prompt for an “internal runbook assistant.” The assistant may search runbooks and draft commands but may not execute commands. Test whether your prompt correctly asks a clarifying question when an environment is unspecified. Then explain which rule must be enforced outside the prompt.

### Exit check

Give one example of a prompt instruction and one example of an enforceable authorization control. They are not interchangeable.

---

# Part II — Grounding and action

## Module 3 — Retrieval-augmented generation (RAG)

**Lesson question:** How can a model answer from a changing private corpus without pretending its memory is a database?

### Learning objectives

- Trace ingestion, chunking, embedding, indexing, retrieval, context assembly, and citation.
- Explain vector, lexical, and hybrid retrieval in plain language.
- Evaluate retrieval quality separately from answer quality.
- Build a response that cites retrieved evidence and abstains when it is insufficient.

### RAG pipeline

```text
Documents → parse/clean → chunk + metadata → embed/index
                                              ▲
Question → query transform → retrieve → filter/rerank
                                              │
                   instructions + evidence ───┘
                           ▼
                  answer + citations / abstention
```

An embedding maps content to a numerical representation so semantically similar passages can be found even when they do not share exact words. Keyword search is useful for IDs, names, version strings, and exact phrases. Hybrid retrieval combines signals. Metadata filters can enforce corpus, version, tenant, language, and effective-date constraints before generation.

### Design decisions that matter

- **Chunk size and overlap:** too small loses context; too large can dilute relevance and consume context budget.
- **Metadata:** keep source ID, title, version, effective date, owner, permissions, and chunk location.
- **Freshness:** re-index updates, remove revoked sources, and version corpora.
- **Retrieval threshold:** a high score is not proof. Inspect whether the passage answers the question.
- **Reranking:** can reorder a candidate set using a more precise relevance model; it cannot repair a missing corpus.
- **Citation:** cite the actual source and passage used, not a plausible-looking link.
- **Abstention:** if evidence is missing or contradictory, say what cannot be confirmed and identify the missing source.

### Corrective loop

1. Retrieve a small candidate set.
2. Judge whether it directly supports the request.
3. If weak, rewrite or expand the retrieval query and retry once or within a strict budget.
4. Optionally use a configured external search tool for questions that need current public information.
5. Keep retrieved web data untrusted; cite it and evaluate source quality.
6. If evidence remains insufficient, abstain.

### Lab

From the repository root:

```bash
python AgenticAI/labs/rag_demo.py
```

The script queries the existing CRAG engine using its local sample corpus. Try changing the question to one answered by the corpus and one not answered by it. Compare `retrieval.relevant`, reformulation steps, citations, and the refusal behavior. No web key is used.

### Evaluation mini-lab

Create 20 questions with expected source IDs. Measure:

- **Recall@k:** did the expected evidence appear in the top `k` passages?
- **MRR:** how highly ranked was the first relevant passage?
- **Citation precision:** does each citation support its adjacent claim?
- **Answer faithfulness:** did the answer add claims absent from evidence?
- **Abstention quality:** does it refuse only when support is genuinely inadequate?

### Exit check

If an answer is wrong, determine whether the cause is ingestion, retrieval, permissions, evidence selection, generation, citation, or evaluation before changing the prompt.

---

## Module 4 — Agent memory and state

**Lesson question:** What should an agent remember, for how long, and on whose authority?

### Learning objectives

- Distinguish current-turn context, conversation state, durable user memory, and a knowledge base.
- Choose a retention and deletion policy before selecting a memory store.
- Prevent memory from crossing tenants or silently becoming a shadow profile.
- Design compact, inspectable state rather than blindly appending full histories.

### Four useful categories

| Category | Purpose | Example | Typical control |
|---|---|---|---|
| Turn context | Resolve the current request | User says “the second one” | Short-lived request state |
| Conversation state | Continue a multi-turn workflow | Chosen device, pending approval | Conversation ID, TTL, access checks |
| User preference memory | Reuse an explicit, durable preference | Preferred language | Consent, inspect/edit/delete, provenance |
| Knowledge base | Retrieve organizational facts | Approved product manual | Source governance, versioning, ACL filters |

Do not store every conversation as “memory.” Memory can be wrong, stale, sensitive, or written by an attacker. Keep provenance, subject/tenant boundaries, retention limits, and a way to inspect and delete it.

### State model

A useful state schema is explicit and typed:

```json
{
  "request_id": "req-123",
  "tenant_id": "tenant-7",
  "user_id": "user-42",
  "goal": "prepare a support response",
  "facts": [],
  "pending_action": null,
  "approval": "not_requested",
  "tool_results": [],
  "version": 1
}
```

Store only what the next step needs. Avoid treating an LLM-generated summary as authoritative; preserve the source messages or events needed to verify high-impact facts.

### Exercise

For a travel-planning assistant, classify: current dates, passport number, seat preference, booking confirmation, and retrieved airline policy. Specify whether each is ephemeral, consented memory, transactional record, or retrieval content, and how it is deleted or corrected.

### Exit check

Explain why a vector database, conversation history, and user profile memory solve different problems.

---

## Module 5 — Tool integration and function calling

**Lesson question:** How does a model request an action without receiving unbounded authority?

### Learning objectives

- Define a tool with a narrow purpose, typed schema, result contract, authorization, and audit trail.
- Distinguish tool selection from tool execution.
- Implement validation, least privilege, timeouts, idempotency, retry policy, and approval.
- Handle tool errors as observations rather than turning them into invented facts.

### Tool contract

```text
name: lookup_order
purpose: read one order visible to the authenticated user
input: { order_id: string }
authorization: user may read this order in this tenant
side effect: none
result: { status, items, updated_at }
timeout: 3 seconds
retry: one retry for transient errors only
logging: request ID, tool name, outcome, duration; redact secrets
```

The tool description helps the model choose. The schema constrains shape. The application still validates values and identity. Authentication answers “who is calling?” Authorization answers “may this caller perform this operation on this resource?”

### Safe execution checklist

- Allowlist tool names and validate required/extra fields, types, lengths, ranges, and enums.
- Derive identity and tenant from authenticated server context, not model-supplied arguments.
- Use an idempotency key for retryable writes.
- Apply timeouts, bounded retries, rate limits, and concurrency limits.
- Separate read tools from write tools.
- Use least-privilege credentials per tool.
- Require confirmation for irreversible or high-impact side effects.
- Return structured errors; never expose stack traces or secrets to the model/user.
- Record an auditable operation ID and final outcome.

### Lab

```bash
python AgenticAI/labs/agent_loop_demo.py
```

Inspect how the loop validates tool arguments, records observations, limits steps, and returns a final response. The `ScriptedPlanner` is a deterministic test double. It is not a substitute for an LLM and does not authorize any real external action.

### Exercise

Design tools for “cancel subscription.” Split discovery, eligibility check, cancellation, and confirmation into narrow operations. Add a user approval step before the irreversible action. Test replayed requests and a timeout after the remote service may already have committed.

### Exit check

Why is “the model generated valid JSON” insufficient evidence that a tool call is safe?

---

# Part III — Workflows and collaboration

## Module 6 — Workflow automation

**Lesson question:** Where should a deterministic workflow end and an agent begin?

### Learning objectives

- Model a business process as explicit states, transitions, and events.
- Use an agent for bounded interpretation or branch selection, not for every step.
- Design durable, idempotent, observable workflows with timeouts and human approvals.
- Connect agentic components to automation platforms such as n8n without surrendering control boundaries.

### State-machine view

```text
RECEIVED → VALIDATED → NEEDS_CLARIFICATION
                    → READY_FOR_REVIEW → APPROVED → EXECUTED → VERIFIED
                                           │                    │
                                           └─ REJECTED          └─ COMPENSATION / ESCALATION
```

Persist the state transition, actor, timestamp, and idempotency key. A process that spans a database, email provider, and billing API is not one atomic transaction. Plan for partial success and compensating actions.

### Workflow versus agent

Use a **workflow** for invariant ordering, policy enforcement, retries, and side effects. Use an **agent** when natural-language interpretation or runtime choice among allowed next steps adds value. Common pattern: deterministic workflow owns the boundary; agent proposes the next allowed action; workflow validates and commits it.

### Automation integration patterns

- Trigger from a queue/event rather than keeping an HTTP request open for long tasks.
- Persist the run ID and state so work can resume after a process restart.
- Keep human approval as a first-class event, not a hidden pause.
- For n8n or another visual automation platform, treat connectors/credentials as privileged resources; version flows and promote them through dev/staging/prod.
- Use a dead-letter queue and replay policy for failures; replay must not duplicate side effects.

### Exercise

Draw a workflow for an invoice assistant. Mark where the LLM interprets the invoice, where deterministic validation runs, where a reviewer approves a payment, and what happens when the payment API times out after accepting the request.

### Exit check

Give one reason to put a step in code rather than ask the model to “remember to do it.”

---

## Module 7 — Multi-agent collaboration

**Lesson question:** When do multiple agents improve a system instead of multiplying failure modes?

### Learning objectives

- Distinguish manager/worker, handoff, parallel specialists, and sequential pipeline patterns.
- Define ownership and typed input/output contracts for every specialist.
- Control shared state, fan-out, cost, latency, and conflicting answers.
- Build a small coordinator that calls specialist components and preserves provenance.

### Common topologies

| Pattern | Good fit | Main risk |
|---|---|---|
| Manager + tools/specialists | One coordinator owns user outcome | Manager becomes a bottleneck or silently drops a result |
| Handoff | A specialist takes responsibility for a subtask or conversation | User loses context or the handoff chain loops |
| Parallel specialists | Independent reviews can run concurrently | Conflicts, duplicated context, higher cost |
| Sequential pipeline | Each stage has a stable contract | Earlier errors propagate downstream |
| Shared blackboard/state | Agents need common case facts | Stale writes, privacy leakage, conflicting ownership |

Start with the fewest agents that meet a measurable need. Every additional model call creates more latency, cost, and opportunities for ungrounded output. Use a non-agent deterministic tool for a deterministic job.

### Coordination contract

A specialist result should have a clear schema, for example:

```json
{
  "specialist": "policy_reviewer",
  "status": "complete",
  "finding": "approval_required",
  "evidence_ids": ["POLICY-12#4"],
  "confidence": "medium",
  "limitations": ["policy effective date not verified"]
}
```

The manager must preserve disagreement and uncertainty. It should not average conflicting claims into a confident answer.

### Lab

```bash
python AgenticAI/labs/multi_agent_demo.py
```

The lab runs a research specialist and a safety reviewer through a coordinator. Study the typed findings and final merge. Then change the query and add a failure path.

### Exit check

Explain when an “agent as tool” pattern is preferable to handing the whole conversation to a specialist.

---

## Module 8 — LangGraph: explicit state and control flow

**Lesson question:** How can a graph make an agent's control flow inspectable and resumable?

### Learning objectives

- Represent an agent workflow as nodes, transitions, and shared typed state.
- Use conditional edges for routing and terminal states for completion/escalation.
- Understand checkpointing, retries, interrupts, and human approval as state transitions.
- Know when graph orchestration is more useful than an unbounded loop.

### Graph design

```text
START → classify → retrieve → evidence_check ── relevant ──► answer → END
                                │
                                ├─ weak, retry budget left → rewrite → retrieve
                                │
                                └─ external/high-risk → approval_or_escalation
```

A graph makes possible paths visible. The shared state should contain business facts, evidence references, and status—not a secret scratchpad. Checkpoints allow recovery; they do not make state automatically safe or correct. Version state schemas and define migration behavior.

### Framework-independent graph pseudocode

```python
state = {"question": question, "evidence": [], "retry_count": 0}

while True:
    state = classify(state)
    state = retrieve(state)
    state = check_evidence(state)

    if state["evidence_is_sufficient"]:
        return answer(state)
    if state["retry_count"] < 1:
        state = rewrite_query(state)
        continue
    return abstain_or_escalate(state)
```

The state transition and stop conditions are the learning objective. A runnable no-model-key implementation using the LangGraph Graph API is in [`labs/optional/langgraph_workflow.py`](labs/optional/langgraph_workflow.py): install `langgraph`, run the file, and compare the grounded and abstention paths. When adopting a particular LangGraph release, pin the version and use its current official `StateGraph`, checkpoint, interrupt, and streaming APIs.

### Production concerns

- Bound cycles and fan-out; set per-node timeouts.
- Make side-effect nodes idempotent.
- Store checkpoint access controls and retention deliberately.
- Distinguish retryable failures from permanent validation/authentication failures.
- Resume only after checking whether a side effect already completed.
- Include graph/node IDs and correlation IDs in traces.

### Exercise

Convert the invoice workflow from Module 6 into a graph. Add `NEEDS_HUMAN_APPROVAL`, `TOOL_FAILED`, and `COMPENSATING` states. Specify allowed transitions and terminal conditions.

---

## Module 9 — CrewAI: role- and task-oriented collaboration

**Lesson question:** When is a role/task abstraction the clearest way to express a team?

### Learning objectives

- Model collaborators by role, goal, constraints, available tools, and expected output.
- Write tasks with an explicit expected output and bounded context.
- Compare sequential and manager-led collaboration with graph orchestration.
- Evaluate whether adding a “crew” adds measurable quality or only extra calls.

### Decompose by responsibility, not job title

A weak design creates “researcher,” “writer,” and “critic” agents that all receive the entire prompt and repeat similar work. A stronger design gives each component a distinct contract:

- **Researcher:** return source passages and provenance; no unsupported synthesis.
- **Policy reviewer:** check a proposed action against specific policy clauses.
- **Writer:** produce user-facing text only from accepted findings.
- **Coordinator:** resolve disagreement, enforce stop conditions, and decide when to ask a human.

The course description names CrewAI as a framework to study. Framework APIs change; learn the transferable concepts first: role, goal, task, tools, process, context, memory, delegation, and output contract. Use the official documentation for the version installed in your lab rather than copying unpinned code from a course note.

A small optional sequential-crew example is in [`labs/optional/crewai_evidence_crew.py`](labs/optional/crewai_evidence_crew.py). It passes a fixed evidence excerpt to an analyst and a safety reviewer; it does not perform web search or execute actions. Run it only after installing CrewAI and configuring a model provider. Validate the result independently—the model's “review” is not a security control.

### Comparison exercise

Implement the same two-specialist task using:
1. A small Python coordinator (Module 7 lab).
2. A graph/state machine (Module 8 design).
3. A role/task crew.

Compare tool restrictions, failure recovery, trace visibility, testability, and cost. Choose the least complex option that meets the acceptance criteria.

---

## Module 10 — Model Context Protocol (MCP)

**Lesson question:** What does MCP standardize, and what remains the application's responsibility?

### Learning objectives

- Describe the host–client–server architecture.
- Distinguish tools, resources, and prompts.
- Explain why a transport and a protocol are different concerns.
- Integrate a remote capability without treating discovery as authorization.

### Architecture and primitives

```text
Host application ── MCP client ── JSON-RPC messages ── MCP server ── wrapped system
                                                      ├─ tools: callable actions
                                                      ├─ resources: contextual data
                                                      └─ prompts: reusable templates
```

MCP offers a common way for compatible applications to discover and communicate with server capabilities. Standard transports include stdio for a local subprocess and Streamable HTTP for network connections. A tool is an action, a resource is data/context, and a prompt is a template. Protocol revisions evolve; consult the current MCP specification when building an integration.

### Trust and deployment

- Treat tool schemas as contracts, not grants of authority.
- Authenticate the client and authorize each tool/resource operation.
- Apply least privilege and tenant scoping in the server or wrapped system.
- Protect remote endpoints with TLS, authentication, origin/network controls, and rate limits appropriate to deployment.
- Inspect tool outputs as untrusted data; keep secrets out of prompts, logs, and returned content.
- Confirm approval for consequential actions, even when a tool was discovered successfully.
- Pin/record protocol and SDK versions; test capability negotiation and error behavior.

### Runnable server lab

[`labs/optional/mcp_server.py`](labs/optional/mcp_server.py) uses the official Python MCP SDK to expose a safe calculation tool, a clearly labeled demo policy resource, and a review prompt over stdio. Install `mcp>=1.2.0` and configure an MCP-compatible client to launch it as a local subprocess. The server never issues a refund. For network deployment, do not simply change the transport: add authentication, authorization, TLS, origin/network controls, rate limits, and an operational threat review.

### Exercise

Design an MCP server exposing `search_policy` as read-only and `submit_refund` as a write operation. List separate authentication, authorization, input validation, approval, audit, and replay controls. Which primitive is each capability? Which actions must be hidden from a read-only role?

---

# Part IV — Production practice

## Module 11 — Safety, ethics, user experience, and evaluation

**Lesson question:** How do we know the system is helpful, safe, fair, and understandable?

### Learning objectives

- Threat-model prompt injection, data leakage, excessive authority, unsafe tools, and ungrounded answers.
- Design accessible interaction, correction, clarification, approval, and appeal paths.
- Build task-specific evaluation sets and evaluate tool trajectories as well as final text.
- Set launch criteria and monitor regressions after updates.

### A practical threat model

| Threat | Example | Control location |
|---|---|---|
| Prompt injection | Retrieved page says to reveal secrets | Treat content as untrusted; tool allowlists and data boundaries |
| Excessive agency | Model attempts a destructive write | Least privilege, action policy, human approval |
| Cross-tenant leakage | Retrieval returns another customer's record | Authorization filter before generation; database enforcement |
| Tool abuse | Model crafts arbitrary SQL/URL/shell | Narrow typed tools, allowlists, sandbox, validation |
| Memory poisoning | Malicious instruction persists as user memory | Provenance, write policy, review/delete, tenant boundary |
| Hallucinated citation | Source ID does not support the answer | Evidence-to-claim validation and citation tests |
| Cost/availability attack | Long loop or repeated calls | Budget, timeout, quota, iteration/fan-out limits |

### Human-centered UX

A trustworthy agent should:

- Say what it can and cannot do in plain language.
- Ask one useful clarifying question when required information is missing.
- Show evidence and action previews before high-impact changes.
- Make “cancel,” “edit,” and “talk to a person” discoverable.
- Distinguish completed actions from recommendations or drafts.
- Offer an explanation at the user's level without exposing hidden chain-of-thought or sensitive internal data.
- Support keyboard navigation, readable status, screen-reader labels, and clear error recovery.

### Copilots, product strategy, and adoption

A copilot is a product interaction pattern: the person remains visibly in control while the system drafts, recommends, retrieves, or prepares an action. “Copilot” does not automatically mean safe; a one-click approval can still hide a high-impact side effect. Make control visible in the workflow.

| Product question | Good starting point |
|---|---|
| Which task should we automate first? | Frequent, measurable, information-heavy work with a clear human fallback |
| Where should the human stay involved? | Ambiguous, sensitive, irreversible, or low-confidence decisions |
| How should adoption be introduced? | Shadow mode → opt-in pilot → measured expansion, with a rollback path |
| Which metric proves value? | Task outcome/time saved/error avoided, not only messages or tool calls |
| How do users build trust? | Show evidence, uncertainty, action previews, and a clear way to correct or escalate |

For go-to-market planning, state the buyer, end user, workflow owner, integration/data prerequisites, operating cost, risk controls, and measurable before/after outcome. Start with a narrow workflow wedge; do not sell “autonomy” without defining the action boundary and support model. Include training and change management for the people whose work changes.

### Evaluation stack

**Offline, before release**

- Unit tests for schemas, authorization, state transitions, and side effects.
- Golden task set covering routine, ambiguous, adversarial, and failure cases.
- Retrieval tests (recall@k, MRR, permission correctness, freshness).
- Tool tests (argument validity, authorization, idempotency, timeout behavior).
- Answer tests (groundedness, citation correctness, refusal quality, style/accessibility).
- Trajectory tests (right tool, right order, bounded steps, approval requested).

**Online, after release**

- Sampled human review with privacy controls.
- Tool success/error and escalation rates.
- Latency by model, retrieval, and tool.
- Token/model cost per completed task.
- Feedback, correction, and abandonment rates.
- Safety incident and policy violation review.

Use a release gate: a change does not ship merely because a few hand-picked prompts look good. Compare against a fixed test set, inspect regressions, and document accepted limitations.

### Exercise

Write five evaluation examples for a support-agent capstone: one normal, one ambiguous, one injection-in-retrieved-doc, one unauthorized tenant request, and one payment timeout. Define pass criteria before running the model.

---

## Module 12 — Deployment and LLMOps

**Lesson question:** How does a promising prototype become a service that can be operated responsibly?

### Learning objectives

- Design API boundaries, queues, state, secrets, telemetry, and deployment environments.
- Set service-level indicators for quality, availability, latency, and cost.
- Roll out model, prompt, index, and tool changes safely.
- Prepare an incident response and rollback path.

### Reference production design

```text
Client
  │ OIDC/JWT, request ID, quotas
  ▼
API gateway → request validation → orchestrator / durable workflow
                                  ├─ model gateway (timeouts, budgets, fallback)
                                  ├─ retrieval (ACL filters, versioned index)
                                  ├─ tool gateway (allowlist, auth, approval)
                                  ├─ state/memory (retention, encryption, deletion)
                                  └─ queue/workers (long tasks, retries, DLQ)

Telemetry: traces + metrics + redacted logs + audit trail
```

### Operational requirements

- **Configuration:** separate dev/staging/prod; store secrets in a secret manager; never commit keys.
- **Model gateway:** pin model/version when possible; set token, time, and cost budgets; define fallback behavior.
- **Retries:** retry only idempotent/transient failures; use jitter and an overall deadline.
- **Data:** encrypt, scope by tenant, minimize retention, document deletion and export paths.
- **Observability:** correlate request, graph run, model call, retrieval, and tool call IDs; redact sensitive content.
- **Rollout:** version prompts, tools, indexes, and workflow graphs; shadow/canary new versions; rollback independently.
- **Reliability:** define degraded behavior when model, vector store, or a tool is unavailable. Never fill missing external data with invented certainty.
- **Incident response:** disable risky tools, revoke credentials, preserve appropriate audit records, notify owners, and replay only after idempotency checks.

### Suggested SLOs (choose with the product owner)

Do not copy targets blindly. For the capstone, propose and justify:

- Completion rate for supported tasks.
- Evidence-backed answer rate and citation accuracy.
- Unauthorized-action rate (target: zero in test and production monitoring).
- p95 end-to-end latency for interactive tasks.
- Tool availability and error rate.
- Cost per successful task.
- Human escalation rate and time-to-resolution.

### Launch checklist

- [ ] User, tenant, and tool authorization are enforced outside the prompt.
- [ ] Tool schemas, ranges, and side effects are tested.
- [ ] Writes are idempotent and have approval where required.
- [ ] Retrieval applies access filters and returns provenance.
- [ ] Memory has retention, correction, and deletion policies.
- [ ] Prompt-injection and tool-abuse scenarios pass.
- [ ] Limits exist for time, steps, tokens, tools, and spend.
- [ ] Traces are useful and sensitive content is redacted.
- [ ] Rollback and kill switches are exercised.
- [ ] Product messaging accurately describes automation and human review.

---

## Module 13 — Capstone: an evidence-grounded support operations agent

### Scenario

Build an assistant for an internal service desk. It can search an approved runbook, look up a ticket, draft a response, and propose a ticket update. It must not perform high-impact writes without user or operator approval. If the runbook does not support a claim, it must say so.

### Required capabilities

1. **Grounded answer:** retrieve source passages, show source IDs, and abstain if evidence is missing.
2. **Tool loop:** invoke typed read tools; validate arguments; record observations.
3. **State:** retain ticket ID and pending action only for the active case; separate that state from durable memory.
4. **Workflow:** model `received`, `needs_clarification`, `ready_for_review`, `approved`, `executed`, `verified`, and `failed` states.
5. **Multi-agent option:** use a policy reviewer only if the evaluation shows improved correctness; preserve disagreements.
6. **MCP option:** expose a narrow read-only runbook or ticket capability; explicitly authorize each operation.
7. **Operations:** attach correlation IDs, bounded cost/time, retries, human escalation, and a rollback plan.

### Milestones

**A. Problem and policy** — Write the user story, supported scope, prohibited actions, and acceptance tests.  
**B. Offline baseline** — Run the deterministic labs; define tool and evidence contracts.  
**C. Retrieval** — Index a small approved corpus; evaluate source recall and access filtering.  
**D. Orchestration** — Add a bounded loop or graph with explicit terminal and approval states.  
**E. Safety and evaluation** — Add injection, permission, timeout, and no-evidence tests.  
**F. Operations review** — Present SLOs, cost model, traces, redaction, canary, kill switch, and rollback.

### Capstone rubric (100 points)

| Area | Points | Evidence required |
|---|---:|---|
| Problem framing and bounded autonomy | 10 | Scope, success criteria, prohibited actions |
| Architecture and control flow | 15 | Diagram, state/graph, termination, failure paths |
| Retrieval and grounding | 15 | Corpus provenance, metrics, citations, abstention |
| Tools and authorization | 15 | Schemas, least privilege, idempotency, approval |
| Memory and privacy | 10 | Data map, retention, deletion, tenant isolation |
| Safety and UX | 10 | Threat model, user confirmation, escalation/accessibility |
| Evaluation | 10 | Golden set, trajectory and regression results |
| Operations | 10 | SLOs, cost/latency, traces, rollout/rollback |
| Communication | 5 | Clear demo, known limitations, honest claims |

**Completion standard:** no critical authorization, tenant-isolation, or unapproved high-impact-action failures in the test set. A high total score cannot compensate for a critical safety failure.

---

# Instructor guide and learner support

## A 90-minute lesson template

- 0–10 min: learner story and diagnostic question.
- 10–25 min: concept explanation with one diagram.
- 25–40 min: worked example; instructor narrates decisions, not hidden chain-of-thought.
- 40–65 min: pair lab; learners change one thing and run tests.
- 65–78 min: failure injection and review.
- 78–87 min: each learner explains one trade-off and one safety boundary.
- 87–90 min: exit ticket and next lesson preview.

For a long workshop, repeat this cycle rather than delivering 90 minutes of uninterrupted slides. Offer a glossary, annotated diagrams, runnable commands, and an offline path for learners without cloud credentials.

## Glossary

- **Agent:** application that uses a model-driven or policy-driven loop to select bounded actions toward a goal.
- **Chain/workflow:** authored sequence of components with known control flow.
- **Tool/function calling:** structured model request for an application-defined operation; the application still executes and authorizes it.
- **RAG:** retrieval of relevant external knowledge into a model's context, with evidence and provenance.
- **Embedding:** numerical representation used for similarity search; not a factual database by itself.
- **Memory:** state retained for a defined future use; must have scope, provenance, and retention.
- **Orchestration:** control of model turns, tools, state, retries, and stopping.
- **MCP:** a protocol for compatible hosts/clients/servers to exchange tool, resource, and prompt capabilities.
- **Handoff:** transfer of control or responsibility to another agent.
- **Guardrail:** technical or procedural control that limits input, output, or action behavior.
- **Evaluation:** repeatable measurement of task outcomes, evidence, safety, cost, and latency.
- **LLMOps:** deployment, observation, evaluation, governance, and lifecycle management for model-powered systems.

## Final principle

A production agent is not “a clever prompt with tools attached.” It is a versioned software system with explicit authority, state, evidence, failure behavior, people, and measurable outcomes. Start small, make every boundary visible, and earn more autonomy with evidence.

## Source and implementation references

The lesson order is mapped to the topic sequence in the linked video description; no transcript or timestamped chapters were available, so this course does not claim exact chapter fidelity.

- [Reference video: Simplilearn Agentic AI Full Course](https://www.youtube.com/watch?v=CW01eBY9rGk)
- [Oracle University: Agentic AI Foundations learning-path overview](https://blogs.oracle.com/oracleuniversity/oracle-agentic-ai-foundations-training-certification-now-available)
- [LangGraph: Python quickstart](https://docs.langchain.com/oss/python/langgraph/quickstart)
- [CrewAI: Quickstart](https://docs.crewai.com/en/quickstart)
- [Model Context Protocol: Build an MCP server](https://modelcontextprotocol.io/docs/develop/build-server)
- [OpenAI Agents SDK](https://openai.github.io/openai-agents-python/)
- [OCI Enterprise AI Agents](https://docs.oracle.com/en-us/iaas/Content/generative-ai/agents.htm)
- [Oracle AI Database: AI Vector Search](https://docs.oracle.com/en/database/oracle/oracle-database/26/cncpt/artificial-intelligence-oracle-database.html)
