# FDE Practice Set 2: System Architecture and Distributed Systems

**Format:** 100 original, single-best-answer questions  
**Suggested time:** 150 minutes (a self-imposed pacing target)  
**Scoring:** 1 point per question; raw percentage = `correct ÷ 100 × 100`.

> Unofficial study material based on the Udemy course's public topic outline, not its paid questions or assignments. FDE roles and interview formats vary by employer. This set is not endorsed by Udemy or an employer and is not a hiring prediction.

**Instructions:** Choose one best answer for each question. Complete this file before opening the [separate answer key](set-2-system-architecture-answer-key.md).

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

## 1. Requirements and quality attributes

### 1.

A customer asks for “a scalable platform.” What should the architect clarify first?

A. How many microservices to create before seeing the workflow.  
B. Which cloud vendor has the most services.  
C. Expected users, workload shape, latency/availability goals, constraints, and measurable acceptance criteria.  
D. Whether the interface should use a dark theme.  

### 2.

A batch report can be delayed by an hour, but a dispatch alert must arrive in seconds. What follows?

A. Put both in one synchronous request with a one-hour timeout.  
B. Model them as distinct latency classes and choose delivery patterns accordingly.  
C. Disable the batch report.  
D. Give both the same priority because they use one database.  

### 3.

An architecture must work inside a customer-controlled network. What is the first design constraint?

A. Identify network boundaries, allowed dependencies, identity flows, and deployment/egress rules.  
B. Assume the customer network can reach public services.  
C. Put a public endpoint in front of every component.  
D. Move the customer's data to a personal cloud account.  

### 4.

A system must preserve financial updates while tolerating node failure. Which requirement should be made explicit?

A. The number of comments in source code.  
B. Durability/consistency guarantees and the allowed recovery point/objective.  
C. The color used in error messages.  
D. Whether the service name contains a dash.  

### 5.

A customer needs a pilot next month but expects future deployments at 20 sites. What design is sensible?

A. Build a small vertical slice with clear extension points and validate deployment assumptions early.  
B. Hard-code one customer's credentials into the codebase.  
C. Build a global platform for every imagined future use case first.  
D. Skip the pilot and wait until all 20 sites are ready.  

### 6.

Two proposed designs meet the functional need; one is simpler and easier to operate. What should guide the choice?

A. Choose the design with the most components by default.  
B. Choose the design with the newest acronym.  
C. Explicitly compare risk, operating cost, constraints, and reversibility; prefer the simpler fit when trade-offs are acceptable.  
D. Let a diagram's visual complexity decide.  

### 7.

A system's peak load is 50 times its average. What information is most useful before capacity planning?

A. The size of the source repository.  
B. The number of developers in the customer's office.  
C. Peak duration, request mix, burst pattern, concurrency, and latency target.  
D. Average load alone.  

### 8.

A critical workflow must continue during a regional outage. What is needed?

A. A promise that outages are impossible.  
B. More replicas in the same failure domain only.  
C. A second dashboard with the same single-region backend.  
D. Defined failure-domain strategy, recovery objectives, tested failover, and data-consistency behavior.  

### 9.

A customer says “zero downtime” but accepts a short maintenance window. What should be documented?

A. No operational goal until launch.  
B. A guaranteed 100% uptime in every contract.  
C. The phrase “zero downtime” without a measurement method.  
D. The actual availability objective, permitted maintenance, measurement window, and exclusions.  

### 10.

An architecture review has unresolved assumptions about network access. What is the best next artifact?

A. A final implementation plan that treats assumptions as facts.  
B. An assumption/risk list with owners, validation steps, and decision deadlines.  
C. A larger service diagram with no notes.  
D. A launch announcement.  

## 2. Service boundaries and architecture patterns

### 11.

A workflow has one deterministic sequence of steps and no runtime decision-making. What is usually the simplest fit?

A. A separate microservice for every line of code.  
B. A conventional service/workflow with explicit steps rather than an open-ended agent loop.  
C. A swarm of agents with unrestricted tools.  
D. A vector database without orchestration.  

### 12.

A team is splitting a monolith. What is a strong first boundary signal?

A. A desire to use more deployment pipelines.  
B. Every database table must become a service.  
C. A folder that contains many files.  
D. A cohesive business capability with clear data ownership and independently meaningful change cadence.  

### 13.

Two services both write the same customer record. What is the primary risk?

A. Conflicting ownership and update races; define a source of truth and write contract.  
B. Queries become impossible to index.  
C. Network latency disappears.  
D. The record becomes automatically more consistent.  

### 14.

A customer-facing request needs a result from a dependency that is often slow. What architectural choice can protect the request path?

A. Retry every millisecond until the dependency responds.  
B. Use an asynchronous job or bounded timeout/fallback where the business workflow allows it.  
C. Wait forever in a synchronous call.  
D. Disable dependency health checks.  

### 15.

A team wants one service to own data writes while others read through a contract. What pattern is this closest to?

A. Client-side database credentials for all consumers.  
B. Every service directly editing the same tables.  
C. A shared mutable global variable.  
D. Clear service ownership with API/event-based integration rather than shared uncontrolled writes.  

### 16.

A new feature needs to query three legacy systems. Which boundary reduces coupling?

A. An integration adapter/anti-corruption layer that maps legacy contracts into a stable internal model.  
B. Let each UI call databases directly.  
C. Rename all legacy systems without changing behavior.  
D. Copy each legacy schema into every service.  

### 17.

A service needs to publish a database change to a message broker without losing consistency. What pattern is useful?

A. Write the database row, then hope a separate timer publishes it.  
B. Store the event in application logs only.  
C. Transactional outbox or another atomic state-and-event publication design.  
D. Send the message first and ignore database failure.  

### 18.

A read-only analytics workload is slowing transactional writes. What is a reasonable architectural option?

A. Copy production data to a public bucket.  
B. Isolate analytics reads using an approved replica, warehouse, or change-fed projection.  
C. Disable transactional writes during business hours.  
D. Run analytics at maximum concurrency on the primary.  

### 19.

A team proposes microservices to improve reliability, but all services share one database and deploy together. What should be challenged?

A. Whether the added network/operational complexity provides independent ownership or failure isolation.  
B. Whether the database supports SQL.  
C. Whether every service has a separate logo.  
D. Whether services should have names.  

### 20.

A service boundary must change while old clients remain deployed. What should the migration plan include?

A. A compatibility window, parallel contract or adapter, consumer migration, telemetry, and deprecation criteria.  
B. An indefinite duplicate implementation with no owner.  
C. Silent response changes and no consumer inventory.  
D. A same-day removal with no notice.  

## 3. Consistency, ordering, and distributed state

### 21.

A write succeeds in the primary but a read replica lags. What behavior should the application consider?

A. Remove the primary database.  
B. Assume replicas are always synchronous.  
C. Return stale data without indicating any consistency expectation.  
D. Read-your-writes needs, replica lag bounds, and routing or retry behavior for affected requests.  

### 22.

Two workers update the same entity concurrently. Which control helps prevent lost updates?

A. Optimistic concurrency/version check or an appropriate transaction/lock strategy.  
B. Ignore write ordering.  
C. Increase log retention.  
D. Use a longer display name.  

### 23.

A distributed operation spans two services and cannot use one database transaction. What is a common approach?

A. A saga with explicit steps, compensations, and observable failure states.  
B. Assume a local SQL transaction covers remote services.  
C. Hide partial completion from users.  
D. Retry the entire workflow forever without tracking state.  

### 24.

A client retries a timed-out `POST` that created a shipment. What prevents duplicate shipments?

A. A longer timeout only.  
B. An idempotency key or equivalent deduplication state persisted with the operation.  
C. Removing request IDs.  
D. A different random payload on each retry.  

### 25.

Two events share a timestamp but have different sequence numbers. Which ordering is stronger?

A. Use the source sequence as a tie-breaker if it is guaranteed and scoped correctly.  
B. Use arbitrary worker completion time.  
C. Sort by payload length.  
D. Discard one event at random.  

### 26.

A distributed lock expires while the original worker is paused, and a new worker acquires it. What additional protection is useful?

A. A retry loop without a deadline.  
B. Longer comments in the lock code.  
C. A client-side spinner.  
D. A fencing token/version checked by the resource before accepting writes.  

### 27.

A cache serves a stale price after an update. What should the design specify?

A. Invalidation/update semantics, acceptable staleness, and behavior on invalidation failure.  
B. Randomly changing prices to hide staleness.  
C. Disabling all source-of-truth writes.  
D. A rule that caches never expire.  

### 28.

A queue consumer processes messages at least once. What should message handling assume?

A. Every message is guaranteed exactly once in every failure case.  
B. Ordering is global even across partitions.  
C. Acknowledgements cannot be lost.  
D. Duplicates can occur; use idempotent handlers and observable deduplication where side effects matter.  

### 29.

A customer requests strict ordering across all events, but throughput is low. What should be discussed?

A. Ignore sequence numbers.  
B. Scope the ordering requirement; global ordering can constrain parallelism, while per-key ordering may be enough.  
C. Add random consumers to increase global ordering.  
D. Use an unordered cache as the source of truth.  

### 30.

A service must show a newly submitted record immediately, while replicas update asynchronously. What can meet the user expectation?

A. Tell users the write did not happen.  
B. Delete the replica.  
C. Wait indefinitely for every replica to catch up.  
D. Temporarily read from the primary/session-consistent path or return the committed write representation.  

## 4. Resilience and failure containment

### 31.

A downstream service is failing and callers are piling up. Which control limits cascading resource use?

A. Remove request deadlines.  
B. Bounded timeouts and a circuit breaker with a deliberate fallback or failure response.  
C. Add synchronous dependencies to the failing service.  
D. Unlimited retries from every caller.  

### 32.

One customer’s slow workload exhausts all worker threads. What pattern can isolate impact?

A. Retrying all jobs on the same saturated pool.  
B. A shared unbounded queue.  
C. Disabling tenant identification.  
D. Bulkheads or per-tenant concurrency/resource limits.  

### 33.

A timeout is set to 60 seconds at every layer in a call chain. What should be improved?

A. Increase every timeout to several hours.  
B. Set coherent end-to-end deadlines and shorter per-hop budgets, accounting for remaining time.  
C. Remove cancellation propagation.  
D. Use no timeouts because the requests are internal.  

### 34.

A dependency returns HTTP 400 for invalid input. Should a generic retry policy retry it?

A. Yes, retry indefinitely at high speed.  
B. Usually no; classify permanent validation errors separately from transient failures.  
C. Retry only after changing the user ID randomly.  
D. Convert it into a success response.  

### 35.

A customer workflow can continue with cached reference data during a short outage. What is required before using that fallback?

A. Keep using stale data forever without notification.  
B. Let each service invent its own fallback semantics.  
C. Define acceptable staleness, cache provenance, and how the user is told about degraded mode.  
D. Delete the reference source.  

### 36.

A queue is growing because consumers are slower than producers. Which response is best first?

A. Remove queue-depth metrics.  
B. Drop the oldest messages silently.  
C. Measure rate, processing time, and bottleneck; apply backpressure or bounded scaling with capacity limits.  
D. Add unlimited workers without checking downstream capacity.  

### 37.

A retry policy multiplies load during an outage. What should be added?

A. More nested retry loops.  
B. A higher request rate limit for every client.  
C. Exponential backoff, jitter, caps, retry budgets, and circuit breaking as appropriate.  
D. Synchronized retries at fixed short intervals.  

### 38.

A process is restarted after every liveness-check timeout while it is merely waiting for a slow dependency. What is likely misconfigured?

A. The database should be restarted each time.  
B. Liveness is being used for dependency readiness; separate liveness from readiness and set suitable probes.  
C. The container image must be larger.  
D. The service needs no health checks.  

### 39.

A multi-step workflow partially succeeds and then fails permanently. What should the system expose?

A. A generic success message.  
B. No record of the workflow.  
C. A loop that repeats the completed irreversible step.  
D. A durable state showing completed steps, failed step, compensation/retry options, and owner action.  

### 40.

A third-party system has a documented maintenance window. How should the integration respond?

A. Send more requests during the window.  
B. Treat every missing response as an empty result.  
C. Disable all local error monitoring.  
D. Use planned degraded-mode behavior, bounded retries, queued work if safe, and clear status/alerts.  

## 5. Queues, caching, and asynchronous workflows

### 41.

A synchronous request fans out to eight slow services. What is the main architectural risk?

A. Retries become impossible.  
B. The request becomes automatically faster.  
C. Data becomes encrypted by default.  
D. Tail latency and availability degrade with dependency fan-out; reduce critical-path calls or use async composition.  

### 42.

A queue delivers a message before the database transaction that created it commits. What pattern can avoid publishing phantom events?

A. Remove transaction boundaries.  
B. Sleep for an arbitrary duration before every publish.  
C. Publish before writing any state and never verify it.  
D. Transactional outbox or a transactionally coordinated publish mechanism.  

### 43.

A queue's dead-letter queue is accumulating messages. What is the right response?

A. Delete the queue immediately without reviewing the messages.  
B. Replay all messages at maximum rate to production.  
C. Ignore it because the main queue is still available.  
D. Inspect failure categories, repair causes, define replay controls, and track age/count with an owner.  

### 44.

A cache key omits tenant ID, so one tenant can receive another's cached result. What should change?

A. Make all cache entries public.  
B. Increase the cache TTL.  
C. Include the authorization/tenant scope in the key and test isolation, while still enforcing access on reads.  
D. Hide the cache from users.  

### 45.

A queue message schema changes while old consumers are still running. What is safest?

A. Use backward-compatible evolution or versioned envelopes and coordinate consumer rollout.  
B. Send arbitrary binary blobs with no version.  
C. Remove old fields immediately without inventory.  
D. Assume every consumer deploys at the same instant.  

### 46.

A user clicks “start export” twice. What should the workflow do?

A. Create two full exports every time.  
B. Disable job status so duplicates are invisible.  
C. Use an idempotency/client request key or detect an existing equivalent job before creating another.  
D. Randomize the user's identity for each click.  

### 47.

A queue consumer acknowledges a message before its database write. What can happen on crash?

A. The queue can infer the missing row from the payload.  
B. The database automatically retries the queue operation.  
C. The message can be lost even though the write never completed.  
D. The message is always redelivered after acknowledgement.  

### 48.

A fan-out service sends 10,000 notifications. How can it avoid overwhelming a provider?

A. Use a bounded queue, provider-aware rate limits, retries, and progress/error reporting.  
B. Create 10,000 concurrent synchronous calls without limits.  
C. Ignore provider response codes.  
D. Retry every failed notification immediately forever.  

### 49.

A cache miss triggers expensive recomputation for many simultaneous requests. Which pattern can help?

A. Make each request recompute independently.  
B. Request coalescing/single-flight per key, with bounded wait and failure behavior.  
C. Increase the number of cache misses intentionally.  
D. Store the computation in an unauthenticated public key.  

### 50.

A background job is no longer needed after a customer cancels it. What should the system support?

A. Delete the job record but allow workers to continue.  
B. Re-label the job as complete.  
C. A durable cancellation state and cooperative checks before further irreversible work.  
D. Assume killing the web request stops every worker.  

## 6. Scaling and load balancing

### 51.

A stateless API service needs more throughput. What is usually the simplest horizontal-scaling step?

A. Add instances behind a load balancer after checking downstream capacity and state externalization.  
B. Make every request route to a random database primary.  
C. Store all session state in process memory and add instances.  
D. Disable health checks.  

### 52.

A load balancer routes traffic only to healthy instances. What probe is most relevant for deciding whether an instance can serve requests?

A. A check that the source repository is reachable.  
B. Readiness/health signal tied to required local capability and startup state.  
C. A probe that always returns success.  
D. A check of the engineer's laptop battery.  

### 53.

Sticky sessions are required because session state is stored only in one process. What is the better long-term direction?

A. Route all users to one instance.  
B. Externalize shared session state or use stateless signed tokens if appropriate and safe.  
C. Increase stickiness indefinitely and accept uneven load.  
D. Disable failover.  

### 54.

A service autoscaler reacts only to CPU, but queue delay is the main user-facing bottleneck. What metric should be considered?

A. Number of code comments.  
B. The color of the queue dashboard.  
C. Queue depth/age or service-specific saturation correlated with the SLO.  
D. The average age of engineers on call.  

### 55.

An autoscaler adds workers, but the database connection pool is already saturated. What is likely to happen?

A. Connections are automatically free.  
B. Queue lag always falls without side effects.  
C. More workers may increase contention and worsen database load; cap concurrency or scale the actual dependency.  
D. The database becomes infinitely faster.  

### 56.

A cache cluster is overloaded after a cold restart. What can smooth the recovery?

A. Flush the cache repeatedly during peak traffic.  
B. Disable cache metrics.  
C. Controlled warm-up, request coalescing, rate limits, and graceful fallback.  
D. Increase every client retry rate.  

### 57.

A global service must serve users in two regions. What should be evaluated before active-active writes?

A. Conflict resolution, data ownership, replication lag, failover behavior, and consistency needs.  
B. Whether all writes can be applied in any order without testing.  
C. Whether two regions can share a logo.  
D. Whether to remove request identity.  

### 58.

A very large tenant causes noisy-neighbor effects. What helps contain them?

A. Drop other tenants' jobs silently.  
B. Hide its metrics from operators.  
C. Give that tenant unlimited shared resources by default.  
D. Per-tenant quotas, concurrency/resource budgets, and separate capacity tiers where justified.  

### 59.

A load balancer sends traffic to a newly started instance before dependencies are initialized. What should be used?

A. A longer DNS name.  
B. A random startup delay with no health signal.  
C. A liveness probe that always kills the process.  
D. A readiness gate that remains false until required initialization succeeds.  

### 60.

A service receives traffic bursts beyond sustainable capacity. Which control is useful?

A. Disable all timeouts.  
B. Admission control, bounded queues, rate limits, and graceful overload responses.  
C. Unbounded in-memory queues.  
D. Accept every request and hope the host never runs out of memory.  

## 7. Storage, partitioning, and data ownership

### 61.

A system stores transactional records and analytics aggregates with very different query patterns. What is a good starting design?

A. Duplicate write authority across every system.  
B. Force every analytical query onto the transaction path at peak concurrency.  
C. Store all data in application logs only.  
D. Keep the transactional source authoritative and publish purpose-built analytical projections.  

### 62.

A table is growing beyond a single node's storage and write capacity. What should be assessed before sharding?

A. The table's display color.  
B. Whether to shard alphabetically without looking at queries.  
C. Access patterns, partition key/cardinality, hot-key risk, cross-shard transactions, and operational cost.  
D. Whether database backups are needed.  

### 63.

A read replica is used for a workflow that must immediately show a committed update. What risk remains?

A. The replica necessarily returns future data.  
B. Replication lag may return stale data; use a consistency-aware read path for read-your-writes.  
C. The write never reaches the primary.  
D. Reads from replicas are always transactionally current.  

### 64.

A write must update two rows in the same database atomically. What should be used?

A. A cache-only write.  
B. A log message saying both rows were updated.  
C. A database transaction with appropriate constraints/isolation for the invariant.  
D. Two unrelated client calls with no error handling.  

### 65.

A partition key sends most traffic to one shard. What is the issue called?

A. Checkpoint compaction.  
B. Hot partition/key skew.  
C. Schema normalization.  
D. Referential transparency.  

### 66.

A customer needs historical changes, not only current state. Which storage model helps?

A. Save only the latest dashboard screenshot.  
B. Store history in an unstructured temporary variable.  
C. Append-only event/history or temporal records with defined retention and correction semantics.  
D. Overwrite each row and discard all prior values.  

### 67.

A database backup has never been restored in a test. What is the main gap?

A. The backup automatically restores itself in an outage.  
B. The database has too many columns.  
C. The backup file name is too short.  
D. Restore/recovery confidence and verified recovery time/data loss objectives.  

### 68.

A multi-tenant system places all tenants in shared tables. What must be designed carefully?

A. Tenant-aware authorization, query scoping, indexing, backup/retention, and isolation testing.  
B. Assume table separation is unnecessary because IDs are random.  
C. Let clients submit unrestricted SQL.  
D. Use one shared administrator credential for all users.  

### 69.

A schema migration must add a non-null column to a large live table. What rollout reduces risk?

A. Make every old application version write a value it does not know.  
B. Lock the whole table indefinitely and deploy without a backup.  
C. Drop the table and recreate it during business hours.  
D. Add nullable/default-compatible schema, backfill in bounded batches, validate, then enforce the final constraint.  

### 70.

A warehouse contains duplicate copies of the same source data. What is the first governance question?

A. Whether to remove all lineage records.  
B. How to duplicate it one more time.  
C. Whether file names can be randomized.  
D. Which system is authoritative, why copies exist, who owns them, and what retention/access policy applies.  

## 8. Deployment, Kubernetes, networking, and restricted environments

### 71.

A Kubernetes pod is alive but cannot serve requests until warm-up finishes. Which probe should govern routing?

A. Readiness probe.  
B. No probe; send production traffic immediately.  
C. Liveness probe that returns failure throughout normal startup.  
D. A probe on the container image registry only.  

### 72.

A Kubernetes liveness probe fails during a temporary slow dependency. What risk does this create?

A. It permanently improves database latency.  
B. It prevents all network errors automatically.  
C. It validates user authorization.  
D. Unnecessary restarts may amplify load; probe local process health separately from dependency readiness.  

### 73.

A container repeatedly exceeds memory limits. What should be done first?

A. Increase CPU and assume memory use disappears.  
B. Profile memory behavior, inspect limits/requests and workload size, then adjust code or capacity based on evidence.  
C. Remove all memory limits permanently.  
D. Restart the pod every second without investigation.  

### 74.

An application needs different database endpoints per customer environment. What should the image contain?

A. The same versioned image, with environment-specific config injected through approved deployment controls.  
B. A separate hard-coded image with credentials for each customer.  
C. A developer's local `.env` file copied into every container.  
D. No configuration validation.  

### 75.

A customer requires an air-gapped deployment. What should the release package include?

A. Approved, versioned artifacts/dependencies, integrity/provenance information, and offline installation instructions.  
B. A script that downloads arbitrary latest packages from the internet during install.  
C. Production data embedded in the image.  
D. A request to disable network controls.  

### 76.

A deployment uses Kubernetes Secrets, but values are stored unencrypted in a public Git repository. What is wrong?

A. Encoding or using a Secret object does not make source-control exposure acceptable; rotate and move secrets to approved management.  
B. Only usernames need protection.  
C. Nothing; Base64 makes secrets confidential.  
D. Secrets are safe if the filename ends in `.yaml`.  

### 77.

A service can't reach an internal database after deployment. Which evidence is most useful first?

A. A random restart of every cluster node.  
B. The font selected for the service dashboard.  
C. The number of open pull requests.  
D. DNS resolution, route/firewall policy, service endpoint, TLS/auth configuration, and connection error details.  

### 78.

A pod is evicted when another workload consumes node resources. Which configuration helps scheduling fairness?

A. Appropriate resource requests and limits, plus capacity/priority policy aligned to workload criticality.  
B. Hard-code one node name forever.  
C. Remove all requests so the scheduler has no information.  
D. Put every workload at the highest priority.  

### 79.

A deployment update must be reversible. Which release mechanism is useful?

A. Editing running containers manually with no record.  
B. Deleting the previous version before the new one is verified.  
C. Versioned artifacts and controlled rollout/canary with a tested rollback or roll-forward plan.  
D. Replacing binaries in place without health checks.  

### 80.

A customer allows outbound traffic only through an approved proxy. What should the service do?

A. Use random public IPs to evade the egress policy.  
B. Tunnel traffic through an employee's personal hotspot.  
C. Configure and test the approved proxy, document required destinations, and fail visibly if policy blocks access.  
D. Disable TLS verification to make the proxy work.  

## 9. Observability, SLOs, and cost

### 81.

A service is “up” but customer jobs are stuck in a queue. What monitoring is missing?

A. User-workflow indicators such as queue age, completion rate, and end-to-end latency.  
B. More raw payload logs without metrics.  
C. A larger service logo.  
D. Host uptime only.  

### 82.

A trace shows one request across API, queue, worker, and database. What makes correlation possible?

A. A dashboard color palette.  
B. A shared text log file with no timestamps.  
C. Different unrelated IDs generated at every step.  
D. Propagated trace context and identifiers at each boundary.  

### 83.

An SLO is 99.9% monthly success. What is the error budget?

A. The number of engineers in the incident channel.  
B. The monthly cloud invoice limit.  
C. The allowable failure amount implied by the SLO over its measurement window.  
D. A guarantee that no request will fail.  

### 84.

A metric has a label containing every user ID, causing millions of time series. What is the problem?

A. User IDs make metrics more accurate at no cost.  
B. High cardinality can overload metrics storage; use bounded labels and keep identifiers in traces/logs with controls.  
C. The service should generate a random label for each scrape.  
D. Metrics cannot have labels.  

### 85.

A dashboard displays average latency only, while a small group sees very slow requests. What should be added?

A. A second average calculated from the same points.  
B. Percentile/tail latency and segmentation by relevant workflow or dependency, with privacy-safe dimensions.  
C. A filter that excludes slow requests.  
D. A metric that counts code comments.  

### 86.

An alert fires hundreds of times for one underlying outage. What should be improved?

A. Disable alerting permanently.  
B. Send each alert to more people.  
C. Hide the alert history.  
D. Deduplicate/group related alerts, tune actionable thresholds, and preserve incident context.  

### 87.

A customer asks for a per-tenant cost report. What must be considered?

A. Metered usage attribution, shared-cost allocation assumptions, and data/label cardinality limits.  
B. Use request payloads as billing labels with no review.  
C. Ignore shared infrastructure costs entirely.  
D. Assign all shared cost to the smallest tenant.  

### 88.

A service has no explicit SLO but receives 24/7 pages. What is a useful first improvement?

A. Page on every debug message.  
B. Define user-centered indicators and targets with owners, then align alerting to actionable SLO risk.  
C. Set every metric target to 100% without feasibility review.  
D. Turn off the pager and stop measuring reliability.  

### 89.

A service emits logs containing access tokens. What should happen?

A. Stop/redact the exposure, rotate affected credentials as needed, restrict log access, and review retention.  
B. Publish logs to a public dashboard.  
C. Rename the token field and leave the value.  
D. Keep the logs because they are helpful for debugging.  

### 90.

A data pipeline's cloud cost doubles but row volume is unchanged. What should be examined?

A. Only the customer support team's headcount.  
B. Increase the budget and stop measuring.  
C. Query plans, retries, resource utilization, egress, retention, and recent deployment/config changes.  
D. Delete all cost labels.  

## 10. Security and architecture decision scenarios

### 91.

A service account can read every tenant's records although it serves one tenant. What is the best correction?

A. Share the account password with every operator.  
B. Hide the account name from dashboards.  
C. Keep broad access because the service is internal.  
D. Scope credentials and authorization to the minimum required tenant/resources, with rotation and audit.  

### 92.

An architecture depends on a third-party API returning data in a stable shape. What should be included?

A. No tests because it is a trusted vendor.  
B. An assumption that the vendor never changes behavior.  
C. Contract validation, timeout/rate-limit handling, monitoring, and a fallback or safe failure policy.  
D. Storing the vendor's credentials in client-side code.  

### 93.

A customer asks to bypass encryption because the service is on a private network. What is the best response?

A. Disable encryption immediately without documenting the exception.  
B. Remove all authentication because the network is internal.  
C. Follow approved security policy; private networking does not alone replace required encryption and identity controls.  
D. Send credentials in cleartext if the IP is private.  

### 94.

Two regions may both accept writes during a partition. What must be designed?

A. Assume conflicting updates merge correctly by themselves.  
B. Disable replication monitoring.  
C. Conflict detection/resolution and ownership semantics, or a deliberate choice to limit writes for consistency.  
D. Let the latest local clock always win without analysis.  

### 95.

A new architecture decision has important trade-offs. How should it be recorded?

A. Draw a diagram with no decisions or dates.  
B. Use a short decision record with context, options, choice, consequences, owners, and revisit conditions.  
C. Keep the rationale only in one engineer's memory.  
D. Record only the selected product name.  

### 96.

An agentic component can call a payment service. What boundary is most important?

A. Enforce authorization, limits, validation, idempotency, and approval outside the model at the tool/service boundary.  
B. Hide the tool name but grant unrestricted credentials.  
C. Let retrieved documents alter permissions.  
D. Trust the model's reasoning as the payment authorization system.  

### 97.

A single shared database is the only state store for API, worker, and reporting. What architecture question matters most?

A. Whether ownership, isolation, workload contention, backup, and change coordination meet the actual requirements.  
B. Whether every service can bypass the API and write directly.  
C. Whether each team can create tables without review.  
D. Whether database telemetry can be disabled.  

### 98.

A dependency has no redundancy and is required for every user request. What should be reviewed?

A. Whether to remove all request timeouts.  
B. Its logo and release-note style.  
C. Its failure impact, alternatives/fallback, SLO contribution, and whether the dependency belongs on the critical path.  
D. Whether errors can be renamed as warnings.  

### 99.

A team wants to adopt a new database for one customer's use case. What is the best evaluation approach?

A. Adopt it before defining data ownership.  
B. Compare workload fit, operational maturity, migration/rollback, security, cost, and team support against simpler alternatives.  
C. Adopt it because it is newest.  
D. Ignore deployment restrictions because the database is popular.  

### 100.

An architecture passes load tests but has never been tested during dependency failure. What should happen before production reliance?

A. Remove alerts so tests are quiet.  
B. Run controlled failure/recovery tests for critical dependencies and verify behavior against the SLO/runbook.  
C. Assume load testing proves failure resilience.  
D. Wait for a real outage to learn recovery behavior.  
