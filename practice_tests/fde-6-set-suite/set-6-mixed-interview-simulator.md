# FDE Practice Set 6: Mixed FDE Interview Simulator

**Format:** 100 original, single-best-answer questions  
**Suggested time:** 150 minutes (a self-imposed pacing target)  
**Scoring:** 1 point per question; raw percentage = `correct ÷ 100 × 100`.

> Unofficial study material based on the Udemy course's public topic outline, not its paid questions or assignments. FDE roles and interview formats vary by employer. This set is not endorsed by Udemy or an employer and is not a hiring prediction.

**Instructions:** Choose one best answer for each question. Complete this file before opening the [separate answer key](set-6-mixed-interview-simulator-answer-key.md).

## Answer sheet

| Q | Answer | Q | Answer | Q | Answer | Q | Answer | Q | Answer |
|---:|:---:|---:|:---:|---:|:---:|---:|:---:|---:|:---:|
| 1 | ____ | 2 | ____ | 3 | ____ | 4 | ____ | 5 | ____ |
| 6 | ____ | 7 | ____ | 8 | ____ | 9 | ____ | 10 | ____ |
| 11 | ____ | 12 | ____ | 13 | ____ | 14 | ____ | 15 | ____ |
| 16 | ____ | 17 | ____ | 18 | ____ | 19 | ____ | 20 | ____ |
| 21 | ____ | 22 | ____ | 23 | ____ | 24 | ____ | 25 | ____ |
| 26 | ____ | 27 | ____ | 28 | ____ | 29 | ____ | 30 | ____ |
| 31 | ____ | 32 | ____ | 33 | ____ | 34 | ____ | 35 | ____ |
| 36 | ____ | 37 | ____ | 38 | ____ | 39 | ____ | 40 | ____ |
| 41 | ____ | 42 | ____ | 43 | ____ | 44 | ____ | 45 | ____ |
| 46 | ____ | 47 | ____ | 48 | ____ | 49 | ____ | 50 | ____ |
| 51 | ____ | 52 | ____ | 53 | ____ | 54 | ____ | 55 | ____ |
| 56 | ____ | 57 | ____ | 58 | ____ | 59 | ____ | 60 | ____ |
| 61 | ____ | 62 | ____ | 63 | ____ | 64 | ____ | 65 | ____ |
| 66 | ____ | 67 | ____ | 68 | ____ | 69 | ____ | 70 | ____ |
| 71 | ____ | 72 | ____ | 73 | ____ | 74 | ____ | 75 | ____ |
| 76 | ____ | 77 | ____ | 78 | ____ | 79 | ____ | 80 | ____ |
| 81 | ____ | 82 | ____ | 83 | ____ | 84 | ____ | 85 | ____ |
| 86 | ____ | 87 | ____ | 88 | ____ | 89 | ____ | 90 | ____ |
| 91 | ____ | 92 | ____ | 93 | ____ | 94 | ____ | 95 | ____ |
| 96 | ____ | 97 | ____ | 98 | ____ | 99 | ____ | 100 | ____ |

---

## 1. Integrated data-ingestion case

### 1.

A shipment feed is late and sometimes redelivers the same record. Which first-version design is strongest?

A. Persist source identity/version, use idempotent upserts, track freshness, and expose late/duplicate counts.  
B. Ignore timestamps and overwrite randomly.  
C. Mark the feed fresh whenever the scheduler starts.  
D. Append every delivery as a new shipment.  

### 2.

The customer needs to backfill two years while live updates continue. What should be coordinated?

A. Stop all source writes indefinitely without approval.  
B. Load both streams with no deduplication.  
C. A consistent snapshot boundary, CDC/start position, bounded backfill, and reconciliation before cutover.  
D. Start live CDC after the backfill with no shared boundary.  

### 3.

A source uses a composite key that is not documented. What should the FDE do?

A. Use the first column as the key by convention.  
B. Generate a random key on every import.  
C. Confirm identity semantics with the owner and test uniqueness/stability before selecting a target key.  
D. Deduplicate only by display name.  

### 4.

A daily import has 3% rejected rows, but the dashboard is published automatically. What is the risk?

A. The dashboard will infer missing rows.  
B. Rejected rows always improve correctness.  
C. Partial data may be mistaken for complete; define reject thresholds, quarantine, and publish-state rules.  
D. The scheduler's success means every record loaded.  

### 5.

A source field changes type from integer to string mid-file. What should the ingestion boundary do?

A. Ask the UI to infer the value.  
B. Remove type checking for all feeds.  
C. Convert every malformed value to zero silently.  
D. Validate types, preserve offending examples safely, and quarantine or convert only under an explicit rule.  

### 6.

A warehouse total differs from source by 1.5%. What is the best investigation?

A. Reconcile by date/key/status and inspect filters, duplicates, rejects, and transformation grain.  
B. Add 1.5% to every output value.  
C. Change the dashboard query until totals match.  
D. Ignore it if the chart looks smooth.  

### 7.

The initial load is too large for memory. What design should be used?

A. Split files randomly and discard partition metadata.  
B. Raise memory limits without measuring.  
C. Stream or process bounded partitions, checkpoint progress, and publish validated batches safely.  
D. Load the full data set into one process list.  

### 8.

A customer requests historical deletion propagation. What must be traced?

A. Raw, staged, transformed, cached, exported, and downstream copies under the retention/deletion policy.  
B. Only the source table name.  
C. The UI route and button label only.  
D. Nothing once data is hashed.  

### 9.

A pipeline's freshness SLO is missed after a partner API slowdown. What should be communicated?

A. Hide the lag metric until it recovers.  
B. Claim the data is current because the job ran.  
C. Measured lag/impact, dependency status, mitigation, and the next update or recovery checkpoint.  
D. Blame the partner without evidence.  

### 10.

A backfill and live stream both update the same target records. What prevents stale backfill rows overwriting newer live state?

A. Disable the live stream during every backfill with no plan.  
B. Version/event-time-aware merge rules and a defined precedence for late writes.  
C. Store updates in arbitrary order.  
D. Let whichever process finishes last win.  

## 2. API and service design case

### 11.

A new client needs to create a work order and safely retry after timeout. What should the API support?

A. An unprotected database connection string.  
B. A success response before persistence.  
C. A non-idempotent endpoint with no request identity.  
D. Authenticated creation with idempotency key, validation, canonical result, and traceable operation ID.  

### 12.

A partner's response schema changes without notice. What design helps contain impact?

A. Spread partner field names through every service.  
B. Versioned/validated adapter contract, tolerant handling for additive fields, alerting, and compatibility tests.  
C. Parse by byte offset and assume no future changes.  
D. Disable integration errors.  

### 13.

A request accesses `/tenants/{id}/records/{id}`. What is mandatory beyond authentication?

A. Client-side hiding of other tenant IDs only.  
B. Server-side tenant and object-level authorization for the requested record.  
C. A longer URL path.  
D. An unbounded request limit.  

### 14.

A large export takes minutes and may be retried. Which API pattern fits?

A. Hold a request open indefinitely with no status.  
B. Durable async job with status/result, idempotent submission, bounded artifact access, and expiry.  
C. Return the entire export in a query string.  
D. Copy data to a public bucket.  

### 15.

A callback endpoint is customer-configurable. Which risk must be addressed?

A. Whether the callback is called synchronously or asynchronously only.  
B. The URL's capitalization.  
C. Only CSS injection in the callback name.  
D. SSRF/data exfiltration; validate destination, egress, authentication, signing, and retry behavior.  

### 16.

A client asks to PATCH `status` but omit all other fields. What semantics should be specified?

A. Omitted fields remain unchanged; explicit null/clear behavior is separately defined and authorized.  
B. Every PATCH replaces the entire object silently.  
C. Omitted fields always become zero.  
D. The server picks random defaults.  

### 17.

A route returns 403 for both missing authentication and forbidden access. What is the concern?

A. The route cannot use JSON.  
B. 403 always means success.  
C. The API should return database credentials.  
D. It obscures useful client behavior; distinguish authentication and authorization outcomes per security policy.  

### 18.

A new optional field is added to a public response. What should release testing include?

A. A guarantee every parser ignores unknown fields.  
B. Removing all old clients from inventory.  
C. Only a test of the field's display color.  
D. Old-client compatibility and contract tests for current supported versions.  

### 19.

A payment API request is sent twice after a timeout. What should be used?

A. A one-second sleep with no key.  
B. A stable idempotency key persisted atomically with the payment operation/result.  
C. A client-side button disable only.  
D. A new random key for each retry.  

### 20.

A request body includes unexpected writable fields. What prevents mass assignment?

A. Explicit writable-property allowlist and field-level authorization on the server.  
B. Deserialize directly into every database column.  
C. Hide fields in the UI only.  
D. Trust the model to remove protected properties.  

## 3. Architecture and distributed-systems case

### 21.

A dependency outage causes requests to pile up and exhaust threads. What changes help?

A. Add synchronous calls to more dependencies.  
B. Tight deadlines, circuit breaker, bounded concurrency/queue, and a defined degraded response.  
C. Remove all timeouts.  
D. Infinite retries and waits.  

### 22.

Two systems need to coordinate a multi-step business action without a global transaction. What pattern fits?

A. Assume one database transaction spans both systems.  
B. Retry forever without recording completed steps.  
C. Hide partial completion.  
D. Saga/workflow with durable state, compensations, idempotency, and observable step outcomes.  

### 23.

A queue's oldest message age rises while CPU remains low. What should be checked?

A. Only CPU limits.  
B. Blocked I/O, downstream quota, partition skew, consumer assignment, and poison messages.  
C. The service's page title.  
D. Whether the messages use uppercase text.  

### 24.

A cache returns stale data after a write. What is needed?

A. Infinite cache TTL.  
B. A larger cache cluster only.  
C. Freshness/invalidation contract, read-your-writes behavior if required, and fallback on invalidation failure.  
D. A different logo for the cache.  

### 25.

A hot key overwhelms one partition. What should be evaluated?

A. Randomly mutate keys every request.  
B. Whether key distribution can be refined safely while preserving required per-entity ordering.  
C. Drop events for the hot customer.  
D. Add workers to the same single-threaded partition only.  

### 26.

A region fails and the secondary is available but several minutes behind. What should the incident owner decide from?

A. A guarantee that replication is always current.  
B. The secondary region's dashboard color.  
C. Whether the customer prefers a shorter region name.  
D. Recovery objectives, data-loss tolerance, replication state, and approved failover policy.  

### 27.

A deployment is scaled out, then the database reports connection exhaustion. What is likely?

A. More application instances always reduce connections.  
B. The database has no connection limit.  
C. The new instances changed DNS record casing.  
D. Per-instance pools multiplied beyond database capacity; coordinate pool/concurrency budgets.  

### 28.

A transaction must be read immediately after commit, but replicas lag. What is an option?

A. Remove the primary database.  
B. Return a random replica result.  
C. Wait for an unspecified duration and assume catch-up.  
D. Route the session to the primary or provide a session-consistent read path for that operation.  

### 29.

A retry storm occurs after a network outage. What should be adjusted?

A. Unlimited retry nesting.  
B. Exponential backoff/jitter, retry budgets, deadlines, and circuit breaking across layers.  
C. Synchronized retries with shorter intervals.  
D. Disable rate limits.  

### 30.

A feature requires global event order, but throughput is inadequate. What should be clarified?

A. That adding consumers guarantees a single global order.  
B. Whether per-entity ordering is sufficient; global ordering imposes a significant parallelism constraint.  
C. That event order never matters.  
D. That messages should be discarded.  

## 4. SQL, Python, and data reasoning case

### 31.

A SQL join doubles a count of orders because each order has several lines. What is the fix?

A. Aggregate at order grain or count distinct order IDs after validating the intended relationship.  
B. Remove the join condition.  
C. Count joined rows and call them orders.  
D. Add the order ID twice.  

### 32.

A query must find the latest status row per ticket. What approach returns a coherent row?

A. Independently take `MAX(timestamp)` and `MAX(status)`.  
B. Rank rows per ticket by event timestamp and tie-breaker, then select rank one.  
C. Count rows by status only.  
D. Use alphabetical status order.  

### 33.

A Python job reads an 8 GB CSV. What is memory-safe?

A. Load the whole file plus a second copy into memory.  
B. Stream/chunk records, validate incrementally, and write bounded batches.  
C. Print every row to logs.  
D. Convert the file to one huge string.  

### 34.

A Python time conversion changes results across environments. What should be fixed?

A. Remove all timezone information.  
B. Add one hour to every value.  
C. Define source timezone, use timezone-aware timestamps, and normalize at a documented boundary.  
D. Use the host's local timezone silently.  

### 35.

A pandas comparison misses rows whose field is `NaN`. What is appropriate?

A. Drop the entire column.  
B. Convert every NaN to the string “0”.  
C. Compare NaN to itself with `==`.  
D. Use a missing-value predicate such as `isna()` rather than equality comparison.  

### 36.

A SQL query uses user input as an `ORDER BY` column. What is safe?

A. Concatenate the raw string into SQL.  
B. Map an allowlisted sort key to known identifiers and validate direction.  
C. Trust authenticated users to send valid SQL.  
D. Base64-encode it and concatenate.  

### 37.

A customer record is missing a value. How should a transformation distinguish unknown from zero?

A. Preserve null/unknown separately and document any imputation rule.  
B. Convert all missing fields to zero.  
C. Delete the record.  
D. Use a random default.  

### 38.

A metric uses binary float for exact currency aggregation. What should be considered?

A. Rounding each row arbitrarily.  
B. Concatenating amount strings.  
C. Treating amounts as booleans.  
D. Decimal/fixed-point representation and explicit currency/rounding semantics.  

### 39.

A CSV parser drops a row with an invalid date but reports success. What is needed?

A. Structured reject reason, counts/threshold, quarantine, and a visible partial-completion state.  
B. Silent dropping to keep the job green.  
C. Remove date validation.  
D. Substitute today's date for every error.  

### 40.

An update watermark has second-level precision and tied updates. What is safer?

A. Round to the nearest hour.  
B. Use strict timestamp greater-than and ignore ties.  
C. Add a stable sequence/key or use CDC/overlap plus idempotent deduplication.  
D. Use destination arrival order only.  

## 5. Deployment and customer environment case

### 41.

A container works locally but fails in an air-gapped customer environment. What should be inspected?

A. Whether the customer's network can access public internet.  
B. Offline dependencies/artifacts, configuration, certificates, network policy, architecture, and startup logs.  
C. Only the source-code theme.  
D. The engineer's home Wi-Fi speed.  

### 42.

A pod is running but should not yet receive traffic. Which mechanism applies?

A. Liveness probe that kills every process during startup.  
B. DNS record deletion.  
C. A manual user refresh.  
D. Readiness probe.  

### 43.

A release contains a schema migration and old code may still run. What pattern is safer?

A. Stop backups and run a one-step destructive migration.  
B. Rename/drop columns before deploying compatible code.  
C. Assume every instance updates simultaneously.  
D. Expand-compatible schema, migrate app/data, verify, and contract/remove old schema later.  

### 44.

A customer-specific API key is found in a container image. What is the response?

A. Leave it because images are immutable.  
B. Treat it as exposed, rotate/revoke, assess access, and move it to approved secret management.  
C. Rename the image tag and keep the key.  
D. Publish the key in a runbook.  

### 45.

A deployment needs to run as a non-root user but file writes fail. What should be fixed?

A. Run everything as root forever.  
B. Directory ownership/permissions and volume configuration for the least-privilege runtime identity.  
C. Disable filesystem permissions.  
D. Store outputs in logs.  

### 46.

A customer restricts outbound traffic. How should package installation work?

A. Use approved internal mirrors or prevalidated offline artifacts with provenance and scanning.  
B. Disable package verification.  
C. Download arbitrary latest packages at runtime.  
D. Tunnel around the firewall through a personal hotspot.  

### 47.

A rollout causes errors for a subset of users. Which release strategy helps limit blast radius?

A. Disable error reporting during release.  
B. Keep shipping changes until the error disappears.  
C. Canary/gradual rollout with health gates, cohort monitoring, and rollback criteria.  
D. Deploy globally at once with no metrics.  

### 48.

A new environment lacks a required variable. What behavior is best?

A. Continue with undefined behavior.  
B. Print all secret values to logs.  
C. Use a hidden developer default.  
D. Fail fast with a safe configuration error and validate environment settings before promotion.  

### 49.

A rollback restores application code but not an incompatible data migration. What was missing?

A. Data/schema rollback or roll-forward plan and compatibility validation.  
B. A larger service name.  
C. More UI screenshots.  
D. A lower log level.  

### 50.

A customer requires a software bill of materials for offline review. What should the release provide?

A. A screenshot of the build server.  
B. An unversioned binary with no dependency information.  
C. A promise that no dependencies exist.  
D. Versioned dependency inventory/provenance and signed or verifiable artifacts through the approved path.  

## 6. Production investigation case

### 51.

Customer imports fail only after the weekend. What evidence helps first?

A. A random restart of every service.  
B. The color of the weekend calendar.  
C. Time-windowed source arrival, scheduled jobs, credentials/rotation, network changes, and recent deploys.  
D. The project's first commit date.  

### 52.

The service is healthy but the customer's critical workflow is blocked. What should be prioritized?

A. The number of open tickets.  
B. The service's logo.  
C. End-to-end user impact and safe mitigation, not only process health.  
D. The green process health badge.  

### 53.

A new release correlates with a p99 spike. What is a safe next action?

A. Delete the latency data.  
B. Increase concurrency without measuring dependencies.  
C. Compare traces/cohorts and, if impact warrants, canary rollback or mitigate while preserving evidence.  
D. Claim the release is the cause without testing.  

### 54.

A database query slows after a data-volume increase. What should be compared?

A. The UI color palette.  
B. Actual query plan, cardinality, indexes, locks, and representative workload.  
C. Only source file line count.  
D. The developer's typing speed.  

### 55.

A remote API returns 429, then the importer retries every second. What should change?

A. Rotate through unauthorized user credentials.  
B. Treat 429 as a successful empty page.  
C. Increase workers and retry faster.  
D. Honor `Retry-After`, add backoff/jitter and shared rate control, and monitor lag.  

### 56.

A customer sees duplicate updates after a worker restart. What should be examined?

A. The provider's public marketing page.  
B. The UI title font only.  
C. Ack timing, idempotency store, transaction boundaries, and replay semantics.  
D. Whether the database has more rows than columns.  

### 57.

A request times out but a record may have been created. What should the caller do?

A. Delete the user's account.  
B. Assume failure and hide the record.  
C. Query operation/idempotency status before creating a new logical operation.  
D. Retry with a different key repeatedly.  

### 58.

A report is off by one day for one region. What is a likely root cause?

A. The number of worker pools.  
B. Timezone/date-boundary conversion or source timestamp semantics.  
C. The file extension.  
D. Object-level authorization only.  

### 59.

A queue's age rises but depth is stable. What could cause it?

A. A shorter source code file.  
B. A color mismatch in the dashboard.  
C. A stuck old message, partition starvation, or priority queue imbalance.  
D. Perfect throughput.  

### 60.

A workaround restored service but users report missing records. What remains?

A. Close the incident because HTTP is 200.  
B. Reconcile and repair data using approved procedures, then verify end-to-end workflow recovery.  
C. Delete all records and re-import without a plan.  
D. Hide missing rows in the UI.  

## 7. AI and decision-support case

### 61.

A retrieval assistant cites documents from another tenant. What is the immediate design correction?

A. Hide the citations.  
B. Increase retrieval top-k.  
C. Enforce tenant authorization in retrieval before model context construction and test isolation.  
D. Ask the model to avoid cross-tenant citations.  

### 62.

A prompt injection appears in a customer document. What boundary should hold?

A. Treat document text as untrusted input and enforce tools/permissions in application code.  
B. Execute document instructions because they are recent.  
C. Put the text in the system role.  
D. Disable user authorization.  

### 63.

A model proposes a refund but lacks eligibility evidence. What should the product do?

A. Abstain or request authoritative evidence and route the action for review.  
B. Issue the refund because the model is confident.  
C. Hide the missing evidence.  
D. Borrow evidence from another customer.  

### 64.

A model response must update a CRM. What should run before the write?

A. Directly execute raw model text.  
B. Store the API key in the prompt.  
C. Schema/business validation, entity authorization, preview/approval as required, and audit.  
D. Disable transaction checks.  

### 65.

An AI pilot has high accuracy on a handpicked test set. What is missing?

A. Representative, versioned evaluation with edge cases, subgroup outcomes, and human review where needed.  
B. Only a longer prompt.  
C. More marketing copy.  
D. A higher temperature.  

### 66.

A model provider becomes unavailable. What should happen?

A. Remove the service's health signal.  
B. Use a bounded retry/circuit-breaker and safe degraded or human workflow; report the limitation.  
C. Fabricate answers from stale cache without disclosure.  
D. Loop indefinitely until the provider returns.  

### 67.

A user asks an AI assistant for policy guidance, but no authorized source supports an answer. What should it do?

A. Make an uncited claim with certainty.  
B. Guess the most popular policy.  
C. Search another tenant's documents.  
D. State insufficient evidence and offer a human/approved-source path.  

### 68.

A reviewer approves every AI recommendation without inspection. What is the concern?

A. Audit logs should be disabled.  
B. The model becomes deterministic.  
C. Rubber-stamping/automation bias; design visible evidence, meaningful review, and escalation.  
D. More approvals always eliminate model error.  

### 69.

A customer asks to send sensitive records to an external model. What comes first?

A. Send a sample before policy review.  
B. Remove names and assume full anonymity.  
C. Data classification, authorization/contract/provider approval, minimization, and retention review.  
D. Put “confidential” in the prompt.  

### 70.

Model performance falls for one user cohort. What is the right response?

A. Investigate cohort data and outcomes, mitigate harm, and involve accountable domain owners.  
B. Suppress cohort metrics because average accuracy is high.  
C. Assume the cohort is using the product incorrectly.  
D. Increase prompt length only.  

## 8. Security, privacy, and governance case

### 71.

A client submits a tenant ID to select records. What is the safe design?

A. Bind tenant scope to authenticated identity and enforce object authorization server-side.  
B. Trust any valid UUID.  
C. Use a hidden UI field as security.  
D. Let the model rewrite the tenant value.  

### 72.

A credential appears in application logs. What should happen?

A. Redact/contain exposure, rotate credential, restrict logs, and assess access/retention.  
B. Publish logs for faster debugging.  
C. Rename the log field only.  
D. Keep it because the log store is convenient.  

### 73.

A customer asks for production data in a local developer database. What is the best default?

A. Email the dump to the team.  
B. Copy the full database to every laptop.  
C. Remove only names and assume no re-identification risk.  
D. Use synthetic/de-identified data; production data requires explicit approval and a governed minimum-access environment.  

### 74.

A partner API response is inserted into a SQL query. What protection is needed?

A. Trust the partner because it has an API key.  
B. Remove database authentication.  
C. Base64-encode values and concatenate them.  
D. Parameterize values and validate/allowlist identifiers; do not trust third-party data as safe SQL.  

### 75.

A data export is sent to an external analytics vendor. What should be verified?

A. Approved purpose/destination, minimum fields, access, encryption, retention, and contract requirements.  
B. Whether the export can be made public.  
C. Vendor logo quality.  
D. Whether the file is large enough.  

### 76.

An FDE needs elevated production access for one hour. What is appropriate?

A. Time-bound approved least privilege, audit, and verified revocation afterward.  
B. Permanent shared admin access.  
C. An unlogged personal account.  
D. A credential in a chat message.  

### 77.

A customer contract requires data to remain in-region. What should be checked?

A. The service logo.  
B. Primary data, backups, logs, telemetry, support access, and subprocessors/AI providers.  
C. The user's browser language.  
D. Only the primary database name.  

### 78.

An endpoint fetches arbitrary user-supplied URLs from the server. What can prevent SSRF?

A. Accept every scheme and private IP.  
B. Hide the endpoint from docs only.  
C. Disable authentication.  
D. Destination allowlists, DNS/IP checks, redirect controls, egress policy, and response limits.  

### 79.

An audit trail stores full payloads forever. What should be reviewed?

A. Nothing; audit logs have no privacy risk.  
B. Purpose, minimization/redaction, retention, access, integrity, and deletion requirements.  
C. Whether to add credentials for completeness.  
D. Whether the logs can be made public.  

### 80.

A customer asks to bypass access controls during a demo. What is the best response?

A. Use an approved demo environment/data path and explain the controls that cannot be disabled.  
B. Use real records on a shared public screen.  
C. Disable controls without noting it.  
D. Create a hidden admin token for the demo.  

## 9. Customer trade-offs and delivery decisions

### 81.

The customer wants an exact launch date before a dependency is tested. What should the FDE do?

A. Hide the dependency.  
B. Promise the date without caveats.  
C. Stop all planning until every detail is known.  
D. Communicate estimate assumptions, validate dependency early, and agree on a decision checkpoint/fallback.  

### 82.

An executive wants complete automation, while operators require approval for exceptions. What is a good design discussion?

A. Segment by risk, automate bounded low-risk cases, and preserve review for ambiguous/high-impact actions.  
B. Require human review for every read-only action.  
C. Let the model choose when policy applies.  
D. Remove approval to satisfy executive preference.  

### 83.

A customer asks for a custom feature that duplicates a supported platform capability. What is wise?

A. Rebuild it immediately without review.  
B. Reject the need because a platform exists.  
C. Validate the workflow need and compare native configuration with bespoke lifecycle/support costs.  
D. Add a duplicate with no owner.  

### 84.

A pilot saves time but increases manual corrections. What should be reported?

A. A claim that corrections are irrelevant.  
B. Only total usage count.  
C. Both time saved and correction/error cost against baseline, with user feedback.  
D. Only the time-saved metric.  

### 85.

A stakeholder adds a request that would delay a critical integration. What should be surfaced?

A. Accept both with no timeline change.  
B. Hide the request from the plan.  
C. Value and urgency trade-off, effort/dependency impact, revised scope/date, and decision owner.  
D. Cut tests silently.  

### 86.

Frontline users reject the new workflow. What is the best response?

A. Force adoption immediately.  
B. Remove safeguards to reduce clicks.  
C. Claim user resistance proves the system is valuable.  
D. Observe task completion, understand friction, and iterate with representative users while retaining safety requirements.  

### 87.

A project needs an approval from security but the reviewer is unavailable. What should happen?

A. Ship to production and ask later.  
B. Treat silence as approval.  
C. Share an admin credential with the team.  
D. Identify the authorized delegate/decision path and safe parallel work; do not bypass required approval.  

### 88.

A customer asks “Can you guarantee this will never fail?” What should the FDE say?

A. Explain measurable reliability goals, known failure modes, mitigations, and recovery rather than promise impossibility.  
B. Guarantee zero failures forever.  
C. Avoid mentioning incident response.  
D. Claim tests prove every future condition.  

### 89.

A stakeholder wants to launch to all users after one successful demo. What is a prudent proposal?

A. Stage rollout with representative pilot, health/quality gates, feedback, and rollback criteria.  
B. Enable all accounts immediately without monitoring.  
C. Stop gathering metrics after the demo.  
D. Remove the manual fallback.  

### 90.

A customer asks for a status report with uncertain root cause. What is best?

A. Wait until the incident closes to communicate.  
B. Separate confirmed facts, hypotheses, impact, action, and next update time.  
C. Present a hypothesis as a fact.  
D. Send unexplained raw traces.  

## 10. Integrated interview prompts

### 91.

You receive a vague request to “modernize customer operations.” What is the best first move?

A. Map users/workflow, baseline pain, data/authority constraints, and measurable outcome before choosing technology.  
B. Choose a model provider immediately.  
C. Promise full automation in a week.  
D. Start with a microservices diagram.  

### 92.

A data pipeline and API team disagree about which timestamp is authoritative. What should you do?

A. Remove timestamps from outputs.  
B. Use server time silently.  
C. Involve the source/domain owner, define event/update semantics, and encode the decision in contract tests.  
D. Pick whichever timestamp is easiest to parse.  

### 93.

A system's uptime is high, but users cannot complete a workflow. How should success be measured?

A. Host uptime alone.  
B. End-to-end task completion, latency/freshness, errors, and user-impact SLOs.  
C. The amount of logs produced.  
D. Number of containers only.  

### 94.

An interviewer asks you to design an integration with an undocumented legacy database. What do you do?

A. Clarify owner/permissions, profile approved samples, map schema/semantics, and build a tested adapter boundary.  
B. Connect with an admin account and dump every table.  
C. Assume column names are correct descriptions.  
D. Build a direct UI-to-database write path.  

### 95.

A customer needs a fast result but data quality is uncertain. What is a reasonable delivery?

A. A bounded pilot with quality indicators, manual review/fallback, and an explicit limit on decisions.  
B. Automate high-impact decisions first.  
C. Delay all feedback until the data is perfect.  
D. Hide uncertainty to preserve launch momentum.  

### 96.

A production incident overlaps with a planned release. What should the team do?

A. Deploy automatically because the pipeline is green.  
B. Delete the change record.  
C. Ignore the incident until after release.  
D. Follow incident/change policy, assess release risk, and pause or proceed only with accountable approval and clear mitigation.  

### 97.

An AI assistant recommends a database write with missing required fields. What is safe?

A. Disable schema validation for AI calls.  
B. Reject/validate the proposal and ask for missing information or route to review; do not guess and execute.  
C. Treat model confidence as authorization.  
D. Fill fields with defaults and commit automatically.  

### 98.

A customer deployment is working, but no one owns the runbook. What should be done before handoff?

A. Leave ownership blank because the FDE built it.  
B. Disable alerts to avoid ownership questions.  
C. Assign an operational owner, review recovery steps/alerts/access, and verify the owner can use them.  
D. Transfer the developer's personal account.  

### 99.

An architecture choice optimizes latency but increases cost and operational burden. How should you present it?

A. Hide cost because latency is technical.  
B. State the trade-off as objectively best for every customer.  
C. Let the team decide without sponsor input.  
D. Quantify expected latency/cost/complexity trade-offs, alternatives, assumptions, and decision owner.  

### 100.

What is the strongest overall FDE delivery principle?

A. Optimize only for a polished demo.  
B. Say yes to every request and ignore constraints.  
C. Pair technical rigor with customer-outcome ownership, secure boundaries, clear communication, and sustainable operations.  
D. Maximize code shipped regardless of user outcome.  
