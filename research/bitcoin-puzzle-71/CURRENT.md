# Current evidence and decision — CP01 / 2026-10-18

## Result, not a promise

No #71 solution was recovered. No payout or transaction was attempted. Continue only evidence-driven research; no basis for buying computation has been established. This checkpoint adds real-key validation and bounded experiments to the preserved earlier synthetic-only audit.

## Target and chain observations

Base58Check mainnet P2PKH target: `1PWo3JeB9jrGwfHDNpdGK54CRas7fsVzXU`.
Locally decoded HASH160: `f6f5431d25bbf7b12e8add9af5e3475c44a0a5b8`.
Range: `0x400000000000000000 <= k < 0x800000000000000000`.
Width W = 2^70 = 1,180,591,620,717,411,303,424 scalars.

Both captured explorer address responses reported 70 funded and zero spent outputs, 710,192,391 confirmed satoshis (7.10192391 BTC) and no mempool activity [S1,S2]. Separate tip responses were 971828 and 971685. Their 143-block difference prevents a synchronized freshness claim. The cause, response cache age and common block anchor are unknown. The UTXO response was truncated: only two complete example records were retained, not a reconciled 70-output inventory. An unspent address does not prove that nobody knows its scalar. Status: **reported unspent; freshness unresolved**.

## Cryptographic prerequisites and strategy

A P2PKH address stores a hash, not the full EC point Q=kG. Ordinary interval Kangaroo and BSGS require Q; no matching #71 point was independently obtained [S4,S5]. If Q is later authenticated, verify HASH160 of its exact serialization against the target first. Kangaroo has order sqrt(W) expected group work, with implementation constants and resource constraints; sqrt(W)=2^35. This conditional estimate is not an available #71 solution or a seconds-to-recovery guarantee.

| Approach | Necessary input / cost model | Current decision |
|---|---|---|
| Incremental candidate checking | Target HASH160; order W work | Correct reference implemented; only capped research probes justified |
| Optimized native CPU / GPU | Same pipeline plus audited hardware-specific kernel | Not compiled or benchmarked; no CUDA/WebGPU device established |
| Kangaroo | Authenticated full Q and interval; order sqrt(W) group work | Missing prerequisite for #71 |
| BSGS | Full Q; order sqrt(W) work and storage | Also missing Q; tens of billions of entries at this width are not a small table |
| Generator reconstruction | Exact attributable generator, masking rule and validating outputs | No validated artifact or entropy reduction |
| AI/statistical position guess | Genuine prospective predictive evidence | No advantage established by this checkpoint |

SHA-256/RIPEMD-160 target preimage recovery is not the same as a generic collision problem. Deposit transaction signatures belong to funding inputs, not necessarily the puzzle key; they do not establish a same-key nonce attack. A theoretical quantum speedup is not an implemented algorithm on available hardware. Neither unrelated keys nor a curve point substituted for the address hash removes these prerequisites. These are input/algorithm distinctions, not a proof that new cryptanalysis is impossible.

## Historical data and actual execution

The attributed dataset contains public solved pairs #1–70 and #75–135 in steps of five, 83 in total [S3]. Its upstream README said 82 while its data included #135: file contents were used, not the stale count. This does not independently date every solve or verify every historical payout. All 83 pairs passed the new reference implementation; all 83 compressed points also matched cryptography 46.0.4's independent curve backend. Address encoding was additionally checked against known answers. Independent curve checking is not a second implementation of every hashing layer.

27 unit tests passed. Bounded recovery found known fixture #8 after 97 checks, #12 after 636 and #16 after 18,743. These were genuine searches for already-public answers, not new discoveries. Three 4,096-key reference CPU benchmark runs gave a median about 54,111 candidates/s on this container. This affine Python result is not a native CPU or GPU speed claim.

A live-target probe checked exactly the half-open interval `[0x400000000000000000, 0x400000000000001000)`: 4,096 distinct candidates, no hit. Coverage is 3.469446951953614e-18 of W. Do not count the historical-fixture benchmarks or future repeats of this prefix as new #71 coverage. Failed coverage is not a reason to extrapolate that the puzzle is unsolvable.

For puzzles #8–70, normalized residual positions (k-2^(n-1))/2^(n-1) were tested against matched discrete-uniform samples. 10,000 Monte Carlo replicates, seed 71; plus-one p-values and Bonferroni correction for three tests:

| Diagnostic | Statistic | Raw p | Adjusted p |
|---|---:|---:|---:|
| Absolute mean deviation from 0.5 | 0.0279591 | 0.441956 | 1.0 |
| Uniform ECDF distance | 0.1015752 | 0.509249 | 1.0 |
| Absolute lag-one correlation | 0.0859149 | 0.505649 | 1.0 |

These limited checks find no significant departure, not proof of uniformity, independence, security or impossibility of a generator flaw. The protocol was fixed after the data was visible, before numerical analysis: **exploratory, not blinded preregistration or held-out prediction**. Other previously tried hypotheses would add a larger selection burden. The 2017 forum poster claiming to be the creator described masked deterministic-wallet outputs without a pattern [S6]; authorship was not independently cryptographically authenticated here, and exact wallet software/seed/PRNG remains unverified.

## Cost and probability model

Assume a uniform unknown target in W, constant rate r, correct checking and no competing claimant. For m distinct tested scalars, hit probability is min(m/W,1); without-replacement full sweep takes W/r and expected hit time is (W+1)/(2r). For m IID uniform draws with replacement, p=1-(1-1/W)^m and median time is ln(0.5)/(r*ln(1-1/W)). These models must not be mixed; randomly placed batches require accounting for batch size, boundaries and overlap.

At an **assumed, unmeasured** 10^9 candidates/s, a nonduplicated full sweep is about 37,410 years and mean position about 18,705 years (365.25-day year). One 365-day distinct search covers about 0.00267120% of W. Check `hypothetical_rates_not_benchmarks` in the results for other scenarios. Electricity cost is power_kW * elapsed_hours * tariff; cloud cost also needs an actual authorized quote. No tariff, fiat exchange rate, hardware quote or spend has been assumed as current market fact. Competing claims, outages, bad kernels, duplicated work and fees make personal payoff different from raw target-hit probability.

## Krackpot and conditional reward safety

Krackpot's technical author describes browser WebGPU searching, a fixed 6 BTC winner payment with the remainder to the author, locally built claim transactions, private miner submission, claim-time dependencies and encrypted signed-transaction backup to the author [S7]. These are **operator claims**; deployed JavaScript/WGSL, dependencies, network behavior and payouts were not independently audited here. Reading the write-up is not a security audit. Independent solving and accepting that website's split are different arrangements.

If a correct scalar is ever found: stop public logs; verify locally with independent implementations; recheck every selected UTXO against a fresh, trusted node; have the user obtain and verify a mainnet receiving address on their own wallet device. Do not collect their seed or personal private key. A qualified user-controlled wallet workflow should review all outputs, dust selection, fees, size and competing-spend risk before the user signs or submits. No signing/broadcast code is included.

A P2PKH spend exposes its **public key**, not its private key verbatim [S5]. For a narrow puzzle interval this can enable competitors to solve a faster DLP. Signed hex and PSBTs may disclose information; never publish them, make a public test-spend, or assume RBF or a large fee guarantees ownership. A private full node does not automatically provide private mining submission. A miner channel introduces trust and leak risks and does not guarantee confirmation. Verify a channel independently before relying on it; the assistant must not execute an autonomous fund transfer.

## Next gates

First obtain fresh block-anchored chain observations and a complete UTXO inventory, including script verification and outpoint reconciliation. Then prioritize authenticated public-key or generator evidence. A proposed generator must reproduce multiple published outputs under a frozen rule and survive prospective held-out testing. Native/GPU work requires source review, pinned versions, edge/boundary tests, a hardware-specific benchmark and explicit resource approval. Do not buy compute or repeat low-value probes merely because a prize exists.
