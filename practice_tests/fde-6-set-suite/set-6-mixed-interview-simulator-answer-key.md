# FDE Practice Set 6: Mixed FDE Interview Simulator — Answer Key

**Keep this file closed until you have completed** [Set 6](set-6-mixed-interview-simulator.md).

## Quick key

| Q1 | Q2 | Q3 | Q4 | Q5 | Q6 | Q7 | Q8 | Q9 | Q10 |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 **A** | 2 **C** | 3 **C** | 4 **C** | 5 **D** | 6 **A** | 7 **C** | 8 **A** | 9 **C** | 10 **B** |
| 11 **D** | 12 **B** | 13 **B** | 14 **B** | 15 **D** | 16 **A** | 17 **D** | 18 **D** | 19 **B** | 20 **A** |
| 21 **B** | 22 **D** | 23 **B** | 24 **C** | 25 **B** | 26 **D** | 27 **D** | 28 **D** | 29 **B** | 30 **B** |
| 31 **A** | 32 **B** | 33 **B** | 34 **C** | 35 **D** | 36 **B** | 37 **A** | 38 **D** | 39 **A** | 40 **C** |
| 41 **B** | 42 **D** | 43 **D** | 44 **B** | 45 **B** | 46 **A** | 47 **C** | 48 **D** | 49 **A** | 50 **D** |
| 51 **C** | 52 **C** | 53 **C** | 54 **B** | 55 **D** | 56 **C** | 57 **C** | 58 **B** | 59 **C** | 60 **B** |
| 61 **C** | 62 **A** | 63 **A** | 64 **C** | 65 **A** | 66 **B** | 67 **D** | 68 **C** | 69 **C** | 70 **A** |
| 71 **A** | 72 **A** | 73 **D** | 74 **D** | 75 **A** | 76 **A** | 77 **B** | 78 **D** | 79 **B** | 80 **A** |
| 81 **D** | 82 **A** | 83 **C** | 84 **C** | 85 **C** | 86 **D** | 87 **D** | 88 **A** | 89 **A** | 90 **B** |
| 91 **A** | 92 **C** | 93 **B** | 94 **A** | 95 **A** | 96 **D** | 97 **B** | 98 **C** | 99 **D** | 100 **C** |

## Explanations

### 1. Integrated data-ingestion case

1. **A** — Stable identity and observable freshness make redelivery and delay safe to manage.
2. **C** — A defined snapshot/change boundary prevents gaps and duplicate state during concurrent loads.
3. **C** — Correct identity is a domain contract, not a guess from column order.
4. **C** — Process success must reflect data-quality/completeness policy.
5. **D** — Explicit boundary handling prevents silent corruption and localizes source drift.
6. **A** — Segmented reconciliation finds the cause instead of concealing the discrepancy.
7. **C** — Bounded processing and checkpoints control memory and support recovery.
8. **A** — Deletion obligations apply across derived copies and need lineage.
9. **C** — Honest freshness reporting helps customers decide safely while recovery proceeds.
10. **B** — A deterministic version rule preserves the newest authoritative state across concurrent paths.

### 2. API and service design case

11. **D** — Idempotency plus durable identity makes ambiguous retries safe and observable.
12. **B** — An adapter and contract tests isolate external schema changes.
13. **B** — Each object access must be authorized in the trusted service boundary.
14. **B** — Async jobs handle long work and make retries/status and artifact access governable.
15. **D** — Server-side callbacks can reach unintended destinations unless constrained.
16. **A** — Partial update behavior must distinguish omission from explicit clearing/replacement.
17. **D** — Correct status semantics help clients handle access failures while following disclosure policy.
18. **D** — Compatibility must be verified rather than assumed.
19. **B** — Client UI controls cannot replace server-side duplicate protection.
20. **A** — Server-side property allowlists constrain what callers can change.

### 3. Architecture and distributed-systems case

21. **B** — Bounded resource use prevents a dependency fault cascading into total service failure.
22. **D** — A saga models progress and recovery across independently committed services.
23. **B** — Low CPU with old messages suggests waiting or uneven/stuck processing.
24. **C** — Cache consistency depends on explicit freshness semantics and invalidation.
25. **B** — Safe repartitioning addresses skew without breaking ordering or identity semantics.
26. **D** — Failover trade-offs depend on RPO/RTO and actual replicated state.
27. **D** — Horizontal scaling multiplies per-process resources unless globally budgeted.
28. **D** — Read-your-writes can be honored without assuming asynchronous replicas are current.
29. **B** — Coordinated retry controls reduce load amplification during recovery.
30. **B** — The required ordering scope determines architecture and throughput trade-offs.

### 4. SQL, Python, and data reasoning case

31. **A** — Grain-aware aggregation avoids counting each order once per line.
32. **B** — Row ranking keeps status and timestamp from the same event.
33. **B** — Streaming avoids memory proportional to the entire file size.
34. **C** — Explicit timezone rules eliminate environment-dependent conversions.
35. **D** — NaN is not equal to itself under standard floating-point semantics.
36. **B** — Identifiers cannot be safely bound as ordinary values and need an allowlist.
37. **A** — Unknown and measured zero have different business meanings.
38. **D** — Fixed decimal rules prevent precision drift in financial totals.
39. **A** — Observable quarantine protects downstream users from hidden data loss.
40. **C** — Tie-breakers or overlap prevent changes sharing a timestamp from being skipped.

### 5. Deployment and customer environment case

41. **B** — Restricted deployment changes dependency, trust, and networking assumptions.
42. **D** — Readiness controls routing separately from whether the process is alive.
43. **D** — Expand-and-contract supports mixed versions and recovery.
44. **B** — Secrets embedded in images can be extracted and must be rotated.
45. **B** — Correct least-privilege file permissions solve access without broadening runtime privilege.
46. **A** — Supply-chain controls still apply in restricted environments.
47. **C** — Staged rollout and explicit gates enable early detection and controlled rollback.
48. **D** — Early config validation avoids unsafe partial startup.
49. **A** — Application rollback alone cannot reverse incompatible persistent-state changes.
50. **D** — SBOM/provenance support security review and traceability of deployed artifacts.

### 6. Production investigation case

51. **C** — Time-correlated operational dependencies narrow the failure window.
52. **C** — Health must reflect the actual workflow users need to complete.
53. **C** — Correlation guides investigation and impact-based mitigation, not unsupported certainty.
54. **B** — Query plans and workload evidence identify scale-related database bottlenecks.
55. **D** — Server-guided rate limiting avoids amplifying pressure.
56. **C** — Restart redelivery is expected; the processing boundary must prevent duplicate effects.
57. **C** — Timeout leaves the outcome ambiguous; stable operation identity resolves it safely.
58. **B** — Regional date differences commonly arise from implicit timezone boundaries.
59. **C** — Stable depth can still hide old work that is not progressing.
60. **B** — Service recovery does not prove data integrity; reconciliation remains necessary.

### 7. AI and decision-support case

61. **C** — Access control must constrain retrieved data before it reaches the model.
62. **A** — Retrieved content must not override policy or grant capabilities.
63. **A** — Evidence gaps must prevent unsupported consequential action.
64. **C** — Model output is untrusted input and must pass deterministic controls.
65. **A** — Curated easy examples do not establish production generalization or safety.
66. **B** — Degraded-mode behavior should protect users and communicate uncertainty.
67. **D** — Grounded systems should abstain when evidence is unavailable.
68. **C** — Oversight works only when humans can assess and act on meaningful evidence.
69. **C** — External processing needs governed data handling before transfer.
70. **A** — Cohort analysis can reveal harms hidden by overall averages.

### 8. Security, privacy, and governance case

71. **A** — Client input cannot establish authorization authority.
72. **A** — Logged secrets require incident handling and credential rotation.
73. **D** — Local development does not exempt data from privacy and access policy.
74. **D** — External responses are untrusted inputs and need the same safe query construction.
75. **A** — External transfer needs governance and data minimization.
76. **A** — Temporary access should be scoped, approved, traceable, and removed.
77. **B** — Data locality includes copies and processing paths beyond the main database.
78. **D** — SSRF controls constrain where the server can make outbound requests.
79. **B** — Auditability must be balanced with data minimization and retention policy.
80. **A** — Demonstrations should preserve access policy and use safe data.

### 9. Customer trade-offs and delivery decisions

81. **D** — Estimates should reflect uncertainty and include a way to resolve it.
82. **A** — Risk-tiered autonomy balances speed with operational controls.
83. **C** — Reuse may satisfy the need while reducing maintenance, but fit should be verified.
84. **C** — Balanced evaluation avoids cherry-picking a favorable outcome.
85. **C** — Explicit trade-offs allow the accountable owner to prioritize responsibly.
86. **D** — Feedback should guide workflow fit and adoption, not be dismissed.
87. **D** — Approval authority must be explicit, especially for security-sensitive work.
88. **A** — Reliability can be engineered and measured, but not honestly guaranteed as absolute perfection.
89. **A** — A demo is not enough evidence for broad operational readiness.
90. **B** — Clear uncertainty and regular updates maintain trust during investigation.

### 10. Integrated interview prompts

91. **A** — Problem framing establishes what value and constraints the design must serve.
92. **C** — Time semantics are a domain contract and should be agreed and tested.
93. **B** — Reliability is about user outcomes, not only infrastructure availability.
94. **A** — Safe discovery and an adapter reduce risk from unknown legacy semantics.
95. **A** — A controlled pilot can deliver learning without overstating data reliability.
96. **D** — Incident context can change release risk and requires explicit decision authority.
97. **B** — Invalid model-generated tool arguments must not bypass application validation.
98. **C** — A tested owner and runbook make the deployment sustainable after handoff.
99. **D** — Trade-offs require transparent evidence and an accountable business decision.
100. **C** — FDE success combines engineering quality with measurable, safe, lasting customer value.

## References

These references are for further study; the questions are original and do not claim to reproduce the Udemy course's assessments.

- [Udemy course outline](https://www.udemy.com/course/forward-deployed-engineer-fde-practice-suite/)
- [Google SRE Book](https://sre.google/sre-book/table-of-contents/)
- [OWASP API Security Top 10 (2023)](https://owasp.org/API-Security/editions/2023/en/0x11-t10/)
- [NIST AI Risk Management Framework](https://www.nist.gov/itl/ai-risk-management-framework)
