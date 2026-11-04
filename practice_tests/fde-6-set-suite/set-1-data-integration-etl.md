# FDE Practice Set 1: Data Integration and ETL

**Format:** 100 original, single-best-answer questions  
**Suggested time:** 150 minutes (a self-imposed pacing target)  
**Scoring:** 1 point per question; raw percentage = `correct ÷ 100 × 100`.

> Unofficial study material based on the Udemy course's public topic outline, not its paid questions or assignments. FDE roles and interview formats vary by employer. This set is not endorsed by Udemy or an employer and is not a hiring prediction.

**Instructions:** Choose one best answer for each question. Complete this file before opening the [separate answer key](set-1-data-integration-etl-answer-key.md).

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

## 1. Source discovery and requirements

### 1.

A customer asks to combine two operational feeds, but no one can explain what “active” means in either system. What should the FDE do first?

A. Infer the definition from the most frequent value.  
B. Map both values to `true` so the dashboard is consistent.  
C. Drop the field from the integration without documenting it.  
D. Profile representative source records and confirm field meaning and business rules with the data owner.  

### 2.

A source spreadsheet changes column names between monthly exports. Which first step best reduces downstream breakage?

A. Rename columns by position, regardless of header text.  
B. Let every downstream query discover columns dynamically.  
C. Treat every new spreadsheet as a separate product.  
D. Establish a versioned input contract and validate each export against it.  

### 3.

You need to estimate the complexity of a 20-million-row import. Which sample is most useful?

A. A representative sample across dates, rare statuses, nulls, and high-volume entities.  
B. A hand-typed sample designed to look clean.  
C. Only rows with the most common status.  
D. The first ten rows in file order.  

### 4.

The customer says an identifier is “unique,” but two source systems use the same numeric IDs. What should the target key include?

A. The current row number in the export.  
B. A random ID regenerated on every run.  
C. Only the numeric ID, because integers are compact.  
D. A stable source namespace plus the source identifier, unless a governed global key exists.  

### 5.

A data owner says an upstream field is “usually populated.” How should the integration specification represent it?

A. Define nullability, expected meaning, handling, and a measured threshold for missing values.  
B. Ask the model to fill missing values without a review policy.  
C. Ignore nulls during all validation.  
D. Declare it required and silently substitute a default.  

### 6.

The target dashboard must refresh every 15 minutes, while the source can export only hourly. What is the correct response?

A. Confirm the source's actual freshness limit and agree on a feasible service expectation.  
B. Poll the source every minute until it produces new data.  
C. Promise a 15-minute refresh regardless of source capability.  
D. Duplicate yesterday's records to simulate freshness.  

### 7.

A source table contains both `created_at` and `updated_at`. Which should normally drive incremental extraction of changed rows?

A. The display name, sorted alphabetically.  
B. The destination insert time from a previous run.  
C. `created_at`, because it is always earlier.  
D. `updated_at`, if its semantics and precision reliably change on every relevant update.  

### 8.

The source system's owner cannot grant production access yet. What is a productive next step?

A. Borrow another employee's production credentials.  
B. Copy a customer database to a personal drive.  
C. Use an approved representative extract or sandbox, document assumptions, and keep access approval as a release gate.  
D. Build against invented records and claim source validation is complete.  

### 9.

A customer wants one canonical customer record from three systems. What should be defined before entity matching?

A. Let the import order decide which record survives.  
B. Match rules, survivorship rules, source precedence, and a review path for ambiguous matches.  
C. Always keep the record with the longest name.  
D. Merge records whenever any two fields match.  

### 10.

A source file contains the string `N/A` in a numeric column. What is the safest initial treatment?

A. Convert it to the largest representable integer.  
B. Delete every row containing the string.  
C. Convert it to zero without recording that conversion.  
D. Preserve the raw value and apply an explicit, documented parse rule into a nullable typed field.  

## 2. Extraction, pagination, and change capture

### 11.

An API returns `next_cursor` until all records are read. How should the importer complete a large extraction?

A. Request page one repeatedly and overwrite the target.  
B. Stop after the first response because it is sorted.  
C. Follow each cursor until none remains and checkpoint progress for safe resumption.  
D. Increase the timeout and assume one response contains every page.  

### 12.

A timestamp watermark may have multiple rows with the same timestamp. How can an incremental query avoid missing tied records?

A. Sort by an unrelated display label.  
B. Round timestamps to the nearest day.  
C. Use strict `updated_at > last_time` and ignore ties.  
D. Use a composite cursor such as `(updated_at, stable_id)` or an overlap window with deduplication.  

### 13.

A source supports log-based CDC. Why can CDC be preferable to polling whole tables?

A. It removes the need for source authorization.  
B. It can capture inserts, updates, and deletes with lower repeated-read cost when correctly configured.  
C. It guarantees exactly-once delivery without consumer state.  
D. It eliminates the need to manage schema changes.  

### 14.

A customer needs a one-time initial load followed by changes. Which sequence is safest?

A. Load rows in random order and discard the change log.  
B. Finish an uncoordinated snapshot and begin CDC several days later.  
C. Start CDC only after turning off all source writes.  
D. Coordinate a consistent snapshot and CDC starting position, load the snapshot, then apply changes from that position.  

### 15.

A source export is generated at 02:00 but sometimes arrives at 02:20. How should the scheduler behave?

A. Check for the expected artifact with a bounded wait and alert if it misses the agreed arrival window.  
B. Assume an absent file means there were no changes.  
C. Read the previous day's export and mark today's run complete.  
D. Trigger the pipeline every second until a file appears.  

### 16.

A source API limits requests per minute. How should an extractor handle the limit?

A. Start more parallel workers until the source responds.  
B. Apply a shared rate limiter, respect retry guidance, and monitor backlog.  
C. Retry every request immediately after a 429.  
D. Cache credentials in the URL to reduce authentication calls.  

### 17.

A source allows only offset-based pagination, and rows may be inserted during a long scan. What reduces page shifting?

A. Increase the page size to infinity.  
B. Skip every other page to reduce load.  
C. Sort by a non-unique name and accept duplicates.  
D. Use a stable sort key and a consistent snapshot or bounded high-water mark where supported.  

### 18.

A source changes a record's status from `open` to `closed` but leaves `created_at` unchanged. What happens if extraction filters only on `created_at`?

A. The target can infer the new state from the old row.  
B. The update is always captured because status changed.  
C. The source automatically changes the ID.  
D. The update is missed; use a reliable update timestamp, CDC, or another change mechanism.  

### 19.

A source can emit hard deletes but the destination must retain deletion history. What should the integration do?

A. Capture tombstones or deletion events and represent them in the target according to retention policy.  
B. Recreate deleted rows with a blank status.  
C. Purge all destination history on each run.  
D. Ignore deletes because missing rows will eventually disappear by themselves.  

### 20.

The source API returns a short-lived token for each page. What should the client do?

A. Print the token to logs so operators can reuse it.  
B. Store the token in the dataset as a row attribute.  
C. Disable token expiry in the client.  
D. Refresh credentials using the approved flow and resume from a durable cursor.  

## 3. Batch, streaming, and event semantics

### 21.

Two events for one order arrive out of order. Which field should usually determine event chronology?

A. The order in which workers finish processing.  
B. The order in which files are alphabetically listed.  
C. The trusted event time or source sequence, with a defined late-event policy.  
D. The destination database's current local clock only.  

### 22.

A streaming consumer crashes after writing output but before acknowledging the message. What property prevents duplicate side effects?

A. Idempotent processing keyed by a stable event ID or deduplication record.  
B. A larger consumer memory limit.  
C. An assumption that the broker will never redeliver.  
D. Randomly delaying acknowledgements.  

### 23.

A daily batch may be rerun after a failure. What should define the rerun boundary?

A. A newly generated random interval on every retry.  
B. The current wall-clock minute only.  
C. The number of rows from the previous run, regardless of source state.  
D. A deterministic run ID and source interval, with atomic or idempotent writes.  

### 24.

A stream has a five-minute watermark. What does the watermark generally represent?

A. The system's completeness assumption for event time up to a point, subject to a late-event policy.  
B. A guarantee that no later event can ever arrive.  
C. The number of workers in the consumer group.  
D. A database password rotation interval.  

### 25.

A producer retries sending an event after a network timeout. What should the event include?

A. Only a mutable display string.  
B. A new random event ID on every retry.  
C. A stable event ID so consumers can detect duplicate deliveries.  
D. The consumer's database password.  

### 26.

A batch job writes half its output and then crashes. Which design best prevents consumers seeing partial results?

A. Write to a staging area and publish/merge atomically after validation.  
B. Delete the source file before writing begins.  
C. Tell consumers to guess which rows finished.  
D. Mark the job successful before the final write.  

### 27.

A downstream report needs a consistent point-in-time view of several related tables. What helps achieve it?

A. Run the report while disabling transaction isolation.  
B. Read from a consistent database snapshot or coordinated version boundary.  
C. Query each table at random times and combine the latest rows.  
D. Sort every table by its title column.  

### 28.

A stream consumer's lag is growing although processing rate is stable. What should be checked first?

A. Whether the alert threshold is hidden from the dashboard.  
B. Whether incoming event rate exceeds sustainable processing throughput and whether partitions/consumers are balanced.  
C. Whether the database schema uses longer column names.  
D. Whether the user interface has a darker theme.  

### 29.

An event can be corrected after it is first published. Which event design is useful?

A. Reuse an unrelated event ID and hope consumers overwrite correctly.  
B. Make consumers infer corrections from file size.  
C. Include event identity, version/sequence, and correction semantics so consumers can reconcile updates.  
D. Delete all previous events without a tombstone.  

### 30.

A consumer needs to process each customer's events in order but can process different customers concurrently. What partitioning strategy fits?

A. Partition randomly on every retry.  
B. Sort only after side effects have already executed.  
C. Partition by a stable customer key, preserving order within each partition.  
D. Use one global worker and no message key.  

## 4. Data quality and schema management

### 31.

A field is missing in 8% of one source's records. What is the best next step?

A. Drop the entire feed without checking business impact.  
B. Measure missingness by source/time/cohort and confirm whether absence is meaningful before setting a policy.  
C. Convert every missing value to zero.  
D. Use the same default as a different field.  

### 32.

A pipeline receives an unexpected enum value. What should happen?

A. Drop it without a metric.  
B. Preserve or quarantine the value, surface a schema/quality alert, and avoid silently misclassifying it.  
C. Map it to the first enum alphabetically.  
D. Crash every unrelated customer pipeline permanently.  

### 33.

Which check best detects duplicate business entities in a dimension table?

A. A count of rows greater than zero.  
B. A check that every column is non-null.  
C. A uniqueness assertion on the governed natural or surrogate key at the intended grain.  
D. A sort by display name.  

### 34.

A source adds a nullable field. What is normally the safest schema evolution?

A. Reinterpret the existing primary key as the new field.  
B. Ignore all schema changes forever.  
C. Reject every payload until all producers send the field.  
D. Treat the field as optional, update the contract, and test old/new payload compatibility.  

### 35.

A measure reports dollars but arrives as floating-point values. What is safer for exact financial totals?

A. Use a decimal representation with defined currency and rounding rules.  
B. Convert amounts to strings and concatenate them.  
C. Use binary floating point and round differently in each service.  
D. Drop fractional cents during ingestion.  

### 36.

A source date string `03/04/2026` is ambiguous across regions. What should the pipeline do?

A. Require an explicit format/locale or source contract, then parse and normalize consistently.  
B. Replace the date with ingestion time.  
C. Sort the strings lexically and call that chronological order.  
D. Assume month/day order in every deployment.  

### 37.

A target has `quantity=0`, but the source value was blank. How should the model preserve meaning?

A. Delete the quantity column.  
B. Represent missing separately from zero, such as nullable value plus a quality/status indicator.  
C. Convert zero to null but keep blanks as zero.  
D. Treat blank and zero as identical without discussion.  

### 38.

A data-quality rule rejects 20% of a new customer feed. What is the best operational response?

A. Retry the identical file continuously.  
B. Delete rejected records permanently with no report.  
C. Disable all validation to make the load green.  
D. Capture rejected rows with reasons, quantify impact, and review rules with the data owner before changing thresholds.  

### 39.

A pipeline's source schema has a field that sometimes changes from integer to string. What should the boundary do?

A. Convert every string to zero.  
B. Validate types, record incompatible values, and apply an explicit versioned conversion or quarantine policy.  
C. Trust the destination database to guess the intended type.  
D. Remove type checks from the entire pipeline.  

### 40.

Two records share a supposedly unique email address. What should entity resolution do?

A. Merge them because email is always globally unique.  
B. Keep the record processed last and delete the other.  
C. Flag the collision for policy-based resolution rather than merge automatically without evidence.  
D. Add their numeric IDs together.  

## 5. SQL, data modeling, and query reasoning

### 41.

You need the latest event row per device, including its status. Which SQL pattern fits?

A. `COUNT(*)` grouped by status.  
B. `MAX(status)` grouped by device.  
C. `ROW_NUMBER()` over each device ordered by event time and a stable tie-breaker, then filter to one.  
D. `DISTINCT status` without a device key.  

### 42.

A fact table is double-counted after joining to a one-to-many tag table. What should be checked?

A. Use `SELECT *` to preserve every duplicate.  
B. Remove the primary key from the fact table.  
C. Join grain and cardinality; aggregate at the intended grain before or after a controlled bridge join.  
D. Increase the font size in the dashboard.  

### 43.

A query must retain customers with no orders. Which join is appropriate?

A. `INNER JOIN` because it always preserves all customers.  
B. `LEFT JOIN` from customers to orders, with order filters handled without null-rejecting the left rows.  
C. `CROSS JOIN` with every table.  
D. `RIGHT JOIN` from orders while selecting only order rows.  

### 44.

A query filters `WHERE amount = NULL`. Why does it return no matches?

A. `NULL` is always equal to zero.  
B. SQL null uses three-valued logic; use `IS NULL` for null testing.  
C. The database ignores all `WHERE` clauses.  
D. The equality operator converts null to a string.  

### 45.

A SQL `LEFT JOIN` unexpectedly removes rows from the left table after a right-table filter. What is likely wrong?

A. The right-side predicate in `WHERE` rejects null-extended rows; move it into the join condition when appropriate.  
B. Left joins cannot preserve unmatched rows.  
C. The database sorted the left table incorrectly.  
D. The query needs a larger text column.  

### 46.

A table has one row per daily customer snapshot. What should the composite key likely include?

A. Every measure value concatenated in arbitrary order.  
B. Customer identity and snapshot date, matching the table's declared grain.  
C. The database's physical row address.  
D. Only the customer's first name.  

### 47.

An analyst wants to count unique orders after joining order lines. Which expression is safest if the join multiplies orders?

A. `MAX(order_id) - MIN(order_id)`.  
B. `COUNT(DISTINCT order_id)` or an equivalent aggregation at order grain.  
C. `SUM(order_id)`.  
D. `COUNT(*)` over the joined line rows.  

### 48.

Two columns both contain `status` after a join. How can ambiguity be avoided?

A. Convert both statuses to binary integers.  
B. Remove all aliases and rely on database guesswork.  
C. Rename both columns to the same output name.  
D. Use table aliases and qualify column references, with explicit output names.  

### 49.

A query repeatedly scans a large table for rows newer than a timestamp. Which index may help, subject to query plans and selectivity?

A. A unique index on a constant value.  
B. No index can help range predicates.  
C. An index on the filtered timestamp, possibly combined with relevant partition/key columns.  
D. An index on an unrelated comment field only.  

### 50.

A `GROUP BY customer_id` query selects `customer_name` without aggregating it. What is the correct fix?

A. Join to a dimension with one governed name per customer or include a valid aggregation/grain rule.  
B. Disable SQL validation in production.  
C. Select a random name from any row without documenting it.  
D. Remove `customer_id` from the grouping and keep the sum.  

## 6. Python data processing

### 51.

A CSV export is several gigabytes. Which Python approach limits memory use?

A. Stream rows with a CSV reader or process bounded chunks.  
B. Read the entire file into one list of strings.  
C. Convert the whole file to a single Python object before validation.  
D. Print the full file to standard output.  

### 52.

A Python function processes money values. Which type is safest for exact decimal arithmetic?

A. `bool`, because amounts are either paid or unpaid.  
B. `float` with repeated binary arithmetic and no rounding rule.  
C. `set`, because it deduplicates amounts.  
D. `decimal.Decimal` created from strings, with explicit rounding policy.  

### 53.

A pandas column has missing values. Why can `value == float('nan')` fail to identify them?

A. The comparison converts the frame to JSON.  
B. NaN compares equal to every number.  
C. Pandas never supports missing data.  
D. NaN is not equal to itself; use `isna()` or an equivalent missing-value check.  

### 54.

A Python transform must preserve the original input for audit. What is a safe pattern?

A. Reconstruct raw data from the output after lossy normalization.  
B. Log credentials alongside the transformed record.  
C. Keep the raw record immutable or stored separately and write transformed output as a new value.  
D. Mutate the only input object in place and discard the original.  

### 55.

A parser receives malformed rows among valid rows. Which behavior is most supportable?

A. Replace every malformed row with the previous row.  
B. Validate each row, capture structured error reasons, and quarantine failures while reporting counts.  
C. Silently skip every error and report a complete load.  
D. Stop the service permanently on the first bad character.  

### 56.

A Python request handler retries a database write after timeout. What should be established before retrying?

A. Whether the process has printed a debug statement.  
B. Whether the operation is idempotent or protected by an idempotency key/transaction strategy.  
C. Whether the user prefers longer error messages.  
D. Whether the source file has an uppercase extension.  

### 57.

A customer file contains Unicode names that are corrupted after ingestion. What should be checked first?

A. Increase the database integer precision.  
B. Change all names to lowercase and assume it fixes encoding.  
C. Source and destination encodings, decoding errors, and normalization policy using representative examples.  
D. Strip every non-ASCII character without consultation.  

### 58.

A Python transformation depends on the current timezone of the host. What is the risk?

A. Host timezone affects only variable names.  
B. Results can differ across deployment environments; define timezone semantics and normalize explicitly.  
C. Python will always convert every timestamp to UTC automatically.  
D. Timezones cannot affect date boundaries.  

### 59.

A developer uses `eval()` to parse a field that should contain a number. What is the safer alternative?

A. Ask the user to sign the input.  
B. Use a strict numeric parser and validate range/type instead of evaluating arbitrary input.  
C. Keep `eval()` but hide its source code.  
D. Run the value as a shell command.  

### 60.

A Python job writes a large output file. How can it avoid leaving a partial file that looks complete after a crash?

A. Delete the output before checking whether the input exists.  
B. Append arbitrary retries to the same final file.  
C. Write directly to the final path and mark it complete before opening it.  
D. Write to a temporary path, flush/validate, then atomically rename or publish on success.  

## 7. Orchestration, retries, and recovery

### 61.

An ETL pipeline has extract, transform, and load steps. Where should validation gates run?

A. Never, because schema checks slow all jobs.  
B. Only after a customer reports a bad dashboard.  
C. Only in the user interface.  
D. At source boundaries and before publishing target data, with checks appropriate to each contract.  

### 62.

A task fails because a remote API is temporarily unavailable. What is a good orchestrator policy?

A. Bounded retry with backoff for transient errors, then fail visibly and alert if exhausted.  
B. Mark success to prevent an alert.  
C. Retry every millisecond forever.  
D. Delete the task history and start an unrelated pipeline.  

### 63.

A downstream job should start only after two upstream datasets are complete for the same date. What dependency should be modeled?

A. A fixed sleep of one second after the first dataset.  
B. A join/condition on both successful dataset partitions for that date.  
C. A dependency on whichever task was created last.  
D. No dependency; let the job use mixed dates.  

### 64.

A retry repeats an entire DAG and duplicates its external side effect. What design change is best?

A. Add more workers without changing task semantics.  
B. Disable all retries, including safe reads.  
C. Make side effects idempotent and checkpoint completed units; separate retryable computation from irreversible actions.  
D. Hide the duplicated records from dashboards.  

### 65.

A scheduled pipeline's task depends on local disk from a previous worker. Why is that fragile?

A. Intermediate data should be embedded in logs.  
B. The scheduler guarantees the same machine forever.  
C. Workers may be replaced or scheduled elsewhere; persist intermediate state in an approved shared durable store.  
D. Local disk is always replicated across every worker automatically.  

### 66.

A job completes but writes zero rows when the source is delayed. What state should the orchestrator report?

A. Always report success because the process exited.  
B. Report failure for every legitimate empty interval.  
C. Distinguish a valid empty interval from missing/late input and surface the appropriate status.  
D. Fill the target with duplicate prior-day rows.  

### 67.

A long transformation needs to resume after a worker restart. What helps most?

A. Restart from the beginning and append every result.  
B. Increase the log level to debug.  
C. Keep all progress only in process memory.  
D. Persist deterministic checkpoints or partition completion state and make writes idempotent.  

### 68.

A dependency update changes a parsing library. What should be included in the deployment workflow?

A. Remove the lockfile to make versions flexible.  
B. Skip tests because libraries are externally maintained.  
C. Install the latest package directly in production on every run.  
D. Versioned dependencies, tests against representative fixtures, and a controlled promotion/rollback path.  

### 69.

A pipeline uses a fixed sleep to wait for an upstream export. What is a better replacement?

A. Poll/check for a named artifact or readiness signal with a deadline and alert on timeout.  
B. Treat the sleep duration as proof of completeness.  
C. Increase the sleep indefinitely for every customer.  
D. Start the downstream job before the export exists.  

### 70.

A failed job is rerun with a different input interval by accident. What metadata would prevent this?

A. Store the interval in a temporary local variable.  
B. Save only the operator's display name.  
C. Persist run ID, source interval, code/config version, and input references with the run.  
D. Generate a new random run label after completion.  

## 8. Performance and scale

### 71.

A transformation processes records with an O(n²) nested comparison and slows sharply as volume grows. What should be considered?

A. Add an arbitrary sleep between rows.  
B. Reduce the number of columns without profiling.  
C. Replace repeated scans with an indexed/hash-based lookup or set-based join, then benchmark.  
D. Increase the log volume for every comparison.  

### 72.

A database query filters by tenant and recent timestamp on a large table. Which index design is worth evaluating?

A. A random index on every column without workload analysis.  
B. An index on an unrelated free-text note only.  
C. Removing all indexes so writes are always faster.  
D. A composite index aligned with common tenant/time predicates and ordering, verified by the query plan.  

### 73.

A full-table export saturates the source database. What is the best mitigation?

A. Run the export more often to keep each scan smaller without measuring load.  
B. Disable source monitoring during extraction.  
C. Coordinate an approved read replica/snapshot or incremental extraction and throttle within source capacity.  
D. Increase concurrency to the highest possible value.  

### 74.

One customer partition contains 80% of events and becomes a throughput bottleneck. What should be analyzed?

A. Randomly change keys on each event.  
B. Key skew and workload semantics; consider safe subpartitioning or specialized handling without breaking ordering requirements.  
C. Add more identical workers to the same hot partition and assume it splits automatically.  
D. Drop events for that customer.  

### 75.

A Python pipeline retains all parsed rows and memory grows until out-of-memory. What is the first code-level improvement?

A. Process bounded chunks/iterators and release or persist intermediate batches.  
B. Cache the full source twice.  
C. Write a log line containing the complete dataset.  
D. Increase each row's object size.  

### 76.

A database sink receives many tiny insert statements and becomes the bottleneck. Which change is often useful?

A. Disable constraints without a recovery plan.  
B. Use parameterized bulk/batch inserts within bounded transactions and measure lock/latency effects.  
C. Open a new transaction for each field.  
D. Increase client retries on all insert errors.  

### 77.

A transformation recomputes the same expensive reference lookup for every row. What is a good optimization?

A. Replace the reference data with a random value.  
B. Move the lookup into a per-row sleep.  
C. Cache or join the reference data appropriately, with freshness and memory limits defined.  
D. Recompute it more times to improve accuracy.  

### 78.

A streaming pipeline has high CPU but low throughput. What should be inspected before scaling out?

A. Profiles, serialization cost, backpressure, batch sizes, and time spent on external calls.  
B. Whether all logs are being printed twice.  
C. The color of the service dashboard.  
D. Only the number of comments in source code.  

### 79.

An export causes lock contention on the source. What can reduce the impact?

A. Run writes concurrently to keep the database busy.  
B. Use an approved snapshot/replica, bounded reads, and a lower-impact isolation strategy agreed with the source owner.  
C. Remove source indexes during business hours.  
D. Disable transaction logs.  

### 80.

A target table is partitioned by ingestion date, but queries filter by event date. What should be evaluated?

A. Store event date only in a text blob.  
B. Remove date filters from reports.  
C. Add more ingestion-date partitions regardless of query patterns.  
D. Whether partitioning and indexes match dominant query predicates and retention needs.  

## 9. Governance, security, and privacy

### 81.

An export contains customer names and contact details. What is appropriate before creating a new development copy?

A. Confirm authorization and data classification, minimize fields, and use approved masking or synthetic data where possible.  
B. Assume test environments are automatically exempt from privacy rules.  
C. Include the data in a public bug report.  
D. Upload it to a personal file-sharing account.  

### 82.

A database credential is needed by an ETL worker. Where should it be stored?

A. In a log line for troubleshooting.  
B. In the source code repository for easy deployment.  
C. In an approved secret manager with scoped access and rotation.  
D. In a command-line argument visible to all process users.  

### 83.

A customer asks for a full raw-data retention period but contract terms are unclear. What should the FDE do?

A. Confirm retention and deletion obligations with the accountable owner before setting storage policy.  
B. Keep everything forever to avoid future work.  
C. Copy raw data to another system with fewer controls.  
D. Delete data immediately without confirming operational or legal requirements.  

### 84.

A pipeline crosses a tenant boundary in a shared warehouse. Which is most important?

A. Hide tenant names in the UI but keep unrestricted queries.  
B. Enforce tenant isolation in access policies and query paths, and test for cross-tenant leakage.  
C. Randomize table names daily.  
D. Rely on users not guessing another tenant ID.  

### 85.

A record contains a customer-provided SQL string. What should a query builder do?

A. Bind values as parameters and allowlist any dynamic identifiers; never concatenate untrusted values into SQL.  
B. Place the string in a comment and run it.  
C. Encode it as Base64 and concatenate it.  
D. Execute the string as a query because the customer supplied it.  

### 86.

A user requests deletion of their source document. What should the pipeline support?

A. Rename the file so the request appears complete.  
B. Delete only the UI link and keep all copies without review.  
C. Trace derived copies/indexes and apply an auditable deletion or retention workflow across systems.  
D. Ignore the request because data was already transformed.  

### 87.

An integration logs every request body for debugging. What is the concern?

A. Request bodies cannot contain personal information.  
B. Full payload logging automatically improves data quality.  
C. Logs are always encrypted so no controls are needed.  
D. Logs may expose sensitive data and credentials; minimize, redact, and control retention/access.  

## 10. Validation, lineage, and handoff

### 88.

A new transformation is ready. Which test sequence provides useful confidence?

A. Skip tests and compare screenshots after release.  
B. Only check that the process exits with code zero.  
C. Unit tests for rules, contract tests for schemas, representative integration fixtures, and end-to-end reconciliation.  
D. Test only one clean row from a hand-built file.  

### 89.

A customer asks how a dashboard total was produced. What should be available?

A. Lineage from source/version and transformation rules to output, with run metadata and quality results.  
B. A promise that the model generated the total correctly.  
C. A random sample of raw rows without context.  
D. Only the name of the last person who opened the dashboard.  

### 90.

A backfill changes historical totals. What is the best release practice?

A. Compare old/new outputs, quantify the impact, document the reason, and get appropriate customer sign-off.  
B. Replace historical data without notice.  
C. Disable the totals until no one asks about them.  
D. Keep both totals under the same label.  

### 91.

A pipeline reports success although some partitions were skipped. What should success mean?

A. Logs contain no Python traceback, regardless of missing partitions.  
B. All required partitions meet explicit completion/quality criteria, with partial status surfaced separately.  
C. Any nonzero row count is complete success.  
D. The process ran for at least one minute.  

### 92.

A field mapping changes from source `cust_no` to target `customer_id`. What should the change record include?

A. The developer's guess about what the fields mean.  
B. Only the new field's color in the UI.  
C. No documentation if the code compiles.  
D. Source/target semantics, transformation, owner, version/effective date, and validation evidence.  

### 93.

A reconciliation finds 2% fewer target rows than source rows. What is the best response?

A. Break down counts by interval/status/key and investigate expected filters, rejects, and duplicates.  
B. Ignore the gap if the dashboard looks plausible.  
C. Change the reconciliation query until counts match.  
D. Add 2% random rows to match the count.  

### 94.

A deployment needs a rollback after a target schema change. What should have been planned?

A. A compatible migration/rollback path, backup or recovery option, and clear data reconciliation steps.  
B. A manual deletion of every new row.  
C. Only a screenshot of the schema.  
D. A promise that the database never needs rollback.  

### 95.

A source system changes its business rule but keeps the same field name. How can downstream teams detect the semantic change?

A. Randomly rename the target field every month.  
B. Rely on the column name to encode all future meaning.  
C. Maintain ownership/change communication and monitor contract-level distributions or invariants.  
D. Stop profiling data after initial launch.  

### 96.

A pipeline has a data-quality threshold of 5% rejects. What should happen when it reaches 12%?

A. Disable the metric to avoid future alerts.  
B. Mark all rejected rows as valid.  
C. Raise the threshold silently to 15%.  
D. Stop or quarantine according to policy, alert owners, and expose impact before publishing misleading output.  

### 97.

A customer wants to reproduce yesterday's output after code changed. What metadata is needed?

A. The engineer's current laptop clock.  
B. Code/config version, source interval and snapshot, dependency versions, and run parameters.  
C. A screenshot of the output without run identifiers.  
D. Only the current source table contents.  

### 98.

A source sends a `last_updated` timestamp with only second-level precision. Several updates may occur in one second. What is a robust approach?

A. Assume only one update can occur per second.  
B. Combine timestamp with a stable sequence/key or use CDC/overlap and deduplication.  
C. Use the destination load time as the source change order.  
D. Round timestamps to the nearest minute and discard ties.  

### 99.

An ETL job sends data to an external analytics service. Which control should be verified before launch?

A. Approved destination, minimum required fields, access control, retention, and transfer/security requirements.  
B. Whether the job can send the largest possible payload.  
C. Whether the destination's logo matches the source.  
D. Whether all internal users can see the export.  

### 100.

An ingestion is live. What is the strongest routine operating review?

A. Wait for customer complaints before reviewing pipeline health.  
B. Check only whether the scheduler process exists.  
C. Track freshness, volume, quality/rejects, latency, failures, cost, and ownership/runbook readiness.  
D. Read the entire raw dataset every morning.  
