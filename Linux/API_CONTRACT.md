# P0 implementation contract

Version 1.0 — 2026-10-17. Normative design for [ARCHITECTURE.md](ARCHITECTURE.md). All values in this document are engineering defaults, not provider limits. Product code will live under `Linux/app/`; this research does not claim it already exists.

## 1. Types and persisted records

Use UTC RFC3339 timestamps, nullable unknown values, canonical lowercase hex SHA-256, integer byte counts and explicit evidence scopes. SQLite schema version starts at 1 with migration scripts under `Linux/app/migrations/`.

```sql
CREATE TABLE sources (
 id TEXT PRIMARY KEY, provider TEXT NOT NULL, ecosystem TEXT NOT NULL,
 base_url TEXT NOT NULL, suite_map_json TEXT NOT NULL DEFAULT '{}',
 allowed_hosts_json TEXT NOT NULL, config_json TEXT NOT NULL,
 routing_enabled INTEGER NOT NULL DEFAULT 0 CHECK(routing_enabled IN (0,1)),
 permission_state TEXT NOT NULL DEFAULT 'unreviewed',
 domestic_state TEXT NOT NULL DEFAULT 'unverified',
 failure_domain TEXT, created_at TEXT NOT NULL, updated_at TEXT NOT NULL
);
CREATE TABLE snapshots (
 id TEXT PRIMARY KEY, suite TEXT NOT NULL, inrelease_sha256 TEXT NOT NULL,
 release_date TEXT NOT NULL, valid_until TEXT, acquired_at TEXT NOT NULL,
 origin_source_id TEXT NOT NULL REFERENCES sources(id),
 local_relpath TEXT NOT NULL, status TEXT NOT NULL,
 UNIQUE(suite,inrelease_sha256)
);
CREATE TABLE artifacts (
 sha256 TEXT PRIMARY KEY CHECK(length(sha256)=64), size_bytes INTEGER NOT NULL CHECK(size_bytes>=0),
 ecosystem TEXT NOT NULL, name TEXT NOT NULL, version TEXT NOT NULL,
 architecture TEXT NOT NULL, filename TEXT NOT NULL, license_state TEXT NOT NULL,
 critical INTEGER NOT NULL DEFAULT 0, created_at TEXT NOT NULL
);
CREATE TABLE artifact_paths (
 snapshot_id TEXT NOT NULL REFERENCES snapshots(id), path TEXT NOT NULL,
 sha256 TEXT NOT NULL REFERENCES artifacts(sha256),
 PRIMARY KEY(snapshot_id,path)
);
CREATE TABLE probes (
 id INTEGER PRIMARY KEY, source_id TEXT NOT NULL REFERENCES sources(id),
 sha256 TEXT REFERENCES artifacts(sha256), path TEXT NOT NULL,
 checked_at TEXT NOT NULL, vantage TEXT NOT NULL, outcome TEXT NOT NULL,
 http_status INTEGER, range_supported INTEGER, tls_verified INTEGER,
 latency_ms REAL, body_bytes INTEGER, full_hash_verified INTEGER NOT NULL DEFAULT 0,
 error_code TEXT, retry_after_seconds INTEGER, evidence_relpath TEXT
);
CREATE TABLE locations (
 source_id TEXT NOT NULL REFERENCES sources(id), sha256 TEXT NOT NULL REFERENCES artifacts(sha256),
 path TEXT NOT NULL, state TEXT NOT NULL, verified_at TEXT, expires_at TEXT,
 evidence_probe_id INTEGER REFERENCES probes(id), PRIMARY KEY(source_id,sha256,path)
);
CREATE TABLE storage_objects (
 sha256 TEXT NOT NULL REFERENCES artifacts(sha256), backend TEXT NOT NULL,
 object_key TEXT NOT NULL, status TEXT NOT NULL, verified_at TEXT,
 PRIMARY KEY(sha256,backend)
);
CREATE TABLE profiles (
 id TEXT PRIMARY KEY, definition_json TEXT NOT NULL, manifest_json TEXT NOT NULL,
 baseline_digest TEXT, accepted_at TEXT, acceptance_evidence_relpath TEXT
);
CREATE TABLE jobs (
 id INTEGER PRIMARY KEY, dedupe_key TEXT NOT NULL UNIQUE, kind TEXT NOT NULL,
 payload_json TEXT NOT NULL, status TEXT NOT NULL, attempts INTEGER NOT NULL DEFAULT 0,
 not_before TEXT NOT NULL, locked_at TEXT, last_error TEXT
);
CREATE TABLE audit_events (
 id INTEGER PRIMARY KEY, created_at TEXT NOT NULL, actor TEXT NOT NULL,
 action TEXT NOT NULL, target TEXT NOT NULL, detail_json TEXT NOT NULL
);
```

Artifact identity has both trusted bytes and semantic metadata. P0 allows one canonical semantic record per SHA; aliases can be represented by artifact_paths. Do not overwrite semantic conflicts silently. Never store Rubika tokens/sessions or long-lived signed URL queries in these tables. Private backend credentials live in a mounted secret file. Public artifacts cannot reference private repositories.

## 2. HTTP interface

Only GET/HEAD for public download routes. Administrative mutation is CLI-only in P0, so no public upload surface is needed.

| Endpoint | Success | Meaning / errors |
|---|---|---|
| `GET /` | 200 HTML | Local, responsive Persian UI; sources, limitations and update time. |
| `GET /healthz` | 200 JSON | Process alive; no external requests. |
| `GET /readyz` | 200 or 503 | DB/config valid and selected mode usable; separate `apt_profile_accepted` flag. |
| `GET /v1/sources?cursor=&limit=50` | 200 JSON | Sanitized source/evidence summary; max limit 100. |
| `GET /v1/artifacts?q=&cursor=&limit=50` | 200 JSON | Registered artifact search, not internet URL search. |
| `GET /v1/artifacts/{sha256}` | 200 JSON | Expected size/hash/version and source evidence; 404 unknown ID. |
| `GET /v1/artifacts/{sha256}/resolve` | 200 JSON | Ranked safe choices and reasons; no arbitrary destination input. |
| `GET,HEAD /download/{sha256}/{filename}` | 302 or local 200/206 | Filename must match catalog; 409 bad/conflicting state; 503 no approved usable copy. |
| `GET /v1/gaps?profile=<id>` | 200 JSON | Missing-in-tested-set, unknown, fragile, available; counts include scope/time. |
| `GET /v1/profiles/{id}` | 200 JSON | Requirements, baseline, manifest and real acceptance state. |
| `GET,HEAD /ubuntu/dists/{suite}/{path}` | 200 local file | Valid retained original metadata/by-hash; unsupported paths 404; expired active channel 503. |
| `GET,HEAD /ubuntu/pool/{path}` | 302 or local file | Resolve exact trusted pool path; conflicting digest 409; unregistered path 404. |
| `GET /openapi.json` | 200 JSON | Machine-readable API, no external JS requirement. |

P0 need not expose FastAPI's default CDN-dependent Swagger page. Either self-host its assets or offer local plain HTML instructions plus OpenAPI JSON. Public error envelope: `{"error":{"code":"NO_APPROVED_COPY","retryable":true,"message":"..."},"request_id":"..."}`. Rate limiting yields 429 with Retry-After. Never report source timeout as artifact 404.

Resolve representation:

```json
{
  "artifact_sha256": "<real catalog digest, never a synthetic production value>",
  "mode": "DOMESTIC_ONLY",
  "decision": "redirect",
  "source_id": "<approved-source-id>",
  "download_path": "/download/<digest>/<catalog-filename>",
  "evidence_checked_at": "<actual UTC>",
  "integrity": "full-hash-verified-at-observation",
  "client_verification_required": true,
  "alternatives": [],
  "limitations": ["No transparent failover after redirect"]
}
```

This is a schema illustration, not a real measurement. Responses and redirect decisions use `Cache-Control: no-store`; immutable local metadata/content use correct digest-based ETag and suitable cache headers. Do not put a stale signed Rubika URL into a persistent public API object.

## 3. Python module interfaces

```python
# config.py
load_sources(path: Path) -> list[SourceConfig]
# netguard.py
validate_target(base_url: str, relative_path: str, allowed_hosts: set[str],
                allow_http_signed_metadata: bool = False) -> ValidatedTarget
fetch_bounded(target: ValidatedTarget, method: str, byte_range: tuple[int, int] | None,
              max_body_bytes: int, timeout_seconds: float) -> HttpObservation
# probes.py
classify_observation(observation: HttpObservation, expected_kind: str) -> ProbeResult
probe_artifact(source: SourceConfig, artifact: Artifact, *, full_verify: bool) -> ProbeResult
# aptmeta.py
verify_inrelease(path: Path, keyring: Path) -> VerifiedRelease
stage_bundle(releases: list[VerifiedRelease], index_paths: list[Path]) -> MetadataBundle
publish_bundle(bundle: MetadataBundle) -> str
# catalog.py
import_verified_packages(bundle: MetadataBundle) -> ImportStats
# routing.py
select_location(artifact: Artifact, candidates: list[Location],
                mode: str, now: datetime) -> RouteDecision
# gaps.py
classify_gap(artifact: Artifact, tested: list[ProbeResult],
             eligible_source_ids: set[str], now: datetime) -> GapDecision
# storage.py
class StorageBackend(Protocol):
    def stat(self, sha256: str) -> ObjectInfo | None: ...
    def put_verified(self, file: Path, expected_sha256: str, expected_size: int) -> ObjectInfo: ...
    def download_target(self, sha256: str) -> LocalTarget | RemoteTarget: ...
# scheduler.py
run_due_jobs(now: datetime, budget: ProbeBudget) -> JobRunSummary
```

Use typed dataclasses/Pydantic models with explicit fields; no magic mutable dict conventions across modules. `HttpObservation` includes status, sanitized headers, sampled bytes, connected IP, TLS verification, observation timestamp, duration and error. `ProbeResult` includes classification and integrity scope. `RouteDecision` includes action/local object/source/reason codes and evidence timestamp, not just a URL. `GapDecision` includes tested and untested source sets.

## 4. Safe HTTP and health algorithm

1. Input is a configured source plus registered relative path. Reject credentials, fragments, unapproved hosts/ports, control characters, backslashes and traversal after percent decoding. Reject double-encoded ambiguous paths in P0. Allow only standard HTTP(S) ports unless a reviewed provider exception is configured.
2. Resolve DNS and reject any non-global address, including loopback, link-local, multicast, private, IPv4-mapped private IPv6 and metadata endpoints. Reject mixed public/private answers. Pin the checked address for the actual connection while preserving original Host/SNI/certificate verification. A preflight DNS check followed by a fresh uncontrolled resolution is insufficient.
3. No proxy environment inheritance; no auto redirects. A redirect is a new target requiring explicit allowlist, DNS and mode checks, at most three approved hops. Never forward auth/cookies between origins. In the standalone research probe, redirects are only reported, not followed.
4. Worker samples with `GET Range: bytes=0-4095`, `Accept-Encoding: identity`, max 4096 returned bytes; closes a server's range-ignored 200 response at the cap. HEAD may be used as an optimization, but HEAD failure alone is not absence. Full verification uses streaming SHA-256, exact expected size and a configured maximum artifact size, never unbounded buffering.
5. Valid 206 requires coherent Content-Range, matching start/end and sampled byte count. 200 may show reachability but does not prove Range support. HTML/error bodies are not accepted as `.deb` objects. A partial body hash is never stored as a verified whole-file digest.
6. Map 404/410 to absent only for known mapped paths, 403/429/5xx/timeouts/TLS/DNS to unknown or backoff. Honor Retry-After. Hash mismatch -> quarantine, not retry another hash under the same identity.
7. Defaults: concurrency 4 global/1 per host; request timeout 10s; sample cap 4096B; global 1000 sample requests per day; host minimum interval 1s; status TTL 300s; artifact availability TTL 3600s. Three consecutive transport failures open a five-minute circuit; two later successes close it. Provider-specific documented quotas can only lower these defaults.
8. Full verification budget: 1GiB/day by default, single full-download worker, per-artifact maximum 512MiB for P0. Larger objects remain unverified until explicitly scheduled with a raised cap. Persist counters across restart; do not reset quota by recreating jobs.

## 5. Deterministic source selection

Filter before ranking: configured/enabled, permission reviewed, allowed domestic policy, matching SHA/size and path, full integrity evidence, nonexpired availability, no circuit/quarantine, metadata compatible, quota remaining. An empty set yields 503, not foreign fallback.

Rank eligible remote locations by this stable tuple: independent retained-copy preference for a critical profile, evidence age, configured administrative priority, measured health failure count, measured latency, source ID. No invented latency or national speed ranking. A pinned local verified copy is used when remote sources are unavailable; an operator can prefer local for recovery profiles. Log reason codes and metrics, not user identifiers or bearer URLs.

## 6. Storage contract

Local CAS layout: `<data>/objects/sha256/<first-two-hex>/<digest>`. Write to same-filesystem temp file, stream hash and size, fsync, atomic rename; reject mismatches and symlink escape. Metadata, DB and objects have separate quotas. Return a private internal Nginx path via X-Accel-Redirect, not an arbitrary filesystem path. Nginx handles valid Range/If-Range for completed immutable objects.

`RubikaBackend` is a disabled implementation returning an explicit capability error until approval. An approved future implementation uses official bot methods, private credentials, per-object file_id mapping, refreshed temporary URL validation and full round-trip digest verification. No personal-account automation, quota rotation or unsupported file reassembly in P0.

## 7. Admin CLI

Commands specified for implementation:

```text
python -m app.cli init-db
python -m app.cli import-sources /config/MIRROR_SOURCES.yaml
python -m app.cli probe --source SOURCE_ID
python -m app.cli approve-source --id SOURCE_ID --evidence PATH --permission-note PATH
python -m app.cli sync-apt --profile noble-core
python -m app.cli import-profile --manifest PATH
python -m app.cli run-jobs --once
python -m app.cli set-mode DOMESTIC_ONLY
python -m app.cli backup --destination PATH
```

Approval requires administrator-controlled local evidence and a recorded permission decision; it must not accept a public request as evidence. Audit every mutation. `sync-apt` may prepare metadata but cannot set profile acceptance true. Only the acceptance import command with actual logs can record acceptance.

## 8. YAML contract

`MIRROR_SOURCES.yaml` schema version 1 has `research_date`, `defaults`, and `sources`. Each source includes id, provider, ecosystem, base_url (nullable if not established), declared_type, coverage, evidence_urls, evidence_status, routing_enabled, permission_state, domestic_state, failure_domain, allowed_hosts, suite_map, and notes. Missing or null measurements stay unknown. Discovery-only sources are not activated automatically. Suffix `.ir` is not domestic proof.

The implementation must validate unique IDs, URL/host consistency, legal status values, nonnegative integer budgets and default-disable semantics. HTTP signed APT inputs are an explicit exception to a general HTTPS policy: signature checks stay mandatory, generic unsigned file traffic never inherits the exception, and the public gateway itself uses HTTPS.
