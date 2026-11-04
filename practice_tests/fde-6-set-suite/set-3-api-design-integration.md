# FDE Practice Set 3: API Design and Integration Patterns

**Format:** 100 original, single-best-answer questions  
**Suggested time:** 150 minutes (a self-imposed pacing target)  
**Scoring:** 1 point per question; raw percentage = `correct ÷ 100 × 100`.

> Unofficial study material based on the Udemy course's public topic outline, not its paid questions or assignments. FDE roles and interview formats vary by employer. This set is not endorsed by Udemy or an employer and is not a hiring prediction.

**Instructions:** Choose one best answer for each question. Complete this file before opening the [separate answer key](set-3-api-design-integration-answer-key.md).

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

## 1. HTTP semantics and resource design

### 1.

A client creates a new shipment and needs its canonical URI. Which response is most appropriate after successful creation?

A. `404 Not Found` with the new shipment ID.  
B. `201 Created` with a `Location` or resource representation.  
C. `204 No Content` for every successful request.  
D. `302 Found` to an unrelated page.  

### 2.

A client retries a request to replace a resource at a known URI. Which method is generally idempotent by HTTP semantics?

A. `PUT`, when repeated requests apply the same intended replacement.  
B. `POST`, for every possible operation.  
C. `CONNECT`, for all data writes.  
D. `TRACE`, for resource creation.  

### 3.

A request is valid and accepted for asynchronous processing, but work is not complete. Which response fits?

A. `202 Accepted`, with an operation/status reference where useful.  
B. `500 Internal Server Error` by definition.  
C. `401 Unauthorized` for every queued operation.  
D. `200 OK` claiming the final result is complete.  

### 4.

A successful DELETE has no response body. Which status is commonly appropriate?

A. `301 Moved Permanently`.  
B. `418 I'm a teapot`.  
C. `204 No Content`.  
D. `407 Proxy Authentication Required`.  

### 5.

A client must avoid overwriting a resource changed since it was read. Which HTTP mechanism can help?

A. An unbounded retry count.  
B. A random query parameter.  
C. A CSS class on the response.  
D. ETag with conditional `If-Match` update.  

### 6.

A client polls a resource and the representation has not changed. Which mechanism can reduce payload transfer?

A. Disabling response compression and validators.  
B. Sending the entire object in every request body.  
C. Conditional GET using `ETag`/`If-None-Match` or a date validator.  
D. Replacing GET with DELETE.  

### 7.

An endpoint returns `200` with `{"error":"permission denied"}` for forbidden access. What is the issue?

A. The response needs a larger JSON body.  
B. Permission failures should be hidden as successful empty data.  
C. The HTTP status misrepresents the outcome; use an appropriate 4xx status and stable error contract.  
D. Error objects must always return status 200.  

### 8.

An API exposes `/getAllOrdersNow`. What is a more resource-oriented design?

A. Require a shell command in the query string.  
B. Use a collection resource such as `GET /orders` with documented filters and pagination.  
C. Put the entire order database in the URL path.  
D. Use `DELETE /orders` to list records.  

### 9.

A list endpoint may return millions of records. What should it support?

A. Bounded pagination and filters with documented limits.  
B. One request per field with no limit.  
C. A client-side loop that guesses the server's row count.  
D. An unbounded response body by default.  

### 10.

A request body fails validation. Which response is clearest?

A. `200 OK` with a server stack trace.  
B. A suitable 4xx status with stable machine-readable error details that avoid leaking internals.  
C. `204 No Content` and no indication of failure.  
D. A redirect to an administrator's login page for every client.  

## 2. Authentication, authorization, and tenant isolation

### 11.

A bearer token is sent in a URL query parameter. What is the main concern?

A. Query strings are encrypted by default beyond TLS.  
B. Tokens in URLs expire automatically after one request.  
C. URLs are commonly logged or propagated, exposing credentials; send tokens via an approved header or secure mechanism.  
D. The API cannot parse URLs with tokens.  

### 12.

A client is authenticated but requests another customer's record ID. What must the server check?

A. Whether the request uses JSON rather than XML.  
B. Object-level authorization for that caller and specific record.  
C. Only whether the record ID is a valid UUID.  
D. Whether the caller's browser hides the ID.  

### 13.

A service needs to call another API as a workload identity. What credential pattern is preferred?

A. A developer's personal password embedded in the binary.  
B. An unauthenticated endpoint restricted only by obscurity.  
C. A scoped service identity with managed rotation/short lifetime and minimum required permissions.  
D. One shared administrator token sent to every user.  

### 14.

A client-supplied `tenant_id` selects the database schema. What should the service do?

A. Remove authentication to reduce latency.  
B. Trust any syntactically valid tenant ID.  
C. Ask the model to decide whether the tenant is correct.  
D. Derive tenant scope from trusted identity/context and authorize each operation server-side.  

### 15.

A token has a role claim that may be revoked during the token lifetime. What should the design consider?

A. Assume a signed token can never become stale.  
B. Token lifetime, revocation/refresh strategy, and sensitive-operation authorization requirements.  
C. Store the token in the database as a permanent password.  
D. Ignore revocation for all actions.  

### 16.

Two services need different permissions from the same identity provider. What is best?

A. Give every service the same global administrator scope.  
B. Remove audience validation.  
C. Distinct least-privilege scopes/audiences or identities per service capability.  
D. Use one user token for all background workloads indefinitely.  

### 17.

A public API supports password login. Which control is important in addition to password verification?

A. Secure transport, rate limits/abuse controls, safe credential storage, and session/token lifecycle controls.  
B. Disable account recovery so no one can change credentials.  
C. Use the username as the password hash.  
D. Store passwords in logs to support support staff.  

### 18.

A user may read but not update a case. How should the API enforce this?

A. Encode the update URL in Base64.  
B. Hide the update button and trust the client not to call the endpoint.  
C. Use a different font for read-only users.  
D. Check action-specific permissions on the server for each request.  

### 19.

An API key was accidentally committed to a public repository. What is the immediate response?

A. Delete the latest commit and assume nobody copied it.  
B. Revoke/rotate it, assess use, remove exposure where possible, and follow incident procedures.  
C. Wait for the key's normal expiry without checking exposure.  
D. Rename the variable but keep using the same key.  

### 20.

A service returns different errors for “user exists” and “user not found” during password reset. What risk can this create?

A. Load-balancer stickiness.  
B. Account enumeration; use a response that avoids revealing whether an account exists.  
C. SQL serialization failure.  
D. Request compression mismatch.  

## 3. Contracts, schemas, and versioning

### 21.

A response field is renamed and existing clients break. What should the API team do?

A. Remove the field from all versions immediately.  
B. Rename it silently again next week.  
C. Define a version/deprecation migration, preserve compatibility during a window, and measure consumer adoption.  
D. Tell clients to parse undocumented positional fields.  

### 22.

A new response field is optional. What is the safest rollout expectation?

A. Document it as optional and verify older clients tolerate unknown fields or use versioned contracts.  
B. Return it only when the server randomly chooses.  
C. Change the meaning of an existing field without notice.  
D. Require all clients to send it in requests immediately.  

### 23.

An API specification should describe request/response shapes and operations. Which format is commonly used for HTTP APIs?

A. PNG.  
B. A screenshot of the API console.  
C. CSV with no schema.  
D. OpenAPI.  

### 24.

A client and server disagree on whether a timestamp is local time or UTC. What belongs in the contract?

A. The developer's current operating-system timezone.  
B. Only the word “timestamp.”  
C. An assumption that all clients use the same locale.  
D. Explicit format, timezone semantics, precision, and examples.  

### 25.

A response includes a numeric amount but omits currency. What contract change is appropriate?

A. Assume every customer uses the same currency.  
B. Include currency or define an unambiguous currency context and decimal precision.  
C. Store the amount in an arbitrary integer field.  
D. Format the amount as a localized string only.  

### 26.

A client needs a stable error code across languages and releases. What should the API provide?

A. A randomly generated error label for each request.  
B. A localized sentence that clients must parse exactly.  
C. A documented machine-readable code plus safe message and relevant field details.  
D. A raw stack trace.  

### 27.

A schema uses a field both as “customer reference” and “free-form note.” What is the issue?

A. JSON cannot represent more than one field.  
B. The endpoint needs a larger port number.  
C. Free text should always be treated as an identifier.  
D. The contract mixes distinct semantics; split fields and define types/constraints.  

### 28.

A v2 API should coexist with v1 temporarily. What is important?

A. Return v1 fields from v2 without documenting differences.  
B. Track version usage, security fixes, support window, migration guidance, and removal criteria.  
C. Disable monitoring on v1.  
D. Keep both versions forever with no owner.  

### 29.

A consumer depends on undocumented ordering in a response array. What should the API team do?

A. Either document and test stable ordering or state that order is unspecified so clients do not rely on it.  
B. Change order every request to expose the dependency.  
C. Sort by memory address.  
D. Remove the endpoint without notice.  

### 30.

A numeric field may exceed a 32-bit client range. What should schema design address?

A. Encode values as colors.  
B. Range/precision constraints and client compatibility, with safe representation or migration if needed.  
C. Assume every client uses arbitrary-precision integers.  
D. Truncate high values without notice.  

## 4. Pagination, filtering, and rate limits

### 31.

A collection changes while clients paginate using offsets. What can reduce missed/duplicated records?

A. Randomize offset values between requests.  
B. Sort by a non-unique mutable label only.  
C. Cursor/keyset pagination over a stable ordered key or a snapshot boundary.  
D. Stop returning the next-page token.  

### 32.

A page token contains internal database details in readable form. What is safer?

A. Publish the raw SQL query in the token.  
B. Use a user's password as the cursor.  
C. Use an opaque, integrity-protected token or server-side cursor with expiry and scope checks.  
D. Let clients modify the token to access any partition.  

### 33.

A list API accepts arbitrary `limit=1000000000`. What control is needed?

A. Allocate memory for the requested limit immediately.  
B. Validate and cap page size server-side, with sensible defaults and rate/resource limits.  
C. Trust the client because it is authenticated.  
D. Return the full database.  

### 34.

A filter uses SQL-like expressions supplied by clients. What is safer?

A. Run it as a shell command.  
B. Parse a constrained allowlisted filter grammar and bind values, rather than executing arbitrary SQL.  
C. Disable authentication for filtered calls.  
D. Concatenate the expression directly into a query.  

### 35.

An API applies a per-user rate limit, but one user can create many accounts. What else may be needed?

A. Additional limits by identity, tenant, IP/device, business flow, and cost, with abuse review.  
B. Trust each account to be unique forever.  
C. Remove all rate limits.  
D. Use response content length as the only control.  

### 36.

A client receives 429 with `Retry-After`. What is expected behavior?

A. Retry immediately in a tight loop.  
B. Treat it as a completed success.  
C. Rotate identities to evade the limit.  
D. Honor the delay, apply backoff/jitter, and avoid retrying beyond a bounded policy.  

### 37.

A cursor API must support repeatable exports. What feature can help?

A. Use a random order on every call.  
B. Recompute offsets from the current live table each page.  
C. A snapshot/version boundary tied to the cursor or export job.  
D. Omit stable sort keys.  

### 38.

A filter can return records for any tenant if `tenant_id` is supplied. What is the correct behavior?

A. Trust the filter if the tenant ID is a UUID.  
B. Let users download all tenants and sort locally.  
C. Hide the tenant filter in the UI only.  
D. Validate tenant access from the authenticated context and constrain the query server-side.  

### 39.

A server must support sorting by user-specified column. What is safe?

A. Allow any expression from the request body.  
B. Ignore authorization whenever sorting is requested.  
C. Paste the raw column name into SQL.  
D. Map allowed sort keys to known columns and validate direction; do not interpolate arbitrary identifiers.  

### 40.

A client repeatedly downloads unchanged data. What API feature can reduce bandwidth?

A. Disable caching headers.  
B. More frequent full downloads.  
C. Conditional requests with ETag or last-modified validators.  
D. Random response compression on every request.  

## 5. Idempotency, webhooks, and event delivery

### 41.

A client times out after creating a payment. How can it safely retry?

A. Ask the user to click repeatedly until one succeeds.  
B. Generate a different key for every retry.  
C. Retry with no request identity.  
D. Send a stable idempotency key and have the server atomically associate it with the operation/result.  

### 42.

A webhook signature is supplied in a header. What should the receiver verify?

A. Trust the source IP alone and ignore the signature.  
B. Verify only after applying the side effect.  
C. Verify a cryptographic signature over the raw payload using the expected secret/key and compare safely.  
D. Decode the signature as a URL and execute it.  

### 43.

A webhook provider retries delivery. What response should a receiver return after durable acceptance?

A. Return 500 for every valid event so the provider retries forever.  
B. Return success before any durable capture and discard the event.  
C. A successful acknowledgement promptly, then process asynchronously if needed with deduplication.  
D. Keep the connection open until every downstream workflow finishes.  

### 44.

A webhook arrives before the API can look up the referenced object. What should the integration do?

A. Drop the event because the lookup failed once.  
B. Fabricate the missing object.  
C. Persist the event, retry lookup with bounded backoff, and expose unresolved state.  
D. Mark it complete without verification.  

### 45.

A client sends an idempotency key but reuses it for a different payload. What should the server do?

A. Detect the mismatch and reject or define deterministic conflict behavior.  
B. Silently execute both operations under one key.  
C. Replace the original request body and hide the change.  
D. Disable all idempotency checks.  

### 46.

A webhook event contains a timestamp from the sender. What additional check helps prevent replay?

A. Verify signature, enforce a freshness window where appropriate, and deduplicate event IDs durably.  
B. Trust timestamps without checking signature.  
C. Accept every duplicate if the body is valid JSON.  
D. Compare only the sender's display name.  

### 47.

A payment provider sends the same event ID with a later correction event. How should the API distinguish them?

A. Use unique event identity plus version/correction semantics from the provider contract.  
B. Treat all messages as the same event regardless of version.  
C. Drop every event that shares a payment ID.  
D. Infer correction from the text length.  

### 48.

An API operation is not naturally idempotent, such as incrementing a counter. What can make retries safe?

A. A durable request key/result record or a uniquely identified command processed once.  
B. A shorter timeout only.  
C. A random delay before every retry.  
D. Hiding the counter value.  

### 49.

A consumer must handle events in order per account. What should be specified with the producer?

A. The UI theme.  
B. Ordering key/sequence semantics and behavior for gaps, duplicates, and late events.  
C. Only a JSON indentation style.  
D. That messages arrive in global order without a guarantee.  

### 50.

A webhook receiver processes a valid event but crashes before acknowledging. What should happen on redelivery?

A. Repeat the payment every time.  
B. Deduplication should recognize completed work and return a success acknowledgement without repeating side effects.  
C. Reject all future events from the provider.  
D. Delete the event history.  

## 6. Synchronous, asynchronous, and integration patterns

### 51.

A request can finish in 30 seconds but the client connection may be shorter-lived. What pattern is suitable?

A. Return success before saving the request.  
B. Ask the client to submit repeatedly until finished.  
C. Accept a durable job, return an operation ID, and expose status/result retrieval.  
D. Hold every connection open without a timeout.  

### 52.

A downstream service is required for every synchronous call and often times out. What is a useful safeguard?

A. Remove dependency monitoring.  
B. Retry at maximum rate.  
C. Infinite wait and retry.  
D. Deadline-aware timeout, circuit breaker, and a business-safe fallback or error.  

### 53.

A legacy system supports only nightly CSV exchange. What is a practical integration pattern?

A. Directly rewrite the legacy system before any discovery.  
B. Poll the file share every millisecond.  
C. Parse files without a schema or archive.  
D. A scheduled adapter that validates, stages, reconciles, and reports each file exchange.  

### 54.

A service must notify three consumers when an order changes. What does a broker/topic provide?

A. Decoupled event distribution with consumer-specific processing and delivery semantics.  
B. A single synchronous call to every consumer forever.  
C. Automatic cross-service transaction guarantees in all cases.  
D. A replacement for authorization.  

### 55.

A customer asks for “real-time” updates. What should be clarified?

A. Assume every event arrives instantly and exactly once.  
B. Freshness target, event source, delivery latency, ordering, and behavior during disconnection.  
C. Only the color of the status indicator.  
D. Use a daily batch without disclosure.  

### 56.

A poller sends the same query every second even when data changes hourly. What may be better?

A. Webhooks, CDC, or longer adaptive polling if the source supports them and semantics fit.  
B. Replicate the entire source database to every client.  
C. Add more pollers at one-second intervals.  
D. Remove source rate limits.  

### 57.

A client needs to know whether an async job is complete. What should the API expose?

A. A log file path on the server's local disk only.  
B. No status because queues are internal.  
C. A stable job resource with status, timestamps, progress where meaningful, result/error, and retention policy.  
D. A success toast before the job starts.  

### 58.

A service calls a legacy dependency that returns inconsistent field formats. What is the adapter's role?

A. Rewrite the dependency's database directly.  
B. Validate and normalize the external contract into a stable internal representation while preserving source errors.  
C. Spread legacy quirks into every application layer.  
D. Ignore malformed values and return success.  

### 59.

A request fans out to multiple independent read-only sources. What can reduce end-user latency?

A. Call every source sequentially with no deadline.  
B. Repeat each call ten times.  
C. Remove all source-specific errors.  
D. Parallelize bounded calls with per-dependency timeouts and partial-result semantics defined.  

### 60.

A system synchronizes changes in both directions between two sources. What must be designed carefully?

A. Disable source change tracking.  
B. Assume every update has one origin.  
C. Conflict resolution, ownership, loop prevention, versioning, and reconciliation.  
D. Copy whichever record is read last without audit.  

## 7. Validation, errors, and safe request handling

### 61.

An API accepts an order quantity. Which validation belongs at the server boundary?

A. Type, range, requiredness, business constraints, and authorization for the requested operation.  
B. Whether the number is visually centered.  
C. Only whether the browser rendered the input field.  
D. No validation if the request is authenticated.  

### 62.

A request contains an unknown JSON field. What policy is best?

A. Always assign them to administrator permissions.  
B. Execute unknown fields as code.  
C. Define whether unknown fields are rejected or ignored, keep behavior consistent, and test compatibility.  
D. Silently reinterpret known fields.  

### 63.

An API reports validation errors. Which detail is useful and safe?

A. A generic success response.  
B. Stable field/code references and corrective guidance without stack traces or sensitive values.  
C. Database credentials to help reproduce the issue.  
D. Full server filesystem paths and secret values.  

### 64.

A server fetches a URL supplied by a client. What risk should be addressed?

A. CSS injection in the response headers only.  
B. SSRF; validate allowed schemes/hosts/addresses, block internal destinations, and constrain redirects/egress.  
C. SQL grouping only.  
D. Unicode normalization only.  

### 65.

A request body is 500 MB. What should the API do?

A. Disable request timeouts.  
B. Accept it because TLS compresses every body.  
C. Enforce documented body-size/resource limits and use a separate upload workflow if large files are supported.  
D. Buffer unlimited content in memory.  

### 66.

A client submits an invalid enum value. How should the endpoint respond?

A. Reject with a stable validation error and document allowed values.  
B. Convert it to an arbitrary allowed value.  
C. Return a success and silently discard the field.  
D. Store it as administrator status.  

### 67.

A PATCH endpoint receives only `status`. What semantic issue must be specified?

A. Whether the user's screen is wide enough.  
B. Whether all omitted fields become zero by default.  
C. Whether PATCH means resource deletion.  
D. Whether omitted fields remain unchanged and whether explicit null clears a value.  

### 68.

An API uses `200` for both “no results” and “request failed.” What should change?

A. Put the status only in an undocumented string.  
B. Treat every response as success.  
C. Return HTTP 500 for empty collections.  
D. Use success status for a valid empty result and appropriate 4xx/5xx statuses for failures.  

### 69.

A service returns a database exception to the client. What is safer?

A. Remove all logs and IDs.  
B. Tell the client to retry forever.  
C. Return the full SQL, credentials, and stack trace.  
D. Return a generic stable error and correlation ID; retain sanitized diagnostic detail in restricted logs.  

### 70.

A client sends an excessively deep nested JSON object. What should the server consider?

A. Unlimited parser recursion.  
B. Limits on payload size/depth/complexity and time, plus clear validation behavior.  
C. Executing nested strings as scripts.  
D. Disabling request validation.  

## 8. API security and abuse resistance

### 71.

A user can change `/invoices/123` to `/invoices/124` and see another person's invoice. Which API risk is present?

A. Broken object-level authorization.  
B. Excessive schema versioning.  
C. Incorrect CSS caching.  
D. Missing response compression.  

### 72.

An endpoint is accessible to ordinary users but performs an admin-only action. What control is missing?

A. A larger rate limit.  
B. A comment in the endpoint code only.  
C. A longer JSON property name.  
D. Function-level authorization enforced on the server.  

### 73.

A public API triggers paid SMS for every request. What abuse control is needed?

A. More expensive SMS messages to discourage users.  
B. No limits because each request is syntactically valid.  
C. Hide the endpoint from documentation but keep it public.  
D. Business-flow limits, quotas, anomaly monitoring, and cost-aware authorization.  

### 74.

A third-party API response is assumed safe and inserted into HTML. What should the client do?

A. Treat external content as untrusted, validate/encode for its output context, and handle errors safely.  
B. Disable content security controls.  
C. Execute returned script to confirm the schema.  
D. Trust it because it came from an API.  

### 75.

An API has old debug endpoints left deployed. What governance helps prevent exposure?

A. Rely only on endpoint names being obscure.  
B. Inventory deployed routes/versions, remove deprecated endpoints, and test production configuration.  
C. Assume inactive routes cannot be called.  
D. Add more undocumented endpoints.  

### 76.

A service uses permissive CORS and wildcard origins with credentials. What should be reviewed?

A. Add all origins by default.  
B. Disable authentication to match CORS.  
C. CORS protects server-to-server authorization by itself.  
D. Restrict allowed origins/methods/headers to the intended browser clients and avoid unsafe credentialed wildcards.  

### 77.

An API accepts user-controlled file URLs and downloads them server-side. Which protections are relevant?

A. Store the returned bytes as executable code.  
B. Allowlist destinations, validate DNS/IP after resolution and redirects, limit size/time, and scan content.  
C. Permit all private IP ranges.  
D. Follow redirects without limit.  

### 78.

An API key is intended only for one customer integration. How should it be scoped?

A. Put the same key in every sample application.  
B. Restrict tenant, operations, environment, expiry, and usage; support revocation and rotation.  
C. Grant global admin access for convenience.  
D. Make the key permanent and unlogged.  

### 79.

A password reset endpoint returns whether an email is registered. What should be considered?

A. The database should store plaintext passwords.  
B. Rate limiting is never relevant to reset flows.  
C. The endpoint should publish all valid addresses.  
D. Account-enumeration risk; make responses and timing sufficiently uniform while preserving usable flow.  

### 80.

An API exposes sensitive data in query strings. What is a better approach?

A. Keep sensitive values out of URLs; use a protected request body/header and avoid logging secrets.  
B. Add the values to DNS names.  
C. Encode the values with Base64 and leave them in the URL.  
D. Increase the URL length limit.  

## 9. Testing, documentation, and observability

### 81.

A consumer team changes its request schema. What test can catch compatibility breakage before release?

A. Only load testing the database.  
B. A manual check months after release.  
C. A screenshot comparison of the code editor.  
D. Consumer/provider contract tests in CI using agreed schemas and examples.  

### 82.

An OpenAPI document does not match the running API. What is the risk?

A. Documentation mismatch improves versioning.  
B. Clients generate incorrect integrations and security reviewers miss actual behavior.  
C. The API automatically repairs itself.  
D. The network becomes more reliable.  

### 83.

An API test suite uses only mocks. What is missing?

A. The source-code license.  
B. A color legend for endpoints.  
C. More mock-only tests that never validate assumptions.  
D. Contract/integration tests against representative service behavior and failure modes.  

### 84.

A request crosses gateway, API, worker, and database. What telemetry is useful?

A. Propagated trace context, structured sanitized logs, latency/error metrics, and correlation IDs.  
B. A success counter only.  
C. Full request secrets written to each log.  
D. Separate uncorrelated log files with no timestamps.  

### 85.

A client reports intermittent 503s. What should the API error include?

A. A full stack trace and all environment variables.  
B. A success body that omits the failure.  
C. No response and no server log.  
D. Stable error code and correlation/request ID, with safe retry guidance if appropriate.  

### 86.

An API has a breaking change planned. Which communication is most useful?

A. A release note saying “API updated.”  
B. A private message only to the original author.  
C. Migration guide, dates, examples, compatibility window, and usage telemetry/consumer contact path.  
D. No notice until clients fail.  

### 87.

A test suite needs to validate rate limits. What should it assert?

A. Limits, response status/headers, reset behavior, and that normal traffic remains usable.  
B. That every 429 becomes a 200.  
C. That all rate-limit counters are disabled in production.  
D. That the test can send unlimited requests.  

### 88.

An API's p99 latency rises after a release. Which comparison is most useful?

A. Segment traces/metrics by endpoint, dependency, version, and request shape against the prior baseline.  
B. Compare only average latency across all traffic.  
C. Ask every user to estimate response time from memory.  
D. Delete the new release's metrics.  

### 89.

A generated client library is published. What should accompany it?

A. Versioned spec/source, supported runtime matrix, examples, auth setup, and compatibility notes.  
B. A hard-coded production credential.  
C. A binary with no version number.  
D. A guarantee that every future API change is compatible.  

### 90.

An API receives a burst of retries after an outage. What telemetry helps assess recovery?

A. The number of UI icons.  
B. The number of lines in the deployment script.  
C. Request rate, 429/5xx rates, retry counts, latency, saturation, and queue/backlog age.  
D. Only the API's DNS name.  

## 10. Integration design scenarios

### 91.

A partner sends a daily CSV and also offers a webhook. Which design choice is best?

A. Always use the webhook without examining guarantees.  
B. Reject all data until the partner rewrites its system.  
C. Compare freshness, completeness, cost, recovery, and duplicate semantics; select or combine feeds with reconciliation.  
D. Use both blindly and double every record.  

### 92.

A client's endpoint is intermittently unavailable during a workflow. What should the API return to its caller?

A. A raw database password.  
B. A clear dependency/unavailable outcome or accepted job state, with correlation and safe retry semantics.  
C. The other customer's data.  
D. A fabricated successful result.  

### 93.

A legacy SOAP system must be integrated with a modern REST API. What is a suitable design?

A. Expose SOAP credentials in browser code.  
B. An adapter translating protocols and models, with explicit error/timeout mapping and tests.  
C. Let each client call both systems directly.  
D. Convert every SOAP fault to success.  

### 94.

A client needs a large export once per week. What API design may fit better than paginating millions of records synchronously?

A. A single response with unlimited memory buffering.  
B. A text message containing all rows.  
C. A hidden database dump endpoint with no access checks.  
D. An authorized asynchronous export job with status, bounded artifact access, expiry, and audit.  

### 95.

A third-party API may return duplicate records across pages. What should the importer do?

A. Deduplicate using stable identity/version semantics and reconcile counts, not rely solely on page boundaries.  
B. Drop all records from later pages.  
C. Assume duplicate pages are impossible.  
D. Treat every duplicate as a new entity.  

### 96.

An API request triggers a workflow with irreversible steps. What should happen before accepting it?

A. Start irreversible actions before validating the request.  
B. Let a prompt decide access rights.  
C. Return success before saving any operation state.  
D. Validate authorization and input, establish idempotency/approval requirements, and persist a traceable job state.  

### 97.

A callback URL is supplied by a tenant and the service posts results to it. What should be checked?

A. Destination allowlist/egress rules, tenant ownership, authentication/signing, and retry/SSRF protections.  
B. Nothing; callbacks are always trusted.  
C. Allow callbacks to private metadata endpoints by default.  
D. Put credentials in the callback URL.  

### 98.

A client needs to update only fields it owns. What API design helps prevent mass assignment?

A. Deserialize every JSON field directly into the database model.  
B. Hide fields only in the UI.  
C. Explicit writable-field allowlists and server-side property-level authorization.  
D. Give clients the database password.  

### 99.

An API migration requires both old and new payload formats for a period. What is safest?

A. Never measure which versions are used.  
B. Guess the payload format from whitespace.  
C. Version/translate at a clear boundary, test both contracts, monitor usage, and publish an end-of-support date.  
D. Mix fields from both versions randomly.  

### 100.

A production API has an undocumented admin endpoint. What is the correct response?

A. Inventory and restrict/remove it, assess exposure, document intended routes, and verify deployment configuration.  
B. Keep it public because clients do not know the URL.  
C. Add the route to an internal wiki only.  
D. Rename it to a longer path and leave authorization unchanged.  
