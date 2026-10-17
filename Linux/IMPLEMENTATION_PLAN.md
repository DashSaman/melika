# Iran Smart Mirror P0 Implementation Plan

> **For agentic workers:** Use the installed `superpowers:executing-plans` skill for inline execution, or `superpowers:subagent-driven-development` when independent agents are actually available. Do not pretend unavailable tools ran. Steps use checkboxes and are not marked complete by this research.

**Goal:** Build a limited Ubuntu 24.04 amd64 artifact gateway with evidence-aware routing, verified metadata, a small local fallback store, and an independently testable offline profile.

**Architecture:** A domestic Nginx edge fronts a FastAPI application and local verified metadata/content. SQLite and one worker maintain source evidence and a catalog. Remote immutable artifacts use reviewed 302 redirects; Rubika is disabled until its separate gates pass.

**Tech Stack:** Python 3.12, FastAPI, Jinja2, sqlite3/WAL, native APT/gpgv, python-debian, Nginx, Docker Compose. Dependency versions and image digests are resolved and locked from actual available releases during implementation, not invented here.

**Spec:** [ARCHITECTURE.md](ARCHITECTURE.md), [API_CONTRACT.md](API_CONTRACT.md), [SECURITY_AND_OFFLINE.md](SECURITY_AND_OFFLINE.md).

## Global Constraints

- Change only `Linux/`; preserve all repository-root and unrelated seminar files. Read `Linux/AGENTS.md` and inspect current head/dirty state before work.
- P0 target: `noble`, `noble-updates`, `noble-security`; component `main`; architecture `amd64` and relevant `all` packages. Seed list is in Task 4.
- No signature, date or TLS bypass; no arbitrary-URL endpoint; no private API userbot; no purchases or account creation without specific authority.
- All 27 registry entries start disabled. Documentation alone cannot approve production routing or domestic residency.
- One app process and one scheduler writer. Sample probes: 4 global/1 per source, 10s request timeout, 4096B body, 1000/day global, 1s host interval. Full verification: 1GiB/day and 512MiB per artifact by default. Persist budgets.
- Health TTL 300s, artifact availability TTL 3600s. Metadata cap 1GiB, CAS cap 5GiB. Never evict pinned/live objects to make a test pass.
- Production DNS resolution and total job time must be bounded in addition to socket connect/read. The research probe is not a substitute for a production fetch subsystem.
- `gateway_preview` and `apt_profile_accepted` are separate states. Only real clean-client evidence can set the latter. Blockers do not justify weakening controls.

## Review Focus

1. A 200 HTML login/error page or invalid Content-Range must not become a verified artifact: Task 2 tests.
2. Concurrent metadata publication and old by-hash requests must preserve the correct bytes and trusted mappings: Task 3 tests.
3. Package resolution must not succeed only because the test host already has hidden cached dependencies: Task 4 clean-baseline test.
4. Redirect-after-response failure must be reported honestly rather than advertised as automatic midstream failover: Task 5 test.
5. Service restart during an outage must not need Docker Hub, pip, remote JavaScript, DNS or an external login: Task 7 cold-start test.

## Scope and effort budget

This is a planning allocation, not a promise that all external approvals and transfer/observation tests fit in one day.

| Stage | Engineering budget | Gate |
|---|---:|---|
| 1. Scope, configuration, schema | 1h | Safe default-disable state and migration tests |
| 2. Guarded networking and probes | 1.5h | SSRF/Range/quota tests |
| 3. Signed metadata and catalog | 2h | Tamper, by-hash and atomic-publication tests |
| 4. Profile and gap logic | 1h | Deterministic closure manifest and classifications |
| 5. API, UI and downloads | 1.5h | Router/local-store/API tests |
| 6. Scheduler, audit, backup | 1h | Deduplication, persistence and restoration |
| 7. Compose and acceptance | 1.5h | Local integration; real network gate only when available |
| Contingency | 1–2h | Fix highest-risk failures; defer P1 rather than fake success |

Total planned effort: **10.5–11.5h**. A blocked provider/host/permission, large metadata transfer, Rubika TTL observation or multi-ISP test may remain open. Ship a tested preview and clear blockers rather than mislabel an incomplete mirror.

## File map

Create product files under the following paths; retain the research probe and its existing tests:

```text
Linux/
  app/
    __init__.py
    main.py                 # FastAPI routes and dependency wiring
    models.py               # typed cross-module contracts
    config.py               # YAML validation and default merge
    db.py                   # migrations and transactions
    migrations/001.sql
    netguard.py             # allowed/pinned network access
    probes.py               # observations and full-digest verification
    aptmeta.py              # gpgv, bounded index import, atomic publication
    catalog.py              # artifact/path lookup
    profiles.py             # native APT plan import and baseline evidence
    routing.py              # deterministic eligible-source selection
    gaps.py                 # available/fragile/missing/unknown classification
    storage.py              # verified Local CAS and disabled Rubika adapter
    scheduler.py            # jobs, leases and persistent budgets
    cli.py                  # local administration
    templates/index.html
    static/site.css
  tests/
    test_probe_sources.py   # existing research tool tests; keep them
    test_config.py
    test_netguard.py
    test_metadata.py
    test_catalog.py
    test_profiles.py
    test_routing.py
    test_storage.py
    test_scheduler.py
    test_api.py
    integration/            # isolated signed test repository and two mirror fixtures
  profiles/noble-core.yaml
  scripts/accept_profile.sh
  scripts/validate_delivery.py
  deploy/nginx.conf
  Dockerfile
  compose.yaml
  compose.test.yaml
  requirements.in
  requirements.lock
  requirements-dev.lock
  .env.example
  .gitignore
  Makefile
  RUNBOOK.md
  DELIVERY_REPORT.md
```

Production data goes to a configured data directory outside Git. Tests may generate a temporary signing key at runtime for a clearly labeled test repository; never commit a production private key. No `.github/workflows` change is authorized by this mission.

## Task 1 — Validated source registry and database

**Files:** `app/models.py`, `config.py`, `db.py`, `migrations/001.sql`, `tests/test_config.py`, `tests/test_catalog.py`, `requirements*`, local `.gitignore`.

**Interfaces:** Produce `load_sources(Path)->list[SourceConfig]` and the SQL schema specified in API_CONTRACT. All typed names used by later tasks are declared in models.py. Define per-suite snapshot ID as `suite + ':' + inrelease_sha256`; the separate bundle ID remains the canonical suite/hash-map digest in ARCHITECTURE.

- [ ] Write tests: duplicate IDs rejected; defaults merged; null evidence remains null; every shipped source is disabled; a portal cannot be treated as an APT base; missing keyring/config fails readiness, not liveness.
- [ ] Run `python -m pytest tests/test_config.py tests/test_catalog.py -q`; observe the expected missing-feature failures.
- [ ] Implement validation/migration transactions with SQLite FK/WAL and schema version 1. Reject unknown enum values and invalid base URL/allowed-host combinations.
- [ ] Run those tests and the existing `python -m unittest discover -s tests -p 'test_probe_sources.py' -v`; both must pass before proceeding.
- [ ] Commit only the listed Linux paths after inspecting the diff.

## Task 2 — Safe, bounded provider observations

**Files:** `app/netguard.py`, `probes.py`, `tests/test_netguard.py`, relevant fixture server files.

**Interfaces:** Consume SourceConfig/Artifact; produce `ValidatedTarget`, `HttpObservation`, `ProbeResult` through the exact interfaces in API_CONTRACT. Keep partial sample evidence separate from complete hash evidence.

- [ ] Write tests for private/mapped IPv6/mixed DNS, rebinding, credential URL, unapproved redirect, double-encoded traversal, HTML 200, invalid 206, 404 vs 403/429, oversized body, compressed expansion and deadline.
- [ ] Run `python -m pytest tests/test_netguard.py -q` and verify failures correspond to absent behavior.
- [ ] Implement address-pinned access with correct Host/SNI and certificate verification. A post-check uncontrolled DNS lookup is forbidden. Honor Retry-After; enforce byte, rate and time budgets.
- [ ] Stream full artifact SHA-256 and size only when within the explicit budget; quarantine mismatch. A sample hash must never set `full_hash_verified`.
- [ ] Re-run tests; include a real local TLS fixture rather than mocking all certificate behavior. Fixture-only loopback permission must not be enabled by production config.
- [ ] Commit the isolated task.

## Task 3 — APT metadata chain, by-hash and catalog

**Files:** `app/aptmeta.py`, `catalog.py`, `tests/test_metadata.py`, `tests/test_catalog.py`, `tests/integration/`.

**Interfaces:** Consume guarded fetches and archive keyring; produce VerifiedRelease/MetadataBundle/ImportStats using API_CONTRACT functions. Original metadata stays byte-identical.

- [ ] Write tests for a valid fixture InRelease, changed signature, changed compressed index, wrong Suite/Architecture, future Date, expired Valid-Until, mutable rollback and legitimately old base-suite metadata.
- [ ] Write old/new by-hash and atomic-switch tests: active readers of the old digest still receive old bytes; failed staging leaves active bundle unchanged; path/hash conflicts return a blocking state.
- [ ] Run `python -m pytest tests/test_metadata.py tests/test_catalog.py -q`; verify expected failures.
- [ ] Implement native gpgv verification, bounded decompression and checksum-verified Packages parsing. Apply source-specific archive/security mapping; verify all fetched paths against signed Release entries.
- [ ] Stage files then atomically publish a bundle. Preserve seven-day by-hash retention and referenced profiles; reject new publication if quotas would force unsafe eviction.
- [ ] Re-run tests with an actual generated test-key signature. Mark all fixture evidence as synthetic; do not call it a verified Ubuntu production snapshot.
- [ ] Commit. If this gate fails, keep APT serving disabled; the API preview can still proceed safely.

## Task 4 — Native APT profile and gap analysis

**Files:** `app/profiles.py`, `gaps.py`, `profiles/noble-core.yaml`, `tests/test_profiles.py`, `scripts/accept_profile.sh`.

**Interfaces:** Profile definition -> clean-baseline native APT plan -> manifest with exact version/arch/path/size/hash. `classify_gap` consumes a precise eligible source set and timestamp. `import-profile --manifest PATH` may persist a plan; it sets accepted_at only when the manifest references actual successful acceptance logs, exit codes and matching snapshot/baseline evidence. A boolean supplied in JSON alone is insufficient.

- [ ] Write tests: all eligible sources absent -> missing_in_tested_set; one timeout -> unknown; empty eligible set -> unknown; one fully verified copy -> available; one failure domain without retained backup -> fragile.
- [ ] Define seeds `ca-certificates`, `curl`, `git`, `nginx`, `openssh-client`, `rsync`, `unzip`, `jq`; native APT `--no-install-recommends`. Check component membership instead of assuming it.
- [ ] Run profile/gap tests, implement them, and re-run.
- [ ] On a disposable preloaded Ubuntu 24.04 amd64 baseline, record real image digest and package state. Resolve the profile using only configured sources and import trusted metadata hashes; include Pre-Depends/alternatives and relevant `all` packages.
- [ ] With no authorized Iran host or no verified sources, mark the real profile acceptance `not_run/blocked`. Generate deterministic fixture tests, not fabricated production package names/hashes.
- [ ] Commit the definition/tooling and accurate status, excluding private runtime records.

## Task 5 — Routing, local fallback, API and UI

**Files:** `app/routing.py`, `storage.py`, `main.py`, templates/static, `tests/test_routing.py`, `test_storage.py`, `test_api.py`.

**Interfaces:** `select_location` and StorageBackend exactly as defined in API_CONTRACT. Public endpoints are that document's fixed route table; do not add `/proxy?url=`.

- [ ] Write tests: disabled/unapproved/expired/quarantined sources excluded; exact digest preserved; known conflict 409; unknown ID 404; missing usable source 503; successful remote GET/HEAD 302 with no-store; filename mismatch rejected.
- [ ] Test Local CAS interrupted write, wrong size/hash, symlink escape and quota exhaustion. Test disabled Rubika returns an explicit unsupported-capability error without network calls.
- [ ] Implement safe atomic Local CAS, Nginx internal X-Accel path, bounded search/pagination and local Persian responsive UI. Surface source evidence time and limitations, not an unsupported nationwide speed ranking.
- [ ] Include local OpenAPI JSON. Default Swagger assets must not require a public CDN. Separate `/healthz`, `/readyz` and `apt_profile_accepted`.
- [ ] Test a source that dies after 302: first transfer fails, a new resolve may choose another source; never label the first transfer transparently repaired.
- [ ] Run `python -m pytest tests/test_routing.py tests/test_storage.py tests/test_api.py -q`; commit only after green.

## Task 6 — Worker, administration and backup

**Files:** `app/scheduler.py`, `cli.py`, `tests/test_scheduler.py`, `Makefile`.

**Interfaces:** Implement the CLI names in API_CONTRACT, single worker lock, deduplicated jobs and persistent counters. No public mutation endpoint.

- [ ] Write tests for deduplication, restart without quota reset, stuck-job recovery, three-failure circuit/five-minute cooldown/two-success recovery, offline foreign-route denial and sanitized audit logs.
- [ ] Implement job transactions, explicit source approval with evidence/permission note, mode controls and SQLite backup API.
- [ ] Test backup restoration into an empty data directory including referenced manifests and verified objects; a database-only restore with missing CAS must be reported incomplete.
- [ ] Run `python -m pytest tests/test_scheduler.py -q`, then the complete suite; commit after review.

## Task 7 — Deployment and acceptance delivery

**Files:** Dockerfile, compose files, deploy/nginx.conf, `.env.example`, RUNBOOK, DELIVERY_REPORT, `scripts/validate_delivery.py`.

- [ ] Create Compose services edge/app/worker with persistent volumes, non-root application, resource limits and health checks. Do not bind a public admin service or mount the Docker socket.
- [ ] Lock real dependencies/image versions. Pre-stage all runtime assets; make offline startup refuse pulling unknown images rather than silently reaching outside.
- [ ] Implement Make targets `test`, `integration`, `validate`, `up`, `down`, `offline-test`. Their commands must exist and failures must propagate.
- [ ] Execute `python -m unittest discover -s tests -p 'test_probe_sources.py' -v`, `python -m pytest tests -q`, `docker compose -f compose.yaml config --quiet`, and isolated integration tests. Record actual versions/output/exit codes; report unavailable Docker instead of claiming a pass.
- [ ] Verify tamper, source loss, metadata expiry, cold restart, local CSS/OpenAPI and no foreign egress in the isolated fixture network.
- [ ] When authorized Iranian infrastructure is available, run the real-source procedure and clean-client `apt-get update` / install from SECURITY_AND_OFFLINE. Only this gate accepts the production profile.
- [ ] Validate Markdown links, YAML/JSON, no secrets, no paths outside Linux, and no fake results. Run the full suite again after fixes.
- [ ] Commit and push non-destructively; verify published head and read back key files. Record outstanding P0 blockers and P1/P2 items separately.

## P1 / P2 backlog

P1: independent retention of critical artifacts; separately signed recovery APT repository; Ubuntu22.04/26.04 profiles; selected Git bundles + LFS/assets; Python wheelhouse; S3-compatible storage; Rubika pilot only after its documented gates.

P2: OCI registry/Harbor, npm/Verdaccio, Git forge, broad Debian/RPM/Arch/OpenWrt, dependency ecosystems beyond selected projects, PostgreSQL/multiple edges, operator agreements and measured load testing.

## Definition of delivery

A software preview is accepted when deterministic tests and documented deployment work, with no security shortcuts. An offline Ubuntu profile is accepted only with real clean-client evidence and the exact tested scope. A national public service requires additional operator, network, capacity and operational acceptance; the one-day budget does not claim that milestone.
