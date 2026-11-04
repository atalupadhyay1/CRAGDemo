# Forward Deployed Engineer (FDE) — Practice Test A Answer Key

**Keep this file closed until you have completed** [`forward-deployed-engineer-practice-test.md`](forward-deployed-engineer-practice-test.md).

## Quick key

| Q | Answer | Q | Answer | Q | Answer | Q | Answer |
|---:|:---:|---:|:---:|---:|:---:|---:|:---:|
| 1 | B | 11 | C | 21 | C | 31 | C |
| 2 | C | 12 | A | 22 | A | 32 | D |
| 3 | A | 13 | D | 23 | C | 33 | B |
| 4 | D | 14 | B | 24 | B | 34 | A |
| 5 | B | 15 | A | 25 | D | 35 | C |
| 6 | A | 16 | C | 26 | C | 36 | B |
| 7 | C | 17 | D | 27 | A | 37 | D |
| 8 | A | 18 | B | 28 | B | 38 | C |
| 9 | D | 19 | A | 29 | D | 39 | A |
| 10 | B | 20 | D | 30 | A | 40 | B |

## Explanations

### 1. Customer problem framing and delivery

1. **B** — Start with the people doing the work. Observe the current workflow, the decisions they make, and the systems/evidence they use; then agree on a measurable baseline. A requested dashboard is a proposed solution, not yet a validated problem definition.
2. **C** — Resolve the success definition with the accountable owner and sponsor before optimizing. A primary outcome, baseline, acceptance criteria, and guardrails make trade-offs explicit and prevent teams from declaring success against incompatible measures.
3. **A** — A narrow vertical slice tests the whole workflow and value proposition without waiting for every integration. Representative approved data, an acceptance test, and a manual fallback make the pilot useful while containing delivery risk.
4. **D** — Different actions have different consequences. Low-risk credits can be bounded by explicit policy; ambiguous or high-impact credits need authorization and human review enforced by the application, not guessed by the model.
5. **B** — A blank is not evidence of “completed.” Confirm source semantics with the data owner, preserve uncertainty, and test mappings against real exceptions rather than silently converting or dropping records.
6. **A** — A written decision log and clear acceptance criteria give both sides a shared view of scope and trade-offs. This supports collaboration without promising incompatible work and dates or sacrificing testing invisibly.

### 2. Software engineering and integrations

7. **C** — Cursor pagination must be followed until the API signals completion. A safe checkpoint plus idempotent processing lets the import resume after interruption without skipping or duplicating work.
8. **A** — Webhooks are commonly delivered at least once. A durable idempotency key, recorded atomically with processing state, prevents duplicate deliveries from applying the same side effect twice.
9. **D** — Bounded retries with exponential backoff and jitter reduce load during transient failures. Retry only conditions that may recover, respect server guidance, and stop at a deadline; indefinite or indiscriminate retries can amplify an outage.
10. **B** — Long-running work belongs in a durable asynchronous job flow. Returning a job ID and status lets clients recover and observe progress; the worker must still handle retries safely.
11. **C** — Authentication identifies the caller, but the service must also authorize access to the specific object. A client-side check cannot protect a record if the server accepts an unauthorized identifier.
12. **A** — API contracts need deliberate compatibility rules. Tolerant clients and contract tests can make additive evolution safer; versioning is appropriate when a breaking change cannot be avoided.
13. **D** — A window function ranks rows within each device, so the query can return the complete newest event rather than independently aggregating columns. A deterministic tie-breaker makes equal timestamps reproducible.
14. **B** — HTTP 429 indicates rate limiting. Respect `Retry-After`, reduce request pressure, and monitor backlog rather than adding workers or misreporting the sync as complete.

### 3. Data, AI, and decision quality

15. **A** — Records from the same customer in both training and test sets can leak customer-specific patterns and overstate generalization. Split by the unit or time boundary that best represents deployment and reevaluate.
16. **C** — Authorization must constrain retrieval before protected content reaches the model or user. Prompting the model to choose the right tenant is not an access-control mechanism; tenant isolation should have explicit tests.
17. **D** — Retrieved text is data, not trusted control instructions. Keep system policy separate, and enforce tool permissions in application code even if model or document text asks otherwise.
18. **B** — A schema or constrained-output mode reduces formatting errors, but parsing and business validation are still required. Model-generated structure is a proposal, not trusted executable input.
19. **A** — A representative, versioned evaluation set measures errors against the intended task. Task-specific metrics, safety checks, and human review of ambiguous cases give stronger evidence than easy examples or model self-grading alone.
20. **D** — Without authorized evidence, the assistant should not guess or borrow another tenant’s data. It should make the limitation clear and offer a safe path to obtain authoritative information.
21. **C** — Validate the destination and permitted fields, then expose the proposed change for review. Authorization and approval belong in the system around the model; a prompt is not an adequate safeguard for consequential writes.

### 4. Deployment, reliability, and operations

22. **A** — A repeatable pipeline and production-like checks reduce deployment risk. Smoke/acceptance checks confirm the customer workflow, while a rollback plan provides a path to mitigate a bad release.
23. **C** — Build one versioned artifact and supply environment-specific settings and secrets through approved mechanisms. Baking secrets into images or silently using defaults creates security and configuration risks.
24. **B** — Correlated traces, logs, and metrics let engineers follow a request across service boundaries and see where latency or errors occurred. Sensitive payloads should not be dumped into logs.
25. **D** — In an active incident, reduce customer impact first while communicating and preserving evidence. Root-cause analysis follows mitigation; waiting or deleting logs makes recovery and learning harder.
26. **C** — Expand-and-contract supports deployments where old and new code overlap: add compatible schema, migrate readers/writers and data, verify, and remove obsolete schema only after it is safe.
27. **A** — A partial import should be observable and recoverable. Idempotency/checkpoints protect completed work, while quarantined rows and explicit status prevent silent data loss or false success.
28. **B** — Restricted environments require a deployment plan that respects customer controls, including approved offline artifacts and dependency provenance. Moving customer data to an unapproved environment bypasses those controls.
29. **D** — Alerts should prompt action on user-impacting symptoms and meaningful SLO/error-budget burn. Host-level noise can obscure real issues; an alert also needs enough workflow context to guide response.

### 5. Security, privacy, and governance

30. **A** — Use an approved secret-management system with scoped access and rotation. Source code, frontend bundles, logs, and broadly shared documents expose credentials and complicate revocation.
31. **C** — Check authorization, classification, contract terms, provider approval, and retention before sending data externally. Minimize or mask data and use an approved alternative when requirements are not met.
32. **D** — Tenant identity must come from a trusted authenticated context and be checked for each operation. A syntactically valid tenant ID supplied by a caller does not prove access.
33. **B** — Useful audit records answer who did what, to which target, when, and with what outcome, while controlled access and minimization protect sensitive information. Secrets and unnecessary full payloads should not be retained in logs.
34. **A** — Synthetic or appropriately de-identified data is the safer default for local development. Production data needs explicit approval, minimum necessary access, and a governed environment; removing one field alone may not prevent re-identification.
35. **C** — Follow the incident-response plan, contain access within assigned authority, notify the designated contacts, and preserve evidence. Deleting logs or delaying escalation can worsen impact and impede investigation.

### 6. Collaboration, communication, and product thinking

36. **B** — A bounded pilot with a baseline and representative users tests whether the workflow creates value and reveals safety or adoption issues. Usage counts alone do not show whether work improved.
37. **D** — A strong partner explains the risk without being obstructive and proposes the fastest safe path, including checks and rollback. Customer urgency does not erase operational controls or required approval.
38. **C** — A good handoff makes the system operable by the receiving team: ownership, architecture, access, alerts, recovery, limitations, and training matter alongside the code.
39. **A** — Breaking contracts require early coordination and a migration plan. Compatibility, versioning, and consumer tests reduce avoidable outages and give dependent teams time to adapt.
40. **B** — During an incident, communicate confirmed impact and mitigation, give a safe workaround if one exists, and set the next update time. Clearly separate verified facts from hypotheses.

## Self-review

Calculate the raw score for personal study, then review missed questions by section. This set has no official pass mark and is not a hiring prediction. A strong FDE interview or job performance also depends on hands-on coding, system design, customer communication, judgment under uncertainty, and the employer’s specific expectations.

## References for further study

These references inform the general skills and practices tested here; they do not define a universal FDE standard.

1. [Palantir — “Dev versus Delta: Demystifying engineering roles at Palantir”](https://blog.palantir.com/dev-versus-delta-demystifying-engineering-roles-at-palantir-ad44c2a6e87?gi=faa9514ca844) — one employer’s description of forward-deployed software engineering; role scope varies across organizations.
2. [The Twelve-Factor App — Config](https://12factor.net/config) — separation of deploy-specific configuration from code.
3. [Google SRE Book — Monitoring Distributed Systems](https://sre.google/sre-book/monitoring-distributed-systems/) and [Incident Response](https://sre.google/workbook/incident-response/) — monitoring and incident practices.
4. [OpenTelemetry — Observability primer](https://opentelemetry.io/docs/concepts/observability-primer/) — traces, metrics, and logs.
5. [OWASP API Security Top 10 (2023)](https://owasp.org/API-Security/editions/2023/en/0x11-t10/) — API authorization, resource-consumption, and integration risks.
6. [NIST AI Risk Management Framework](https://www.nist.gov/itl/ai-risk-management-framework) and [Generative AI Profile](https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-generative-artificial-intelligence) — AI risk governance and evaluation context.
