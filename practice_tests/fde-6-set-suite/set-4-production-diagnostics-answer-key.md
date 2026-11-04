# FDE Practice Set 4: Production Diagnostics and Debugging — Answer Key

**Keep this file closed until you have completed** [Set 4](set-4-production-diagnostics.md).

## Quick key

| Q1 | Q2 | Q3 | Q4 | Q5 | Q6 | Q7 | Q8 | Q9 | Q10 |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 **B** | 2 **A** | 3 **B** | 4 **B** | 5 **D** | 6 **C** | 7 **C** | 8 **C** | 9 **A** | 10 **D** |
| 11 **B** | 12 **C** | 13 **A** | 14 **A** | 15 **C** | 16 **A** | 17 **A** | 18 **D** | 19 **B** | 20 **A** |
| 21 **D** | 22 **C** | 23 **A** | 24 **B** | 25 **C** | 26 **C** | 27 **C** | 28 **A** | 29 **C** | 30 **B** |
| 31 **B** | 32 **D** | 33 **C** | 34 **D** | 35 **B** | 36 **D** | 37 **D** | 38 **B** | 39 **B** | 40 **D** |
| 41 **D** | 42 **D** | 43 **D** | 44 **A** | 45 **A** | 46 **B** | 47 **B** | 48 **B** | 49 **A** | 50 **B** |
| 51 **B** | 52 **A** | 53 **D** | 54 **B** | 55 **C** | 56 **D** | 57 **B** | 58 **C** | 59 **B** | 60 **C** |
| 61 **A** | 62 **A** | 63 **D** | 64 **A** | 65 **D** | 66 **C** | 67 **B** | 68 **C** | 69 **D** | 70 **D** |
| 71 **B** | 72 **C** | 73 **A** | 74 **C** | 75 **A** | 76 **A** | 77 **C** | 78 **A** | 79 **D** | 80 **C** |
| 81 **C** | 82 **B** | 83 **A** | 84 **D** | 85 **B** | 86 **B** | 87 **D** | 88 **C** | 89 **A** | 90 **C** |
| 91 **B** | 92 **C** | 93 **A** | 94 **A** | 95 **D** | 96 **D** | 97 **C** | 98 **A** | 99 **D** | 100 **D** |

## Explanations

### 1. Triage and initial investigation

1. **B** — Impact and timeline establish priority and guide safe investigation.
2. **A** — A tenant-scoped failure often points to per-tenant data or configuration differences.
3. **B** — Incident response prioritizes impact reduction and evidence-based follow-up.
4. **B** — Correlation narrows hypotheses but must be checked against affected paths and telemetry.
5. **D** — Clock skew and timezone interpretation can distort incident timelines.
6. **C** — Reproduction needs the specific run inputs and a clear discrepancy.
7. **C** — Incident priority should reflect customer harm and operational risk.
8. **C** — Recovery actions must not introduce data loss or duplicate side effects.
9. **A** — Rates and segmentation distinguish increased traffic from degraded per-request reliability.
10. **D** — A shared record reduces duplicated work and preserves reasoning under pressure.

### 2. Logs, metrics, traces, and telemetry

11. **B** — Context propagation connects individual spans into one request path.
12. **C** — Safe context helps correlation without turning logs into a sensitive-data store.
13. **A** — Tail latency exposes slow requests hidden by averages.
14. **A** — High-cardinality labels are costly and may expose identity; metrics need bounded dimensions.
15. **C** — Absolute counts must be interpreted against request volume and SLO behavior.
16. **A** — Consistent time semantics are essential to correlate events across services.
17. **A** — Span breakdown directs investigation to the wait or work dominating the critical path.
18. **D** — Alerts should be actionable and tied to meaningful service risk.
19. **B** — Structured bounded diagnostics preserve usefulness without excessive or sensitive payloads.
20. **A** — User-workflow signals detect failures that process health cannot.

### 3. Network, identity, and protocol diagnosis

21. **D** — Hostname resolution occurs before a connection can reach the target service.
22. **C** — TLS handshake failures commonly involve certificates, trust, time, or protocol policy.
23. **A** — Authentication failures often follow token, scope, identity, or configuration changes.
24. **B** — 403 indicates authenticated access may be disallowed by authorization rules.
25. **C** — Environment-specific network controls can block a path that works elsewhere.
26. **C** — Resets can arise at multiple layers and need correlated timing/path evidence.
27. **C** — Browsers enforce origin and credential behavior that command-line clients do not.
28. **A** — If the app never received the request, the proxy/upstream path is a likely diagnostic boundary.
29. **C** — Renewal can fail if the new chain or mounted material is not trusted/reloaded.
30. **B** — DNS caching means clients may not observe a change at the same time.

### 4. Database and data-quality debugging

31. **B** — Plans and workload evidence locate scans, bad estimates, contention, or index mismatch.
32. **D** — Lock graphs and transaction ownership identify the blocking path.
33. **C** — Connection saturation requires coordinating pools and workload, not blindly adding clients.
34. **D** — One-to-many joins can duplicate facts and inflate aggregates.
35. **B** — Timezone and boundary errors often shift records across reporting dates.
36. **D** — Schema drift needs owner confirmation and a visible compatibility plan.
37. **D** — A network timeout does not reveal whether the transaction committed.
38. **B** — Asynchronous replication may temporarily serve older state.
39. **B** — Matching counts do not prove value correctness; reconcile measures and transformation logic.
40. **D** — Independent aggregates may come from different rows; select one coherent row by ordering.

### 5. Containers, deployment, and environment differences

41. **D** — Startup/config differences commonly explain local-production divergence.
42. **D** — Misconfigured probes can create restart loops during normal dependency slowness.
43. **D** — Architecture-specific native packages or image manifests can break portability.
44. **A** — Controlled workload comparison separates code/config changes from traffic variation.
45. **A** — Container identity and volume permissions determine write access.
46. **B** — Health/routing must distinguish startup from serving readiness.
47. **B** — Explicit config validation fails early without silently running with unsafe defaults.
48. **B** — Signed requests often rely on time windows, so clock skew can invalidate signatures.
49. **A** — Readiness gates traffic until an instance is safe to receive requests.
50. **B** — Restricted deployments need a policy-compliant and reproducible dependency path.

### 6. Distributed failures and queues

51. **B** — Depth alone can hide old or stuck work; age and partition detail reveal starvation.
52. **A** — Restart/redelivery requires duplicate-safe processing, not more retries.
53. **D** — Poison messages need containment so they do not block all progress.
54. **B** — Synchronized immediate retries amplify outages rather than containing them.
55. **C** — Step-level durable traces explain partial completion and guide safe recovery.
56. **D** — Low CPU with backlog often indicates waiting or constrained downstream resources.
57. **B** — Partition-level metrics can identify skew or a stuck consumer path.
58. **C** — Acknowledging too early removes the broker's ability to redeliver unfinished work.
59. **B** — Background cancellation needs cooperative worker checks and truthful job state.
60. **C** — Explicit scheduling policies protect urgent work while preventing starvation.

### 7. Performance and resource diagnosis

61. **A** — Profiles and correlated telemetry identify CPU work on the affected request path.
62. **A** — Memory profiles reveal leaks or unbounded caches better than guesswork.
63. **D** — Low resource utilization with latency often indicates waiting rather than computation.
64. **A** — Pool and query metrics distinguish leaks, slow work, and undersized capacity.
65. **D** — Bounded transfer and streaming reduce peak memory and bandwidth.
66. **C** — Targeted profiling supports a measured change to the actual hot path.
67. **B** — Nonlinear growth points to plan/complexity/skew issues that need workload-scale evidence.
68. **C** — Transfer-layer deadlines and resume semantics can cause repeated near-completion failures.
69. **D** — Evidence-led, policy-approved cleanup avoids destroying critical data.
70. **D** — Caches add overhead and failure modes; measure their actual effect and correctness.

### 8. Incident response and root cause

71. **B** — Defined roles coordinate response and communication under pressure.
72. **C** — Mitigation and root-cause correction are distinct and need separate tracking.
73. **A** — Risky changes need controlled authorization and a recovery plan even during urgency.
74. **C** — Blameless analysis seeks systemic improvements rather than personal fault alone.
75. **A** — Evidence-based timelines support accurate analysis and future prevention.
76. **A** — Clear, regular communication builds trust without making unsupported promises.
77. **C** — Users need a truthful account of all material impact, not one favorable metric.
78. **A** — Recovery includes data and customer validation plus owned follow-up work.
79. **D** — Specific, owned, testable actions are more likely to reduce recurrence.
80. **C** — Service process health does not prove customer operations have recovered.

### 9. Reproduction, testing, and isolation

81. **C** — A minimal reproducer isolates the triggering condition and supports regression tests.
82. **B** — Shape and skew often trigger failures that a small clean sample misses.
83. **A** — Bisecting or isolated toggles reduce the change set associated with the regression.
84. **D** — Tests must include relevant boundaries and the real integration contract.
85. **B** — Safe, versioned fixtures make bugs reproducible without exposing unnecessary production data.
86. **B** — Logging can change timing and resource use, masking race or concurrency bugs.
87. **D** — Controlled fault simulation and environment comparison isolate integration-only differences.
88. **C** — Flakiness is evidence of hidden nondeterminism, timing, or shared-state issues.
89. **A** — Reproduction should preserve diagnostic value while minimizing exposure.
90. **C** — Suite-only failures often come from leaked state or order/resource interactions.

### 10. Debugging case studies

91. **B** — The job treated absent input as a valid empty interval without checking the source contract.
92. **C** — Dependency latency likely entered the critical path and should be measured/contained.
93. **A** — Redelivery during restart is normal and must be safe through consumer/sink coordination.
94. **A** — Region-specific staleness often follows replication or routing differences.
95. **D** — Delivery failures may occur before the service handler or during receiver processing.
96. **D** — Daylight-saving transitions create ambiguous or shifted local-time intervals.
97. **C** — Per-stage evidence identifies whether source, volume, skew, or transform cost changed.
98. **A** — Horizontal scaling can amplify aggregate demand against a fixed shared limit.
99. **D** — Restart recurrence often indicates unpersisted state or initialization/configuration issues.
100. **D** — Recovery includes correcting data integrity safely, not only restoring process availability.

## References

These references are for further study; the questions are original and do not claim to reproduce the Udemy course's assessments.

- [Udemy course outline](https://www.udemy.com/course/forward-deployed-engineer-fde-practice-suite/)
- [Google SRE Book: Monitoring Distributed Systems](https://sre.google/sre-book/monitoring-distributed-systems/)
- [Google SRE Workbook: Incident Response](https://sre.google/workbook/incident-response/)
- [OpenTelemetry observability primer](https://opentelemetry.io/docs/concepts/observability-primer/)
