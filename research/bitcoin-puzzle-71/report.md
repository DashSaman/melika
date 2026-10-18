# Scientific audit decision — 2026-10-18

## VERIFIED LOCALLY

Bitcoin address `1PWo3JeB9jrGwfHDNpdGK54CRas7fsVzXU` validates as Base58Check P2PKH version 0; HASH160: `f6f5431d25bbf7b12e8add9af5e3475c44a0a5b8`.

Search interval [`0x400000000000000000`, `0x7fffffffffffffffff`] has exactly 2^70 = 1,180,591,620,717,411,303,424 candidates.

Illustration ONLY: at an assumed 250 million UNIQUE keys/second continuously for 365 days, uniform-target a priori success chance is 0.0006678007756152904%. This rate was not benchmarked on ChatGPT Pro.

Synthetic negative control: 3,000 simulated train/holdout splits (60 training, 20 holdout each) selecting the most populated quartile of training yielded 0.25135 test accuracy vs 0.25 expected (z~0.764). This is **not** a test of actual puzzle keys.

## DOCUMENTED / INCONCLUSIVE / REFUTED

Documented externally: [historical research](https://github.com/lutfiEmre/bitcoin-puzzle-71-research) found no verified generator/seed/masking transform, thus no reproducible #71 recovery. Not independently rerun here.

Inconclusive: statistical predictive signal in solved puzzle keys. Actual solved-key training, independent key-to-address verification and prospective blind tests have **not been run**. No verified entropy reduction.

Refuted under given inputs: normal Pollard kangaroo / BSGS based only on HASH160 instead of a known EC public point.

## Final decision

**CLOSED_PENDING_NEW_PRIMARY_EVIDENCE.** No private key recovered; no validated shortcut discovered. No brute-force search was performed. Reopen only for authentic creator material, attributable historic wallet outputs, exact generator-and-mask provenance, or confirmed new on-chain public-key exposure. AI-only solution currently infeasible. Repo maintenance does not imply background research.
