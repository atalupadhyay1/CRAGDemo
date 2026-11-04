# FDE Practice Set 3: API Design and Integration Patterns — Answer Key

**Keep this file closed until you have completed** [Set 3](set-3-api-design-integration.md).

## Quick key

| Q1 | Q2 | Q3 | Q4 | Q5 | Q6 | Q7 | Q8 | Q9 | Q10 |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 **B** | 2 **A** | 3 **A** | 4 **C** | 5 **D** | 6 **C** | 7 **C** | 8 **B** | 9 **A** | 10 **B** |
| 11 **C** | 12 **B** | 13 **C** | 14 **D** | 15 **B** | 16 **C** | 17 **A** | 18 **D** | 19 **B** | 20 **B** |
| 21 **C** | 22 **A** | 23 **D** | 24 **D** | 25 **B** | 26 **C** | 27 **D** | 28 **B** | 29 **A** | 30 **B** |
| 31 **C** | 32 **C** | 33 **B** | 34 **B** | 35 **A** | 36 **D** | 37 **C** | 38 **D** | 39 **D** | 40 **C** |
| 41 **D** | 42 **C** | 43 **C** | 44 **C** | 45 **A** | 46 **A** | 47 **A** | 48 **A** | 49 **B** | 50 **B** |
| 51 **C** | 52 **D** | 53 **D** | 54 **A** | 55 **B** | 56 **A** | 57 **C** | 58 **B** | 59 **D** | 60 **C** |
| 61 **A** | 62 **C** | 63 **B** | 64 **B** | 65 **C** | 66 **A** | 67 **D** | 68 **D** | 69 **D** | 70 **B** |
| 71 **A** | 72 **D** | 73 **D** | 74 **A** | 75 **B** | 76 **D** | 77 **B** | 78 **B** | 79 **D** | 80 **A** |
| 81 **D** | 82 **B** | 83 **D** | 84 **A** | 85 **D** | 86 **C** | 87 **A** | 88 **A** | 89 **A** | 90 **C** |
| 91 **C** | 92 **B** | 93 **B** | 94 **D** | 95 **A** | 96 **D** | 97 **A** | 98 **C** | 99 **C** | 100 **A** |

## Explanations

### 1. HTTP semantics and resource design

1. **B** — `201 Created` communicates resource creation and can identify the new resource.
2. **A** — PUT is defined as idempotent when it replaces the resource with the same state.
3. **A** — 202 indicates accepted processing without claiming completion.
4. **C** — 204 communicates successful processing with no response representation.
5. **D** — Entity tags and conditional requests support optimistic concurrency control.
6. **C** — Conditional requests can return not-modified without retransmitting an unchanged body.
7. **C** — Status codes let clients and observability distinguish success from authorization failure.
8. **B** — Resource-oriented endpoints use HTTP methods on stable resource paths.
9. **A** — Pagination bounds response size and resource consumption.
10. **B** — Clients need a consistent validation error contract without sensitive implementation details.

### 2. Authentication, authorization, and tenant isolation

11. **C** — URLs can leak into logs, histories, referrers, and monitoring systems.
12. **B** — Authentication alone does not grant access to every object.
13. **C** — Managed least-privilege workload credentials limit exposure and simplify rotation.
14. **D** — Client-provided identifiers are not proof of authorization.
15. **B** — Claims may outlive policy changes unless lifetimes and revocation are designed.
16. **C** — Separate scopes and audiences constrain token use to intended recipients and actions.
17. **A** — Authentication security includes transport, storage, abuse resistance, and lifecycle safeguards.
18. **D** — Client-side presentation does not enforce server-side function authorization.
19. **B** — Public exposure requires treating the credential as compromised and investigating use.
20. **B** — Distinguishable responses can reveal valid account identifiers to attackers.

### 3. Contracts, schemas, and versioning

21. **C** — Breaking changes need an explicit compatibility and consumer migration plan.
22. **A** — Optional additive fields can be compatible when client behavior is defined and tested.
23. **D** — OpenAPI provides a machine-readable contract for HTTP operations and schemas.
24. **D** — Timestamps need unambiguous representation and timezone rules.
25. **B** — Amount values are ambiguous without currency and precision semantics.
26. **C** — Stable codes support client logic without depending on human-readable wording.
27. **D** — Overloaded fields make validation and downstream interpretation unreliable.
28. **B** — Version coexistence needs explicit ownership and lifecycle policy.
29. **A** — Contracted semantics must be explicit; accidental ordering is brittle.
30. **B** — Numeric ranges are part of the contract and must match supported clients.

### 4. Pagination, filtering, and rate limits

31. **C** — Stable cursors or snapshots are less sensitive to inserts and deletes between pages.
32. **C** — Page tokens should not expose internals or allow tampering with query scope.
33. **B** — Server-enforced bounds protect resources from accidental or malicious oversized requests.
34. **B** — A limited query language prevents arbitrary input from becoming executable code.
35. **A** — Layered limits address abuse that can bypass a single identity dimension.
36. **D** — Respecting server guidance reduces pressure and avoids retry storms.
37. **C** — A snapshot boundary keeps pages consistent as underlying data changes.
38. **D** — Tenant authorization must be applied by the service, not delegated to client filters.
39. **D** — SQL identifiers require allowlisting because ordinary bind parameters do not bind column names.
40. **C** — Validators let clients avoid transferring representations that have not changed.

### 5. Idempotency, webhooks, and event delivery

41. **D** — Stable idempotency keys prevent duplicate side effects after ambiguous timeouts.
42. **C** — Signature verification authenticates message integrity before processing.
43. **C** — Prompt durable acknowledgement avoids unnecessary redelivery while preserving accepted work.
44. **C** — Eventual availability can be handled with durable pending state and bounded retries.
45. **A** — A key must identify one logical operation; payload mismatch is a conflict, not a new request.
46. **A** — Signatures, freshness, and deduplication address tampering and replay risks together.
47. **A** — Payment identity and event identity are different; versioning preserves legitimate updates.
48. **A** — Durable deduplication can make otherwise non-idempotent effects retry-safe.
49. **B** — Ordering guarantees and recovery rules must be explicit across both sides of the integration.
50. **B** — At-least-once delivery requires duplicate-safe processing across acknowledgement failures.

### 6. Synchronous, asynchronous, and integration patterns

51. **C** — An async job decouples long work from short-lived request connections.
52. **D** — Bounded dependency calls prevent the API from exhausting its own resources.
53. **D** — A controlled batch adapter respects the legacy interface while adding validation and auditability.
54. **A** — Pub/sub reduces direct coupling but does not remove delivery and security design.
55. **B** — Real-time is a service objective that needs measurable latency and failure semantics.
56. **A** — Change-driven mechanisms or adaptive polling can reduce cost and source load.
57. **C** — A job resource makes asynchronous work observable and recoverable to the client.
58. **B** — An adapter contains integration-specific translation and error handling.
59. **D** — Bounded parallel fan-out can reduce latency while preserving failure containment.
60. **C** — Bidirectional sync needs explicit conflict and echo-loop rules.

### 7. Validation, errors, and safe request handling

61. **A** — Authentication does not guarantee valid or permitted business input.
62. **C** — Explicit unknown-field behavior prevents accidental mass assignment and inconsistent clients.
63. **B** — Safe structured errors help clients fix input without exposing internals.
64. **B** — User-controlled URLs can coerce servers into accessing protected network destinations.
65. **C** — Resource limits protect availability; large transfers need a designed path.
66. **A** — Invalid values need explicit, consistent feedback rather than silent reinterpretation.
67. **D** — Partial-update semantics must distinguish omission from explicit clearing.
68. **D** — Correct HTTP status semantics let clients handle empty results and errors distinctly.
69. **D** — Correlation IDs support supportability without exposing sensitive implementation details.
70. **B** — Parser complexity limits prevent resource exhaustion from pathological payloads.

### 8. API security and abuse resistance

71. **A** — Access must be authorized for each object, not inferred from a guessable identifier.
72. **D** — Sensitive functions need server-side role/action checks.
73. **D** — Valid requests can abuse costly business flows without technical input errors.
74. **A** — Third-party data can be compromised or malformed and needs safe handling.
75. **B** — Endpoint inventory and lifecycle management reduce forgotten attack surface.
76. **D** — CORS is a browser policy and should not enable unintended credentialed cross-origin access.
77. **B** — URL fetching risks SSRF and malicious or oversized content.
78. **B** — Scope and lifecycle controls limit compromise impact.
79. **D** — Reset flows can reveal account existence and are susceptible to abuse.
80. **A** — URLs are broadly logged and propagated, making them poor containers for secrets.

### 9. Testing, documentation, and observability

81. **D** — Contract tests verify interface expectations between independently deployed teams.
82. **B** — The contract must reflect actual runtime behavior to support safe integration.
83. **D** — Mocks can diverge from real contracts, so boundary behavior needs integration validation.
84. **A** — Correlated signals reveal end-to-end behavior while avoiding sensitive payload logging.
85. **D** — Correlation and clear transient status help diagnose and recover without exposing internals.
86. **C** — Consumers need actionable migration guidance and a supported transition period.
87. **A** — Tests should verify enforcement and client-visible behavior without hiding the limit.
88. **A** — Segmented tail-latency data helps isolate the change and affected paths.
89. **A** — SDK consumers need reproducible versions and clear usage/compatibility guidance.
90. **C** — Recovery is assessed through workload, errors, latency, and resource saturation together.

### 10. Integration design scenarios

91. **C** — Integration choice depends on delivery guarantees and business freshness requirements.
92. **B** — Honest status and retry semantics preserve correctness and support recovery.
93. **B** — An adapter encapsulates protocol and semantic differences behind a stable interface.
94. **D** — A controlled export job bounds request resources and governs artifact access/retention.
95. **A** — Stable deduplication and reconciliation handle imperfect pagination or source behavior.
96. **D** — Consequential workflows need checks and durable state before executing side effects.
97. **A** — Outbound callbacks can create SSRF and data-exfiltration risks without destination controls.
98. **C** — Explicit field permissions prevent clients from setting protected object properties.
99. **C** — A bounded compatibility layer supports migration without ambiguous behavior.
100. **A** — Undocumented routes remain attack surface and require authorization and lifecycle controls.

## References

These references are for further study; the questions are original and do not claim to reproduce the Udemy course's assessments.

- [Udemy course outline](https://www.udemy.com/course/forward-deployed-engineer-fde-practice-suite/)
- [OWASP API Security Top 10 (2023)](https://owasp.org/API-Security/editions/2023/en/0x11-t10/)
- [RFC 9110: HTTP Semantics](https://www.rfc-editor.org/rfc/rfc9110.html)
- [OpenAPI Specification](https://spec.openapis.org/oas/latest.html)
