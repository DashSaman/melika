# Bitcoin Puzzle 71 research checkpoint plan

**Goal:** Establish a reproducible, challenge-scoped research memory in a separate Melika folder, perform inexpensive real experiments, and avoid unsupported solve or payment claims.
**Architecture:** Independent Python research module, public solved-key fixtures, offline tests, read-only evidence, and scoped agent handoff. No transaction implementation or daemon.
**Tech stack:** Python standard library; installed cryptography used only as an independent curve implementation.
**Spec:** MISSION.md, reflecting the user's six-phase mission.

## Checkpoint sequence
1. Read repository context; preserve the existing main tree. Add only research/bitcoin-puzzle-71/; adopt the concurrently created audit folder rather than create a duplicate.
2. Record source provenance and distinguish reported balances, synchronized chain verification, website claims and calculations.
3. Write failing tests; implement Base58Check, secp256k1 reference arithmetic, bounded search, probability estimates, and structural chain-summary validation.
4. Validate 83 already-public solved-key/address pairs; independently derive the public keys with cryptography/OpenSSL.
5. Recover small solved puzzles and time the actual reference implementation, with explicit operation definitions.
6. Run a fixed descriptive protocol over puzzles 8–70: mean deviation, empirical-CDF distance, absolute lag-one correlation. Use 10,000 matched discrete-uniform simulations and Bonferroni adjustment for three tests. This is exploratory: the dataset was visible before this protocol, not a blinded prediction experiment.
7. Run at most 4,096 candidates against puzzle 71 only, never publishing a successful interval or candidate. Do not run paid or continuing computation.
8. Save non-secret results, limitations, next actions and source hashes; run all new-subproject tests; publish atomically with the latest main tree and no force update; read back the committed checkpoint.

## Review focus
- Reject invalid Base58 alphabet/checksum/network and invalid scalar/range inputs.
- Distinguish hash160 from a full EC public key and collision from target preimage.
- Prevent precision loss in 70-bit counts; use log1p/expm1 for replacement probabilities.
- Do not infer current chain freshness from identical cached balances.
- Public solved fixtures are not newly recovered secrets; live successes never enter JSON logs or Git.

## Open work beyond this checkpoint
Complete and synchronized UTXO/transaction evidence, full Krackpot source audit, reproducible native CPU/GPU build audits, and evidence-based generator hypotheses remain separate gates. A found-key workflow is user-controlled; no assistant signing or broadcasting.
