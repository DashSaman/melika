# Security, outage acceptance and recovery

Design date: 2026-10-17. This document specifies tests to execute; it is not evidence those tests already passed. Research-tool results are in [evidence/RESEARCH_LOG.md](evidence/RESEARCH_LOG.md). Protocol references: [S25–S33](SOURCES.md). Normative implementation details: [API_CONTRACT.md](API_CONTRACT.md).

## 1. Trust boundaries

Untrusted inputs: public path/search parameters, upstream HTTP responses, DNS answers, redirect locations, repository metadata before signature validation, filenames inside downloaded archives, and third-party client install scripts. A source being listed in a community registry does not make its content trusted.

Trusted inputs: reviewed source configuration, an explicitly provisioned archive keyring, verified metadata-to-artifact hash mappings, an administrator-controlled profile definition and a documented permission decision. These still need versioning and audit trails.

Protect the host: process runs without root, read-only image filesystem where practical, no Docker socket in app/worker, separate writable data volumes, secret mounts outside Git, request and disk quotas, and no arbitrary shell commands based on artifact filenames. Pass subprocess arguments as lists and check exit codes. Archive extraction is not required for generic downloads; any future extraction must reject traversal and symlinks escaping the destination.

## 2. Required controls and tests

| Threat | Control | Acceptance condition |
|---|---|---|
| SSRF / metadata endpoint access | Configured host/path allowlist, all-address DNS validation, pinned connection, SNI verification | Private/loopback/link-local/mapped IPv6 and mixed DNS answers rejected before connect. |
| DNS rebinding | Use the validated address for actual socket connection | A second resolution cannot silently change the destination. |
| Open redirect / credential leak | No public URL input, revalidate every allowed hop, strip auth across origin changes | Unlisted redirect blocked; no bearer URL in public log. |
| Path traversal / cache collision | Decode/reject ambiguous paths, content-addressed storage, catalog filename check | Encoded traversal/backslash/symlink and conflicting trusted hashes rejected. |
| Forged repository/package | gpgv and full signed hash chain; quarantine | Corrupted InRelease, index or package never served as verified. |
| Replay / expired data | Date/Valid-Until plus documented mutable-suite policy | Expired active channel fails closed; UI shows original security-data age. |
| Resource exhaustion | Limits on requests, response bytes, decompression, jobs, disk and retries | Infinite/oversized bodies and compressed bombs hit explicit bounds; no unbounded task fan-out. |
| Public administration | CLI-only mutation in P0; later authenticated admin with CSRF protections | Anonymous client cannot enable sources, upload files or change mode. |
| Missing secrets discipline | Secret mounts, sanitized exceptions, no full signed URLs | Secret scanning of staged files and logs finds no credentials. |
| Supply-chain bootstrap | Locked dependencies and image digests; offline wheel/image copies | Service starts without fetching from public registries or CDNs. |

Metadata decompression must have both compressed and expanded size limits. Network timeout applies to connect/read and an outer job deadline; DNS resolution also needs a bounded execution strategy in the production worker. The standalone research probe uses OS DNS resolution and is not the production scheduler.

## 3. Failure-scenario matrix

| Scenario | Detection | Automatic response | Recovery and proof |
|---|---|---|---|
| Normal international access | Multiple expected checks succeed | Online sync only through explicit policy, stage/verify before publish | Import one valid bundle and verify all referenced indices. |
| Complete foreign disconnection | Controlled test policy or corroborated observations | DOMESTIC_ONLY, no foreign sync/redirect/token fallback | Clean-client profile install using approved domestic sources; outbound audit shows no foreign dependency. |
| Foreign DNS unavailable | Resolver failures distinguished from HTTP absence | Use configured domestic resolver/local service names; mark affected source unknown | Resolve public gateway and all approved artifact/CDN hosts without foreign resolver dependency. |
| HTTPS failure on a source | Certificate/handshake error | Quarantine/backoff that route; never disable certificate checks | Valid alternate copy works; corrupted certificate test must fail closed. |
| One domestic mirror down | Circuit breaker / transport evidence | Select already verified alternate or local pinned object | Kill mock source before resolve; decision uses healthy source and preserves digest. |
| Several domestic mirrors down | Multiple circuits open | Serve pinned profile files; explicit 503 otherwise | Never replace unavailable with absent or invent a foreign fallback. |
| Source fails after 302 | Client read error; gateway cannot observe full transfer | Client retries resolve; optional local fallback | Test documents broken first transfer, then complete second download with expected hash. |
| Rubika API unreachable | Backend-specific error | Disable optional backend, preserve other routes | Gateway remains usable without Rubika; no production claim if it was sole copy. |
| Rubika download URL expired | Validated 401/403/expiry behavior | Refresh through official API if allowed, then revalidate target | Real-account test required; fixture test alone is insufficient. |
| Metadata exists but package does not | Known path 404/410 | Missing-in-tested-set only after relevant source-set is checked | Do not mark profile accepted until actual install completes. |
| Old or damaged content | Date policy or full digest mismatch | Stop publication/quarantine object; do not silently resign original metadata | Correct old snapshot retention or distinct opt-in recovery repo. |
| Missing dependency/build asset | Native client install/build fails | Record exact dependency and source; incomplete profile stays incomplete | Re-run on clean baseline after closure is fixed. |
| Disk full / quota exhausted | Threshold and atomic-write failure | Reject new writes, protect pinned/live metadata; no partial publication | Restore disk budget and resume safely; existing local files still hash correctly. |
| Incorrect system clock / impending cert expiry | Local time sanity and certificate lifetime check | Visible degraded state; avoid false freshness claims | Time/cert issue fixed through controlled operations, never backdate client to bypass validity. |
| Cold restart during outage | Restart after caches needed by runtime are deliberately removed from test container | Use already staged app images, runtime dependencies and local assets | Compose starts with pull disabled and API/UI operate without internet. |

Emulated tests prove behavior under the tested constraints. They cannot guarantee reachability during every future national partition, ISP-specific restriction or power failure.

## 4. Safe in-Iran probe procedure

Run only from an authorized server. This script does not change firewall, routes, APT sources or accounts. Its targets are configuration controlled by the operator, not a public API.

```bash
cd /path/to/melika/Linux
python3 -m unittest discover -s tests -v
python3 scripts/probe_sources.py \
  --targets scripts/PROBE_TARGETS.json \
  --vantage iran-authorized-vm-operator-label \
  --output /tmp/melika-mirror-probes.json
```

The label is an operator assertion, not automatic geolocation proof. A 4KiB response is not a complete InRelease signature test or full artifact hash verification. Review the output privately before publishing it; detailed network records can expose infrastructure identifiers.

For real source approval, collect a full InRelease within a bounded size, verify using the pre-provisioned archive keyring, and select a small `.deb` via the verified Packages index. Download that exact file fully, compare size/SHA-256, then test Range and resume separately. Repeat from a second authorized Iranian network for priority sources. Keep expected/actual values and UTC timestamps; do not turn null fields into zero.

## 5. Isolated offline test laboratory

Never cut the host's management connection or change production firewall rules to demonstrate an outage. Use a disposable VM/network namespace or dedicated lab host with console/rollback. Preload client and service images before network isolation.

Deterministic lab: mock mirror A, mock mirror B, gateway, and test client on an isolated Docker network configured `internal: true`. An intentionally small fixture repository is signed by a generated **test-only** key and clearly labeled as a fixture; it must never use Canonical's name or production key identity. This tests routing, tampering, expiry, atomic metadata changes and failure handling, not real Iranian connectivity.

Real domestic-only lab: restrict a disposable client's egress to the verified domestic endpoints and domestic DNS it actually needs; enforce IPv4 and IPv6 consistently, inspect DNS/HTTP redirect/token dependencies, and retain an administrative recovery path outside the lab. Provider CDN IP churn must be reconciled with the approved host policy; do not broadly allow all addresses from a guessed country prefix.

Record: baseline digest, installed package list, APT source files, key fingerprints, snapshot IDs, resolved package manifest, egress policy, mode, time, stdout/stderr and exit codes. Start with empty client APT lists/archive cache except what is explicitly part of the documented baseline. Run `apt-get update`, install the exact profile, then test installed programs. No signature/date/TLS bypass flags.

For `noble-core`, disable translation downloads and specify architecture amd64/component main. Do not add unknown third-party repositories. If a seed is not in the declared component, report the blocking fact and an explicit profile revision; do not secretly expand the mirror scope.

## 6. Long-outage and bootstrap pack

Prepare an offline bootstrap pack before any disconnection: app source at a commit, pinned built images, dependency wheels where applicable, Compose configuration, local UI assets, public archive keyring, source registry, signed metadata, accepted profile manifest, critical objects, restore instructions and checksums. Do not put production secrets or private signing keys in the public pack.

Original upstream metadata is not valid forever. A separately signed recovery repository is a P1 feature, explicitly opt-in and visibly frozen at its source snapshot date. It cannot claim fresh security updates that were never received. A key expiration/revocation and distribution plan is required before that channel is trusted by users.

SQLite backup uses the backup API or a controlled consistent snapshot including WAL state. Test restoration into an empty directory. Preserve referenced CAS objects and manifests; a database backup pointing to deleted files is not a recovery solution. Keep at least one critical backup outside the same provider/failure domain.

## 7. Usage terms and licensing checklist

Before public redirection at meaningful scale, record operator terms, permission decision, quotas and a contact/escalation path. Respect Retry-After; no account/IP rotation to evade limits. Attribute original providers rather than presenting their bandwidth as our owned infrastructure.

Each stored project/artifact has a license review state. Public availability is not blanket permission to redistribute modified binaries, firmware, model weights or Android components. Preserve required notices and corresponding-source obligations where applicable; store original provenance and an export procedure. Do not scrape or republish private repositories. This is an operational checklist, not a jurisdiction-specific legal opinion.

## 8. Required acceptance report

Report three independent sections: **software test results**, **real source probes**, and **in-Iran offline installation**. Include not_run/blocked states and the exact reason. A mocked 200, a browser-rendered page, a checksum of the first 4096 bytes, or a successful frontend screenshot must never be used to claim the final offline-install gate passed.
