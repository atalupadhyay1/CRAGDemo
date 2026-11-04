# FDE Practice Set 1: Data Integration and ETL — Answer Key

**Keep this file closed until you have completed** [Set 1](set-1-data-integration-etl.md).

## Quick key

| Q1 | Q2 | Q3 | Q4 | Q5 | Q6 | Q7 | Q8 | Q9 | Q10 |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 **D** | 2 **D** | 3 **A** | 4 **D** | 5 **A** | 6 **A** | 7 **D** | 8 **C** | 9 **B** | 10 **D** |
| 11 **C** | 12 **D** | 13 **B** | 14 **D** | 15 **A** | 16 **B** | 17 **D** | 18 **D** | 19 **A** | 20 **D** |
| 21 **C** | 22 **A** | 23 **D** | 24 **A** | 25 **C** | 26 **A** | 27 **B** | 28 **B** | 29 **C** | 30 **C** |
| 31 **B** | 32 **B** | 33 **C** | 34 **D** | 35 **A** | 36 **A** | 37 **B** | 38 **D** | 39 **B** | 40 **C** |
| 41 **C** | 42 **C** | 43 **B** | 44 **B** | 45 **A** | 46 **B** | 47 **B** | 48 **D** | 49 **C** | 50 **A** |
| 51 **A** | 52 **D** | 53 **D** | 54 **C** | 55 **B** | 56 **B** | 57 **C** | 58 **B** | 59 **B** | 60 **D** |
| 61 **D** | 62 **A** | 63 **B** | 64 **C** | 65 **C** | 66 **C** | 67 **D** | 68 **D** | 69 **A** | 70 **C** |
| 71 **C** | 72 **D** | 73 **C** | 74 **B** | 75 **A** | 76 **B** | 77 **C** | 78 **A** | 79 **B** | 80 **D** |
| 81 **A** | 82 **C** | 83 **A** | 84 **B** | 85 **A** | 86 **C** | 87 **D** | 88 **C** | 89 **A** | 90 **A** |
| 91 **B** | 92 **D** | 93 **A** | 94 **A** | 95 **C** | 96 **D** | 97 **B** | 98 **B** | 99 **A** | 100 **C** |

## Explanations

### 1. Source discovery and requirements

1. **D** — Data meaning must be agreed with owners before a mapping can be trusted.
2. **D** — A contract makes changes visible and lets the pipeline fail clearly on incompatible input.
3. **A** — Representative profiling reveals skew, edge cases, and data-quality risks.
4. **D** — Source-qualified keys prevent collisions and remain stable across reprocessing.
5. **A** — Explicit null semantics and thresholds make data-quality behavior testable.
6. **A** — End-to-end freshness cannot exceed source availability without another supported change feed.
7. **D** — Incremental extraction must use a source field that advances when records change.
8. **C** — Approved samples enable early work without bypassing access controls or overstating validation.
9. **B** — Matching and survivorship policies govern how identities are reconciled.
10. **D** — Raw preservation plus explicit parsing distinguishes missing values from real numeric zeroes.

### 2. Extraction, pagination, and change capture

11. **C** — Cursor pagination must be followed to exhaustion and checkpointed for recovery.
12. **D** — A tie-breaker or safe overlap prevents equal-timestamp records from falling between runs.
13. **B** — CDC emits changes efficiently, but consumers still handle ordering, duplicates, schema, and access.
14. **D** — A coordinated snapshot boundary avoids gaps and double-count ambiguity between snapshot and CDC.
15. **A** — Arrival checks distinguish delayed data from a valid empty feed and avoid uncontrolled polling.
16. **B** — Coordinated throttling respects capacity while preserving visibility into lag.
17. **D** — Stable ordering and snapshot boundaries reduce omissions or repeats as the source changes.
18. **D** — Creation time does not indicate later updates unless the source explicitly changes it.
19. **A** — Explicit deletion events are needed to synchronize state and preserve audit requirements.
20. **D** — Short-lived credentials should be refreshed securely without losing extraction progress.

### 3. Batch, streaming, and event semantics

21. **C** — Event time or a source sequence represents source chronology better than processing completion order.
22. **A** — At-least-once delivery can repeat work, so the sink must be idempotent.
23. **D** — Deterministic boundaries make retries reproducible and prevent duplicate or missing partitions.
24. **A** — Watermarks bound how long the system waits for out-of-order event-time data.
25. **C** — A stable identity lets consumers deduplicate a producer retry safely.
26. **A** — Staging and atomic publication expose only validated complete output.
27. **B** — A shared snapshot avoids combining mutually inconsistent states.
28. **B** — Growing lag usually signals a capacity or partitioning imbalance between input and consumption.
29. **C** — Explicit identity and versioning let downstream systems distinguish updates from duplicates.
30. **C** — Key-based partitioning preserves per-entity order while allowing parallelism across keys.

### 4. Data quality and schema management

31. **B** — Missingness can be systematic and requires domain interpretation before imputation.
32. **B** — Unknown categories should be visible and handled deliberately, not silently coerced.
33. **C** — Uniqueness must be tested on the key that defines entity identity.
34. **D** — Additive optional fields can be introduced compatibly when contracts and readers are tested.
35. **A** — Decimal arithmetic and explicit currency/rounding avoid binary floating-point surprises.
36. **A** — Ambiguous dates need a known source convention; guessing can shift records by months.
37. **B** — Zero is a measured value; missing means unknown and must remain distinguishable.
38. **D** — Quarantine and evidence let the team distinguish bad data from an incorrect rule.
39. **B** — Explicit boundary validation prevents malformed values from corrupting downstream assumptions.
40. **C** — A collision shows the identifier's uniqueness assumption may not hold for this domain.

### 5. SQL, data modeling, and query reasoning

41. **C** — Window ranking selects a complete row; independent aggregates may pair values from different events.
42. **C** — A one-to-many join multiplies fact rows unless grain is handled deliberately.
43. **B** — A left join preserves unmatched left-side customers.
44. **B** — Null represents unknown and must be tested with `IS NULL` or `IS NOT NULL`.
45. **A** — A `WHERE` condition on the right side can turn a left join into inner-join behavior.
46. **B** — The key should represent the business grain: one customer at one snapshot date.
47. **B** — Distinct order identity or pre-aggregation avoids counting each order once per line.
48. **D** — Qualified references make the source of each field clear and prevent ambiguous-name errors.
49. **C** — A suitable index can support range filtering; the actual plan and workload must be measured.
50. **A** — Every selected value must be defined at the grouped grain or explicitly aggregated.

### 6. Python data processing

51. **A** — Streaming or chunking bounds memory use for large inputs.
52. **D** — Decimal values represent base-10 money more predictably than binary floats.
53. **D** — IEEE NaN equality is false, so specialized missing-value predicates are required.
54. **C** — Separate raw and transformed representations support traceability and replay.
55. **B** — Row-level quarantine gives operators actionable evidence without hiding partial failure.
56. **B** — A timeout can occur after a write committed; retries can duplicate effects without idempotency.
57. **C** — Encoding and normalization must be handled consistently without destroying meaningful characters.
58. **B** — Implicit local-time behavior can shift records and produce environment-dependent results.
59. **B** — `eval()` can execute code; typed parsing restricts the accepted input language.
60. **D** — Atomic publication separates incomplete work from a validated final artifact.

### 7. Orchestration, retries, and recovery

61. **D** — Boundary and pre-publication checks catch bad data before it spreads downstream.
62. **A** — Bounded retries mitigate transient failures without hiding persistent outages.
63. **B** — Explicit data-interval dependencies prevent incomplete or mismatched inputs.
64. **C** — Idempotent tasks and checkpointing make retries safe and focused.
65. **C** — Durable shared storage avoids assumptions about worker locality and lifetime.
66. **C** — Process completion alone does not establish that expected source data arrived.
67. **D** — Durable checkpoints support resumption without repeating or skipping work.
68. **D** — Reproducible dependencies and validation reduce unexpected parser behavior changes.
69. **A** — Readiness checks verify actual availability; elapsed time alone does not.
70. **C** — Run metadata makes retries auditable and reproducible.

### 8. Performance and scale

71. **C** — A hash/index lookup can reduce repeated linear scans; validate improvement with measurement.
72. **D** — Index order should reflect query predicates and be confirmed against real plans.
73. **C** — Incremental reads or replicas reduce impact while respecting source limits.
74. **B** — Hot-key skew limits parallelism; any repartitioning must preserve required semantics.
75. **A** — Bounded processing controls peak memory rather than merely masking the leak.
76. **B** — Batching reduces round trips while bounded transactions limit resource and lock impact.
77. **C** — Reusing a bounded lookup can reduce repeated work while preserving freshness guarantees.
78. **A** — Profiling reveals the actual bottleneck; scaling without diagnosis may multiply waste.
79. **B** — Snapshot or replica-based reads and controlled query pressure reduce interference with production writes.
80. **D** — Partitioning should support real access and retention patterns, not just ingestion convenience.

### 9. Governance, security, and privacy

81. **A** — Development use still needs purpose limitation, least privilege, and approved handling.
82. **C** — Secret management reduces exposure and supports access control and rotation.
83. **A** — Retention decisions must follow approved contractual and policy requirements.
84. **B** — Isolation must be enforced by the data platform, not by obscurity or user behavior.
85. **A** — Parameterization prevents user input from becoming executable SQL syntax.
86. **C** — Data lineage is needed to identify and process downstream copies consistently.
87. **D** — Telemetry can become a secondary sensitive-data store if payloads are logged indiscriminately.

### 10. Validation, lineage, and handoff

88. **C** — Layered tests cover logic, contracts, data edges, and full workflow behavior.
89. **A** — Lineage and run metadata make derived results explainable and reproducible.
90. **A** — Backfills can change business decisions, so impact and provenance must be explicit.
91. **B** — Job status should reflect the expected data interval and quality contract, not just process exit.
92. **D** — Mapping documentation links business meaning and implementation for future diagnosis.
93. **A** — Segmented reconciliation identifies the cause instead of hiding discrepancies.
94. **A** — Schema and data changes need tested recovery, not merely an application binary rollback.
95. **C** — Semantic changes can evade schema checks, so owner communication and invariant monitoring matter.
96. **D** — Threshold breaches should invoke an explicit containment and review policy.
97. **B** — Reproducibility depends on versioned inputs and execution configuration.
98. **B** — Coarse timestamps need a tie-breaker or change-log mechanism to avoid missed updates.
99. **A** — External data transfer requires authorization and data-minimization review.
100. **C** — Operational health combines data correctness, timeliness, reliability, cost, and ownership.

## References

These references are for further study; the questions are original and do not claim to reproduce the Udemy course's assessments.

- [Udemy course outline](https://www.udemy.com/course/forward-deployed-engineer-fde-practice-suite/)
- [PostgreSQL documentation](https://www.postgresql.org/docs/current/queries-table-expressions.html)
- [Apache Airflow concepts](https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/index.html)
- [The Twelve-Factor App: Config](https://12factor.net/config)
