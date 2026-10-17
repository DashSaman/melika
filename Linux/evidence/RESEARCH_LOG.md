# Research and verification log

Research date: 2026-10-17. This is a research/design delivery, not an operational mirror rollout.

## Repository scope

Repository: `DashSaman/melika`, public. GitHub connector reported write permission. Baseline main commit observed: `bfae8680b863d0e339eac790aefdf2d4ef3087b3`; its actual root tree was `73b68c17a14b6bedd0b7fc4df0c676f38b923e3a`. Root contents and AGENTS were inspected. No Linux directory existed in that root tree. All additions in this mission are scoped to Linux; the unrelated root seminar project is not part of this research.

To avoid self-referential commit hashes, the delivery commit is read from Git history rather than embedded into its own body. Final branch/ref readback and changed-path comparison are required before reporting publication success.

## Sources and confidence

The source ledger contains 49 primary/discovery URLs with explicit boundaries, plus direct project/manual links in RELATED_PROJECTS. Provider pages, source repositories and protocol documentation were read through a web-research interface. This can substantiate published claims, not raw TLS/HTTP behavior from an Iranian host.

The YAML registry contains 27 service/candidate entries. They are not 27 independent operators. All routing flags are disabled until evidence and permission gates are completed. DOCUMENTED rows and discovery-only UNVERIFIED rows remain distinct. Exact package-level national coverage or absence was not measured.

Three upstream projects had default-branch commit metadata retrieved through GitHub: MirrorCache 29b7aa7 (committer 2026-09-28), aptly 516fcc6 (2026-10-12), tunasync 702c68c (2026-05-15). RELATED_PROJECTS preserves complete identifiers and links. Other last-activity gaps remain explicit.

## Local research tool tests actually executed

Tool: `scripts/probe_sources.py`, standard-library Python. Tests: `tests/test_probe_sources.py`. Interpreter in the research runtime: Python 3.13 (production design targets Python 3.12; that exact runtime has not been certified here).

An initial red test run failed because the implementation was missing; dependent tests were skipped. After implementation:

```text
python -m unittest discover -s tests -v
Ran 18 tests
OK

python -m py_compile scripts/probe_sources.py
exit status 0
```

These tests cover URL validation, private/mixed DNS rejection, status/Range classification and the distinction between a PGP-looking prefix and real signature verification. DNS is mocked for relevant unit cases. They do not prove real external TLS, end-to-end APT trust, current mirror availability or production security. The saved test transcript is `probe-tests.txt`.

## Actual external probe attempt

The probe was run with `scripts/PROBE_TARGETS.json`, five small candidate noble/InRelease requests, and vantage label `research-sandbox-not-an-iran-probe`. Output: `sandbox-probes.json`.

Observed UTC window: **2026-10-17T01:01:04Z to 2026-10-17T01:01:13Z**. All five targets failed DNS resolution with `gaierror`. They remain `unknown`. HTTP status, TLS and Range are null; complete artifact hash and signature verification are false; country/outage verification are false. This is an environment limitation, not evidence that those providers are globally down or absent inside Iran.

No automatic redirect was followed by the research probe. Body download is capped at 4096 bytes. A sample SHA, if a future run records one, must not be mistaken for a full-file hash. An operator-provided vantage label is not automatic proof of location.

## Tests and actions NOT executed

- No authorized in-Iran VM/second ISP test in this mission.
- No production full `.deb` download/hash or native APT profile install.
- No verified live InRelease signature/import or full mirror freshness scan.
- No Docker deployment, load benchmark or national failover test.
- No Rubika account/token/OTP, upload, anonymous download, Range or 24/72-hour retention test.
- No operator permission agreement, commercial purchase or quota approval.
- No independent storage recovery experiment for live data.

## Remaining evidence gates

Run the delivered probe from an authorized domestic host, then full signature/hash and clean-client tests in SECURITY_AND_OFFLINE. Confirm source paths and permissions, resolve unknown quotas, and measure actual profile bytes. The Arvan storage-overage table/FAQ discrepancy is unresolved; the cost model marks it instead of selecting a convenient value.

## Delivery interpretation

The research package provides architecture, implementation contracts, code-level task plan, source registry and a tested supporting probe. The actual gateway application and production profile are the next implementation phase. No completed research file or passing probe-unit test is represented as an already operating public mirror.
