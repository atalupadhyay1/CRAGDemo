# FDE Practice Set 4: Production Diagnostics and Debugging

**Format:** 100 original, single-best-answer questions  
**Suggested time:** 150 minutes (a self-imposed pacing target)  
**Scoring:** 1 point per question; raw percentage = `correct ÷ 100 × 100`.

> Unofficial study material based on the Udemy course's public topic outline, not its paid questions or assignments. FDE roles and interview formats vary by employer. This set is not endorsed by Udemy or an employer and is not a hiring prediction.

**Instructions:** Choose one best answer for each question. Complete this file before opening the [separate answer key](set-4-production-diagnostics-answer-key.md).

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

## 1. Triage and initial investigation

### 1.

A customer reports that “the system is broken.” What is the best first response?

A. Change production settings immediately without reproducing the issue.  
B. Clarify affected users/workflows, start time, scope, symptoms, and business impact while checking telemetry.  
C. Promise a root cause before collecting evidence.  
D. Ask the customer to send every database password.  

### 2.

A failure affects only one customer tenant. What should be checked early?

A. Tenant-specific config, permissions, data shape, deployment version, and recent changes.  
B. Whether every other tenant should be disabled.  
C. The engineer's monitor resolution.  
D. Global model accuracy only.  

### 3.

An incident may be growing, but root cause is unclear. What is the first operational priority?

A. Ship an unreviewed rewrite.  
B. Mitigate user impact safely while preserving evidence for diagnosis.  
C. Delete recent logs to reduce noise.  
D. Wait for complete root-cause certainty before taking any action.  

### 4.

A release just preceded an error spike. What is the best immediate comparison?

A. Ignore deployment metadata.  
B. Correlate errors with version/change timing, affected routes, dependencies, and user cohort.  
C. Compare office attendance before and after release.  
D. Assume temporal order proves the release is the only cause.  

### 5.

The same incident report contains conflicting timestamps. What should be validated?

A. The user's preferred date format.  
B. The current local time only.  
C. The font used in the incident document.  
D. Clock source/timezone, trace timestamps, event ordering, and ingestion delays.  

### 6.

A customer says a report is wrong but cannot reproduce it. What should be collected first?

A. A screenshot with all sensitive details exposed publicly.  
B. Their personal password.  
C. Report/run identifier, filters, data interval, tenant, source version, and expected versus actual result.  
D. A request to restart every service.  

### 7.

Several errors appear at once. Which helps prioritize them?

A. Which stack trace is longest.  
B. Which error was easiest to fix locally.  
C. User impact, severity, scope, data integrity risk, and time sensitivity.  
D. Which ticket has the most colorful label.  

### 8.

A rollback is possible but may lose accepted jobs. What should happen first?

A. Delete the job queue.  
B. Roll back immediately without checking data behavior.  
C. Assess rollback side effects and protect/record in-flight state before execution.  
D. Tell the customer the jobs completed.  

### 9.

A graph shows a sudden error rate increase but total traffic also doubled. Which metric is useful?

A. Error ratio by request volume and endpoint, not raw error count alone.  
B. Size of the server rack.  
C. Only total error count.  
D. Number of deployments in the last year.  

### 10.

A debugging session is becoming unstructured. What is a useful next step?

A. Stop recording actions.  
B. Ask one engineer to remember everything after the incident.  
C. Have everyone change unrelated settings simultaneously.  
D. Write down hypotheses, evidence, tests, owners, and next actions in a shared incident record.  

## 2. Logs, metrics, traces, and telemetry

### 11.

A request crosses API, queue, worker, and database. What makes traces useful end to end?

A. Disable timestamps.  
B. Propagate trace context and correlate spans across each boundary.  
C. Store only a screenshot of each service.  
D. Generate unrelated IDs at every service.  

### 12.

A log contains an error but lacks tenant and request context. What should be added carefully?

A. The entire database dump.  
B. A random string on every line with no correlation.  
C. Structured, privacy-safe identifiers such as request/trace ID and bounded tenant reference.  
D. Full credentials and raw personal data.  

### 13.

An average latency dashboard looks healthy, but customers report occasional long waits. What should be examined?

A. p95/p99 latency and traces for slow paths, segmented by endpoint/dependency.  
B. The HTTP server's logo.  
C. The number of code comments.  
D. The mean only, at a longer time window.  

### 14.

A metric label includes raw user ID and creates millions of time series. What is the fix?

A. Remove unbounded identifiers from metric labels; use traces/logs with access and retention controls.  
B. Disable all metric collection permanently.  
C. Add more raw identifiers to improve cardinality.  
D. Hash each user ID into an unlimited new label.  

### 15.

An error count doubles but traffic also doubles, while error rate stays stable. What is the likely interpretation?

A. The system is definitely twice as unreliable.  
B. The dashboard is necessarily corrupt.  
C. Raw errors increased with volume; investigate rates and user impact before concluding reliability worsened.  
D. The service has zero user traffic.  

### 16.

Logs are emitted in local time by one service and UTC by another. What should be improved?

A. Standardize timestamps to UTC or include explicit offsets and preserve event time metadata.  
B. Remove timestamps from every log.  
C. Sort log strings alphabetically.  
D. Assume daylight-saving transitions never happen.  

### 17.

A trace shows one dependency consumes most request latency. What should be inspected next?

A. Dependency span details, retries, queueing, connection pool wait, and service-side timings.  
B. The user's monitor brightness.  
C. Whether the trace ID has vowels.  
D. Only application startup logs from last month.  

### 18.

An alert fires continuously, but no user impact is detected. What should the team do?

A. Ignore all alerts from now on.  
B. Delete the metric history.  
C. Increase severity to page more people.  
D. Check alert intent/threshold and its relation to user SLOs; tune or demote non-actionable signals.  

### 19.

A log pipeline truncates long error messages. What should be added?

A. Unlimited raw payload logging.  
B. A bounded structured error code/context and secure correlation to full restricted diagnostics if needed.  
C. No diagnostic data at all.  
D. A random replacement message.  

### 20.

A service is up according to a health check, but customer imports are not completing. What should be monitored?

A. End-to-end completion, backlog age, data freshness, and rejection/failure rates.  
B. The size of the binary alone.  
C. Process existence only.  
D. Whether the dashboard title renders.  

## 3. Network, identity, and protocol diagnosis

### 21.

A service cannot resolve a hostname after deployment. Which layer is most directly implicated?

A. SQL query aggregation.  
B. UI component spacing.  
C. Model temperature.  
D. DNS/configuration or name-resolution path; verify resolver and service name.  

### 22.

TCP connects but the TLS handshake fails. What should be examined?

A. The queue's partition key only.  
B. The database row count only.  
C. Certificate chain, hostname/SAN, trust store, protocol/cipher policy, and system clock.  
D. The user’s browser zoom.  

### 23.

A request returns 401 while the same endpoint worked yesterday. What is a focused check?

A. Token expiry/audience/scope, credential rotation, clock skew, and authentication configuration changes.  
B. Ignore the request headers.  
C. Rebuild every database index immediately.  
D. Increase the JSON response size.  

### 24.

A request returns 403 after authentication succeeds. What should be checked?

A. Whether the client can resolve DNS.  
B. Authorization policy, resource ownership, role/scope, and tenant context.  
C. Whether the request uses a keyboard shortcut.  
D. Whether TLS has a certificate.  

### 25.

A connection works from a developer laptop but times out in the customer network. What is useful?

A. Copy production traffic to an external cloud.  
B. Change application text color.  
C. Verify customer DNS, routes, firewall/egress, proxy, target allowlist, and source network path.  
D. Disable customer firewall without approval.  

### 26.

A client reports intermittent connection resets. What should be compared?

A. The color of the network cable.  
B. Whether all server logs can be deleted.  
C. Connection lifecycle, load balancer/proxy idle timeouts, server resets, and timing of retries.  
D. Only the first successful request.  

### 27.

An API request works with curl but fails in a browser. What should be checked?

A. The database backup schedule only.  
B. Whether curl uses a different font.  
C. CORS/preflight, browser auth/cookie policies, origin headers, and client-generated request differences.  
D. Whether the server can print to a console.  

### 28.

A proxy returns 502 while the application logs show no request. What is a plausible next step?

A. Inspect proxy routing/upstream health and compare proxy logs with application listener/network state.  
B. Assume the application generated a 200 response.  
C. Ask the user to clear browser bookmarks.  
D. Rewrite the database schema immediately.  

### 29.

A service works over HTTP but fails over HTTPS after certificate renewal. What should be verified?

A. Whether the job scheduler has a cron expression.  
B. Record counts in the warehouse.  
C. Certificate chain/SAN, mounted certificate version, reload behavior, and client trust.  
D. The HTML heading level.  

### 30.

A DNS change appears inconsistent across clients. What is likely relevant?

A. The image build command only.  
B. TTL, resolver caches, propagation, and whether clients use the expected resolver.  
C. The API's response schema only.  
D. The SQL isolation level.  

## 4. Database and data-quality debugging

### 31.

A query becomes slow after data volume grows. What is the best starting evidence?

A. Increase every timeout.  
B. Query plan, row estimates/actuals, indexes, filters, locks, and execution timing.  
C. Disable database statistics.  
D. Rewrite the query without measuring.  

### 32.

A write hangs while waiting for a lock. What should be inspected?

A. The CI badge color.  
B. The schema's table names alphabetically.  
C. The user's browser cache.  
D. Blocking/blocked sessions, transaction duration, lock type, and the code path holding the transaction.  

### 33.

A database reports “too many connections.” What should be examined?

A. Disable authentication.  
B. Add a new connection for every row permanently.  
C. Pool sizing, connection leaks, concurrency, timeouts, and database connection capacity.  
D. Increase log verbosity to include passwords.  

### 34.

A query total doubles after adding a dimension join. What is the likely issue?

A. The query needs a longer alias.  
B. The database changed its arithmetic rules.  
C. The UI scales values by two.  
D. Join cardinality or data grain multiplied fact rows.  

### 35.

A report includes records from the wrong day near midnight. What should be checked?

A. The number of worker threads only.  
B. Timezone conversion, source event time, date boundary, and timestamp precision.  
C. The browser's screen size.  
D. Whether the records have long names.  

### 36.

A new source value is rejected by a strict enum constraint. What should happen?

A. Disable all enum validation silently.  
B. Drop the table.  
C. Map every unknown value to “success.”  
D. Confirm the new meaning, update the contract/schema deliberately, and quarantine/alert during transition.  

### 37.

A database update completed, but the API timed out before responding. What should the client assume?

A. The database definitely applied it exactly once.  
B. Retry with a different user ID.  
C. The database definitely rolled back.  
D. Outcome is ambiguous; check using operation ID/idempotency key before retrying a side effect.  

### 38.

A replica returns a stale status immediately after a write. What should be investigated?

A. The database hostname's capitalization.  
B. Replication lag and read routing; consider read-your-writes behavior for that workflow.  
C. The client font cache.  
D. Whether the source CSV used commas.  

### 39.

A data pipeline's row count matches but sums are wrong. What should be compared?

A. Whether the database has a logo.  
B. Key-level reconciliation, transformation rules, null handling, duplicates, and aggregation grain.  
C. Only total row count.  
D. The color of the report chart.  

### 40.

A query returns the latest timestamp but the wrong associated status. Why?

A. A primary key prevents status values.  
B. Timestamp columns cannot be sorted.  
C. The database automatically drops statuses.  
D. The query aggregated timestamp and status independently; rank rows then select the complete latest row.  

## 5. Containers, deployment, and environment differences

### 41.

A container exits immediately in production but runs locally. What should be checked first?

A. Delete the image tags.  
B. Increase the UI font.  
C. Rebuild the customer network from scratch.  
D. Startup command, environment/config, mounted files, permissions, dependencies, and exit logs.  

### 42.

A pod is repeatedly restarted when a dependency is slow. Which probe needs review?

A. The container image registry logo.  
B. The source repository branch name only.  
C. The user's login screen.  
D. Liveness/readiness separation and probe thresholds relative to startup and dependency behavior.  

### 43.

An image works on one CPU architecture but fails on another. What should be validated?

A. The customer email format.  
B. The number of database rows only.  
C. The API response's whitespace.  
D. Image platform/manifest, native dependencies, build target, and runtime architecture.  

### 44.

A new release uses more memory than the previous one. What is the first useful comparison?

A. Same workload, resource metrics, heap/profile data, dependency changes, and deployment configuration.  
B. Disable memory telemetry.  
C. Delete the old version before measuring.  
D. Compare only source-code line counts.  

### 45.

A container cannot write its output directory. What should be checked?

A. Effective user/group, mount ownership/read-only settings, path, and customer policy.  
B. Only the code comment describing the directory.  
C. The DNS TTL.  
D. The queue partition count.  

### 46.

A release is marked healthy while startup migrations are still running. What is the risk?

A. DNS will wait for the database migration.  
B. Traffic may reach an instance before it can safely serve; use readiness and migration coordination.  
C. The image is compressed incorrectly by definition.  
D. The service becomes more reliable automatically.  

### 47.

An environment variable is missing in one customer deployment. What is the best response?

A. Silently use a developer default in production.  
B. Validate required configuration at startup with a safe diagnostic and deployment check.  
C. Print all existing secrets to discover the missing one.  
D. Ignore the missing value and report success.  

### 48.

A container's clock differs from the host and signed requests fail. What should be checked?

A. The table's partition key.  
B. Time synchronization, timezone assumptions, and the signing library's clock-skew tolerance.  
C. Whether the API returns pagination cursors.  
D. The CSS build output.  

### 49.

A Kubernetes service routes to pods that have started but cannot serve. What should be corrected?

A. Readiness checks and service endpoint behavior to exclude unready pods.  
B. Disable the service resource.  
C. Add every pod IP manually forever.  
D. Use liveness as a replacement for authorization.  

### 50.

A customer deployment fails because it tries to download packages from public internet. What is the proper fix?

A. Bypass egress controls using an unapproved hotspot.  
B. Use approved mirrored/packaged dependencies and a tested offline installation process.  
C. Disable package signature checks.  
D. Embed live customer data in the package.  

## 6. Distributed failures and queues

### 51.

A queue has rising age but stable depth. What might explain the symptoms?

A. The user interface is caching fonts.  
B. A small set of old messages, priority starvation, or uneven partition lag; inspect age by partition/key.  
C. The system has no messages.  
D. The data is automatically sorted correctly.  

### 52.

The same event causes duplicate downstream records after a consumer restart. What is the fix?

A. Durable deduplication/idempotent sink keyed by event identity, coordinated with acknowledgment.  
B. Acknowledge before processing.  
C. Increase retry count without changing writes.  
D. Delete all event IDs.  

### 53.

A consumer is stuck on one poison message and never reaches later work. What should be added?

A. Drop every later message without record.  
B. Infinite retry at maximum speed.  
C. Disable message acknowledgements permanently.  
D. Bounded retry, failure classification, dead-letter/quarantine path, and replay tooling.  

### 54.

A downstream call times out, so every worker retries immediately. What is the likely effect?

A. The dependency recovers faster in every case.  
B. A retry storm can deepen dependency overload; use backoff, jitter, budgets, and circuit breaking.  
C. Queue semantics become exactly once.  
D. The network no longer needs timeouts.  

### 55.

A distributed workflow shows one step completed but the final status is failed. What evidence helps?

A. The current dashboard title only.  
B. The exact color of the failure banner.  
C. Durable step state, correlation ID, retry/compensation records, and timestamps.  
D. A random snapshot of worker memory.  

### 56.

A queue backlog grows while consumer CPU is low. What should be checked?

A. Increase producer throughput.  
B. Delete the backlog metric.  
C. Add CPU without profiling.  
D. Blocking I/O, rate limits, database waits, partition assignment, and worker concurrency.  

### 57.

A partition has much higher lag than others. What is a plausible cause?

A. Every partition is balanced by definition.  
B. Hot key, uneven assignment, poison event, or one slow downstream path.  
C. The event schema is too short.  
D. The system's DNS name is misspelled in the UI.  

### 58.

A worker acknowledges before a durable write. What failure mode is possible?

A. The queue backs up more safely.  
B. The message will always be replayed.  
C. A crash after acknowledgement can lose the message's intended side effect.  
D. The side effect is guaranteed exactly once.  

### 59.

A service receives a cancellation while a long job is running. What is a safe design?

A. Delete all job history.  
B. Persist cancellation state and check at safe checkpoints before additional irreversible steps.  
C. Continue silently and mark cancelled.  
D. Assume canceling the HTTP connection kills every worker.  

### 60.

A queue is shared by urgent and bulk jobs; bulk work delays urgent jobs. What can help?

A. Remove urgency metadata.  
B. Increase bulk job priority permanently.  
C. Separate priority queues or fair scheduling with explicit capacity and starvation protections.  
D. Process jobs in random order without metrics.  

## 7. Performance and resource diagnosis

### 61.

CPU usage is high and p99 latency rose. What should be collected?

A. Profiles, endpoint-level traces, request mix, GC/runtime metrics, and recent change comparisons.  
B. Full payload logs without redaction.  
C. Only a screenshot of a dashboard.  
D. The developer's estimated coding speed.  

### 62.

Memory grows steadily over hours and never drops. What is a likely investigation path?

A. Heap/object profiles, cache cardinality, retained references, and workload correlation.  
B. Delete user records randomly.  
C. Reduce CPU limits only.  
D. Increase log verbosity indefinitely.  

### 63.

A service has high latency but low CPU and memory. What bottleneck is plausible?

A. An always-full CPU pipeline.  
B. Missing CSS.  
C. Too many code comments.  
D. External I/O, locks, connection-pool wait, or queueing; inspect traces and wait metrics.  

### 64.

A database connection pool is saturated. What evidence helps locate the cause?

A. Pool wait time, open/idle connection count, query duration, transaction length, and leak checks.  
B. The number of source files.  
C. The keyboard type of the operator.  
D. The API's display name.  

### 65.

A large response increases memory and network time. What can reduce impact?

A. Return the same payload twice.  
B. Buffer additional copies of the full response.  
C. Remove all timeouts.  
D. Pagination/streaming, field selection, compression where appropriate, and response-size limits.  

### 66.

A CPU profile shows most time in JSON serialization. What is a good next experiment?

A. Disable all telemetry and deploy.  
B. Rewrite the database schema immediately.  
C. Measure response shape/size and test safe batching, field selection, or a more efficient serializer.  
D. Increase retries on serialization errors.  

### 67.

A query has low latency on small data but degrades nonlinearly at scale. What should be reviewed?

A. Add a sleep to spread requests.  
B. Query plan, algorithmic complexity, indexes, cardinality estimates, and data skew.  
C. Only the naming convention.  
D. Remove test data from production without analysis.  

### 68.

A file transfer repeatedly times out near completion. What should be examined?

A. The browser bookmarks.  
B. The database's string collation only.  
C. End-to-end timeout budget, proxy idle limits, chunking/resume support, and server processing time.  
D. The file's title casing.  

### 69.

A host reports disk full. What is safe first action?

A. Delete random database files.  
B. Disable alerts and continue writing.  
C. Remove the entire data directory immediately.  
D. Identify filesystem consumers and retention policy, preserve critical state, and free space through approved cleanup.  

### 70.

A service slows after a cache is added. What should be checked?

A. Increase cache TTL without checking correctness.  
B. Remove all metrics.  
C. Assume every cache always makes requests faster.  
D. Cache hit/miss, serialization, network hops, invalidation, connection saturation, and tail latency.  

## 8. Incident response and root cause

### 71.

Multiple teams are responding to a severe incident. What role structure improves coordination?

A. No one communicates until resolution.  
B. A clear incident lead, operations/mitigation owner, communications owner, and shared status record.  
C. Let the newest engineer make every decision without context.  
D. Everyone changes production simultaneously.  

### 72.

A workaround restored service but root cause remains unknown. What should the team do?

A. Delete the workaround record.  
B. Tell customers the issue can never recur.  
C. Keep monitoring, document the mitigation, assign follow-up investigation, and avoid claiming root cause is fixed.  
D. Close the incident as fully understood.  

### 73.

During an incident, an engineer wants to make a risky unreviewed database edit. What should the incident lead ask?

A. Expected impact, rollback/recovery, authority, evidence, and whether a safer mitigation exists.  
B. Whether the edit can be made without logging it.  
C. Whether the engineer can skip customer communication forever.  
D. Whether to delete the backup first.  

### 74.

A postmortem repeatedly blames one operator. What is a more useful focus?

A. Avoid examining the system so nobody feels uncomfortable.  
B. Remove all evidence of the incident.  
C. System conditions, detection/mitigation gaps, contributing factors, and actionable process/technical changes.  
D. Require more heroics from the same operator.  

### 75.

An incident's timeline is incomplete. What should be reconstructed?

A. Customer impact, alerts, deployments, decisions, mitigations, and recovery times from trustworthy records.  
B. Only the final message in chat.  
C. The story that sounds most plausible.  
D. A timeline with invented timestamps.  

### 76.

A customer asks for hourly status during a prolonged incident. What is best?

A. Share confirmed impact, mitigation, known unknowns, next actions, and a predictable update cadence.  
B. Stop responding until root cause is final.  
C. Forward raw internal chat without context.  
D. Promise an exact fix time without evidence.  

### 77.

A mitigation reduced errors but increased data lag. What should the incident update include?

A. Claim the system is fully healthy.  
B. Only the improved error count.  
C. Both error reduction and remaining freshness impact, plus mitigation trade-offs and next steps.  
D. Hide the lag metric.  

### 78.

A production issue is resolved. Which follow-up is most useful?

A. Verify recovery, reconcile any affected data, communicate closure, and assign prevention actions with owners/dates.  
B. Delete incident records to prevent repetition.  
C. Stop monitoring immediately.  
D. Assume no data was affected because API is green.  

### 79.

A postmortem action is “improve monitoring.” How can it become actionable?

A. Leave it as a phrase with no owner.  
B. Add every possible metric without defining action.  
C. Remove all alerts.  
D. Name the signal, threshold/owner, expected detection time, implementation task, and validation method.  

### 80.

A customer is still in a degraded mode after technical recovery. What should the team verify?

A. Only that containers are running.  
B. That the incident channel is quiet.  
C. The customer's end-to-end workflow and backlog/data reconciliation, not just service health checks.  
D. Only that a status page is green.  

## 9. Reproduction, testing, and isolation

### 81.

A bug appears only for one malformed record. What is a good debugging technique?

A. Disable input validation.  
B. Change five unrelated code paths at once.  
C. Preserve a safe sample, minimize it to the smallest reproducer, and test parsing/validation boundaries.  
D. Delete the original and rely on memory.  

### 82.

A failure cannot be reproduced locally because the data volume differs. What should be compared?

A. Only the dataset filename.  
B. Distribution, skew, nulls, ordering, cardinality, and environment/configuration—not just row count.  
C. The developer's screen size.  
D. Number of comments in the source code.  

### 83.

A bug appeared after a large set of changes. How can the suspect range be narrowed?

A. Use controlled rollback/bisect or staged toggles, preserving a reproducible test and data safety.  
B. Revert random commits with no test.  
C. Turn off version control.  
D. Add unrelated features until the symptom disappears.  

### 84.

A unit test passes but production still fails on a boundary value. What is missing?

A. More tests of the same happy path only.  
B. A larger test report font.  
C. Removing the production alert.  
D. Representative edge-case and integration tests that cover production data shape and dependency behavior.  

### 85.

A failed import is difficult to replay. What artifact helps?

A. A verbal description only.  
B. Versioned sanitized input fixture, code/config version, run parameters, and expected output/error.  
C. An unbounded production-data copy on a laptop.  
D. A screenshot without source data or versions.  

### 86.

A bug disappears when debug logging is enabled. What should be considered?

A. Proof that the logs fixed the bug permanently.  
B. Timing/race effects, buffering, altered load, and instrumentation side effects.  
C. Proof that the database is not involved.  
D. A reason to remove all tests.  

### 87.

A dependency failure happens only in an integration environment. What is the best approach?

A. Assume the customer environment is wrong and stop investigating.  
B. Hard-code production credentials locally.  
C. Disable the dependency in production without approval.  
D. Reproduce with controlled dependency faults and compare environment configuration/network/auth paths.  

### 88.

A flaky test fails once in twenty runs. What should be done?

A. Add a longer sleep everywhere.  
B. Delete the test because it is inconvenient.  
C. Capture seeds/timing/resources, isolate shared state and race conditions, then make the test deterministic or robust.  
D. Retry until a green build appears without recording failures.  

### 89.

A production-only defect involves sensitive data. How should a reproducer be prepared?

A. Use minimum necessary approved de-identified/synthetic data while preserving the relevant shape and behavior.  
B. Remove all security controls during reproduction.  
C. Email the data to personal accounts.  
D. Publish the full production record in a public issue.  

### 90.

A system test passes when run alone but fails in the suite. What should be examined?

A. The service logo.  
B. The user's browser history.  
C. Shared state, test ordering, external dependencies, resource contention, and cleanup.  
D. The question's answer key.  

## 10. Debugging case studies

### 91.

A nightly load has zero output but reports success; the source file arrived late. What is the likely defect?

A. The database primary key is too long.  
B. Missing readiness/arrival validation and incorrect empty-input success semantics.  
C. The API response includes too many fields.  
D. The dashboard font is wrong.  

### 92.

An API's p99 latency spikes after adding a third-party lookup. What should be tested?

A. Make the lookup synchronous on every path regardless of need.  
B. Remove p99 from monitoring.  
C. Compare traces and run a controlled test with dependency latency/fallback, then bound the call's deadline.  
D. Increase all service timeouts without measurement.  

### 93.

A message is processed twice after a worker deploy. What should be checked?

A. Ack timing, consumer group/rebalance behavior, idempotency key, and transactional sink/offset handling.  
B. The service's marketing description.  
C. Whether the message contains a comma.  
D. The browser's cache headers only.  

### 94.

A client sees stale data only after writes routed through one region. What is a likely area to investigate?

A. Regional replication lag and read-routing/session consistency.  
B. The SQL field's display label.  
C. CSS caching in the UI only.  
D. The customer's email signature.  

### 95.

A deploy passes health checks but customer webhooks stop arriving. Which diagnostic pair matters?

A. Database schema comments and font files.  
B. The local source-control branch color.  
C. CPU model and user theme only.  
D. Inbound endpoint/proxy reachability and provider delivery/signature/retry logs.  

### 96.

A report count differs only after daylight-saving time changes. What is the likely issue?

A. The CSV quote character.  
B. Row-level authorization only.  
C. The load balancer's TLS certificate.  
D. Local-time boundary conversion or ambiguous/nonexistent times; use explicit timezone rules and test transitions.  

### 97.

One customer's import takes ten times longer after adding a new data source. What should be compared?

A. Only total duration from the previous year.  
B. The color of the customer's company logo.  
C. Per-source timings, row counts, query plans, API limits, data skew, and transformation profiles.  
D. Whether the scheduler uses an even minute.  

### 98.

A service starts returning 429 to its own downstream calls after a scale-up. What is plausible?

A. More instances multiplied aggregate request rate beyond the shared downstream quota.  
B. The API no longer supports headers.  
C. HTTP 429 means authentication succeeded and data is correct.  
D. The new instances automatically reduced traffic.  

### 99.

A fix works until the next restart, then the bug returns. What should be checked?

A. Whether the user closes the browser.  
B. Whether the process ID is a palindrome.  
C. Whether the bug has been solved permanently by definition.  
D. Whether the fix changed ephemeral runtime state instead of durable configuration/data or startup behavior.  

### 100.

The customer reports a recovered service but duplicate records remain. What is the correct next step?

A. Hide duplicate rows in the UI only.  
B. Run a blind delete across all customers.  
C. Ignore duplicates because service health is green.  
D. Reconcile and repair affected data with an approved idempotent procedure, then verify counts and communicate impact.  
