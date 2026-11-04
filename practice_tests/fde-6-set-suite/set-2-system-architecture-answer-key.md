# FDE Practice Set 2: System Architecture and Distributed Systems — Answer Key

**Keep this file closed until you have completed** [Set 2](set-2-system-architecture.md).

## Quick key

| Q1 | Q2 | Q3 | Q4 | Q5 | Q6 | Q7 | Q8 | Q9 | Q10 |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 **C** | 2 **B** | 3 **A** | 4 **B** | 5 **A** | 6 **C** | 7 **C** | 8 **D** | 9 **D** | 10 **B** |
| 11 **B** | 12 **D** | 13 **A** | 14 **B** | 15 **D** | 16 **A** | 17 **C** | 18 **B** | 19 **A** | 20 **A** |
| 21 **D** | 22 **A** | 23 **A** | 24 **B** | 25 **A** | 26 **D** | 27 **A** | 28 **D** | 29 **B** | 30 **D** |
| 31 **B** | 32 **D** | 33 **B** | 34 **B** | 35 **C** | 36 **C** | 37 **C** | 38 **B** | 39 **D** | 40 **D** |
| 41 **D** | 42 **D** | 43 **D** | 44 **C** | 45 **A** | 46 **C** | 47 **C** | 48 **A** | 49 **B** | 50 **C** |
| 51 **A** | 52 **B** | 53 **B** | 54 **C** | 55 **C** | 56 **C** | 57 **A** | 58 **D** | 59 **D** | 60 **B** |
| 61 **D** | 62 **C** | 63 **B** | 64 **C** | 65 **B** | 66 **C** | 67 **D** | 68 **A** | 69 **D** | 70 **D** |
| 71 **A** | 72 **D** | 73 **B** | 74 **A** | 75 **A** | 76 **A** | 77 **D** | 78 **A** | 79 **C** | 80 **C** |
| 81 **A** | 82 **D** | 83 **C** | 84 **B** | 85 **B** | 86 **D** | 87 **A** | 88 **B** | 89 **A** | 90 **C** |
| 91 **D** | 92 **C** | 93 **C** | 94 **C** | 95 **B** | 96 **A** | 97 **A** | 98 **C** | 99 **B** | 100 **B** |

## Explanations

### 1. Requirements and quality attributes

1. **C** — Architecture needs workload and quality-attribute requirements, not a vague scalability label.
2. **B** — Different latency objectives justify different paths and resource policies.
3. **A** — Network and control-plane constraints determine viable deployment architecture.
4. **B** — Recovery and consistency expectations shape storage and replication decisions.
5. **A** — A pilot should prove value while avoiding avoidable one-off coupling.
6. **C** — Operational burden and reversibility are part of architecture fitness.
7. **C** — Burst shape and service objectives determine capacity and buffering needs.
8. **D** — Resilience requires planned and tested failure-domain separation and recovery semantics.
9. **D** — A measurable SLO avoids ambiguous expectations and untestable promises.
10. **B** — Owned assumptions make uncertainty visible and guide validation before commitment.

### 2. Service boundaries and architecture patterns

11. **B** — Fixed workflows are easier to test and operate as explicit deterministic processes.
12. **D** — Service boundaries should align to cohesive capabilities and ownership, not arbitrary file or table counts.
13. **A** — Multiple writers create ambiguous authority and consistency problems.
14. **B** — Async handling or bounded waits prevent one slow dependency from indefinitely consuming request resources.
15. **D** — A single writer/owner reduces conflicting updates and clarifies contracts.
16. **A** — An adapter isolates unstable or inconsistent external models from the core domain.
17. **C** — An outbox couples committed state with eventual event delivery more reliably.
18. **B** — Workload isolation protects the transaction path while providing analytics access.
19. **A** — Distributed decomposition without independent boundaries may add complexity without the intended benefits.
20. **A** — Compatibility and observable deprecation reduce breakage for deployed consumers.

### 3. Consistency, ordering, and distributed state

21. **D** — Replica lag affects read consistency and user-visible behavior.
22. **A** — Version checks or transactions detect conflicting updates rather than overwriting silently.
23. **A** — Sagas model multi-service progress and recovery without a global transaction.
24. **B** — A timeout does not tell the client whether the original side effect committed.
25. **A** — A reliable source sequence resolves timestamp ties deterministically.
26. **D** — Fencing prevents a stale lock holder from writing after a newer owner takes over.
27. **A** — Cache correctness depends on explicit freshness and invalidation guarantees.
28. **D** — At-least-once delivery can redeliver after failures, so duplicate-safe processing is required.
29. **B** — Ordering scope is a trade-off between semantics and parallel throughput.
30. **D** — Read-your-writes can be supported without claiming all replicas are instantly consistent.

### 4. Resilience and failure containment

31. **B** — Timeouts and circuit breakers stop unbounded waiting and reduce cascading overload.
32. **D** — Bulkheads reserve capacity and prevent one workload from consuming every resource.
33. **B** — Nested equal timeouts can exceed the user deadline and waste resources after cancellation.
34. **B** — Permanent client errors are unlikely to recover through retries and can amplify load.
35. **C** — Stale-data fallback is safe only within an agreed freshness and communication contract.
36. **C** — Backlog diagnosis and bounded capacity changes avoid shifting overload to dependencies.
37. **C** — Jitter and budgets reduce retry storms and protect shared dependencies.
38. **B** — Liveness should detect a stuck process, while readiness should reflect ability to serve traffic.
39. **D** — Explicit partial state enables safe recovery and customer communication.
40. **D** — Planned degradation should preserve work and visibility without overwhelming an unavailable system.

### 5. Queues, caching, and asynchronous workflows

41. **D** — A long serial dependency chain inherits latency and availability risk from each dependency.
42. **D** — Outbox-style publication ties event delivery to committed state.
43. **D** — DLQ contents represent unprocessed work and need controlled diagnosis and replay.
44. **C** — Cache keys must preserve data-isolation boundaries; cache hits are not authorization.
45. **A** — Producers and consumers often upgrade independently, requiring compatibility during transition.
46. **C** — Duplicate submissions should map to one safe operation or be clearly represented.
47. **C** — Acknowledging before durable work creates a loss window.
48. **A** — Controlled asynchronous throughput protects the provider and makes partial failure visible.
49. **B** — Coalescing prevents a cache stampede while one result is being produced.
50. **C** — Asynchronous work needs explicit cancellation semantics and safe checkpoints.

### 6. Scaling and load balancing

51. **A** — Stateless instances can scale horizontally when shared state and dependencies are handled safely.
52. **B** — Readiness should indicate whether the instance should receive user traffic.
53. **B** — Externalized state supports balanced routing and instance replacement.
54. **C** — Scaling signals should represent the bottleneck that drives user-visible delay.
55. **C** — Scaling one tier can overload a downstream dependency unless capacity is coordinated.
56. **C** — Cold caches can create stampedes; staged warming and bounded misses reduce pressure.
57. **A** — Multi-region writes require explicit conflict and consistency design.
58. **D** — Tenant-aware budgets make fairness and isolation explicit.
59. **D** — Readiness prevents premature traffic while initialization is incomplete.
60. **B** — Bounded admission protects the service and communicates overload before cascading failure.

### 7. Storage, partitioning, and data ownership

61. **D** — Separate read models can protect transactional workloads while preserving source-of-truth ownership.
62. **C** — Sharding adds complexity and depends on key distribution and query/transaction behavior.
63. **B** — Asynchronous replicas may lag behind committed primary writes.
64. **C** — A transaction protects the all-or-nothing invariant within one database boundary.
65. **B** — Skew concentrates load and defeats the expected parallelism of partitioning.
66. **C** — Historical reconstruction requires retained versions/events, not only current state.
67. **D** — A backup is useful only if recovery is tested against expected objectives.
68. **A** — Shared storage still requires strong isolation at every access path.
69. **D** — Staged, bounded migrations reduce locks and support mixed application versions.
70. **D** — Data ownership and purpose should be clear before changing copies or retention.

### 8. Deployment, Kubernetes, networking, and restricted environments

71. **A** — Readiness controls traffic eligibility independently from process liveness.
72. **D** — Poorly scoped liveness checks can restart healthy processes during dependency degradation.
73. **B** — Memory pressure needs measurement and an evidence-based fix, not blind limit removal.
74. **A** — Artifact immutability with externalized configuration improves reproducibility and secret hygiene.
75. **A** — Air-gapped environments need preapproved, verifiable artifacts and an offline path.
76. **A** — Secrets leaked to source control require incident handling and credential rotation.
77. **D** — Layered network and identity checks isolate connectivity failures systematically.
78. **A** — Resource declarations and priority inform scheduling and contention behavior.
79. **C** — Versioned staged rollouts preserve a recovery path and an audit trail.
80. **C** — Deployments must honor customer egress controls and preserve transport security.

### 9. Observability, SLOs, and cost

81. **A** — Infrastructure health alone does not show whether users' work completes.
82. **D** — Context propagation connects spans into an end-to-end request trace.
83. **C** — The error budget quantifies tolerated unreliability under a defined SLO.
84. **B** — Unbounded label cardinality creates storage and query costs and can expose identifiers.
85. **B** — Tail percentiles reveal user pain hidden by averages.
86. **D** — Alert grouping reduces noise while retaining a useful signal for responders.
87. **A** — Cost reporting needs explicit, auditable allocation rules for shared resources.
88. **B** — SLOs connect operational alerts to user expectations and prioritize response.
89. **A** — Secrets in telemetry require containment and credential hygiene, not merely field renaming.
90. **C** — A cost investigation should follow workload and infrastructure evidence to identify changed drivers.

### 10. Security and architecture decision scenarios

91. **D** — Least privilege limits the impact of service compromise and mistakes.
92. **C** — External services can fail or change; contracts and resilience are still needed.
93. **C** — Network location alone is not an adequate substitute for security controls.
94. **C** — Active-active writes need an explicit consistency and conflict policy.
95. **B** — Decision records preserve why a choice was made and when it should be reconsidered.
96. **A** — Model-generated tool proposals must pass deterministic controls before side effects.
97. **A** — Shared storage can work, but coupling and operational boundaries must be deliberate.
98. **C** — A single critical dependency determines the availability floor unless mitigated.
99. **B** — Technology choices must be assessed against the customer's operational context and alternatives.
100. **B** — Load capacity does not prove safe degradation or recoverability during faults.

## References

These references are for further study; the questions are original and do not claim to reproduce the Udemy course's assessments.

- [Udemy course outline](https://www.udemy.com/course/forward-deployed-engineer-fde-practice-suite/)
- [Google SRE Book](https://sre.google/sre-book/table-of-contents/)
- [The Twelve-Factor App](https://12factor.net/)
- [Kubernetes concepts](https://kubernetes.io/docs/concepts/)
