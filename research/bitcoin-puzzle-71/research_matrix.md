# Evidence audit / avoiding duplicate work — 2026-10-18

| Prior work | What is already done | Limitations | Independent local reproduction |
|---|---|---|---|
| [Historical dossier](https://github.com/lutfiEmre/bitcoin-puzzle-71-research) | Old wallet generator census, Casascius test vectors, TX fingerprint, funding analysis | No established generator/mask/seed or #71 recovery | Not repeated |
| [Old generator census](https://github.com/lutfiEmre/bitcoin-puzzle-71-research/blob/main/GENERATOR_CENSUS_PRE2015.md) | Pre-2015 Electrum/Armory/Casascius candidate families | Possible generator is not proven origin | Not repeated |
| [Solved-key statistics](https://github.com/ingabolee/keys) | 82 solved-key positions | Post-hoc multiple comparisons and dataset provenance issues | Not independently reverified |
| [Solved-key ledger](https://github.com/roadhero/Bitcoin-Puzzle-Info) | Historical solved puzzle listings | Live chain status not verified here | Not repeated |
| [Practical GPU and kangaroo lab](https://github.com/fxlipe124/btc-puzzles-solver) | GPU search and useful address-verification bug report | Hardware speed != keyspace shortcut | Not repeated |
| [Incremental point CPU scanner](https://github.com/juanykty/BTC-PUZZLE-71) | Optimization using P-=G | No genuine reduction of range | Not repeated |
| [Systematic Keyhunt experiments](https://github.com/mlartab/bitcoin-puzzle-systematic-analysis) | Historical PRNG candidates and search methods | No blind evidence for predictive gain | Not repeated |
| [Collider](https://github.com/ONGISTRON/0xcollider) | Distinguishes revealed-pubkey kangaroo from hidden-pubkey brute-force | No point for #71 established | Not repeated |
| Local experiment.py | Exact bounds, Base58Check address validation, synthetic holdout negative control | No real-key predictions | YES |

Do not sum claimed pool scanning percentages without independently authenticating and deduplicating intervals. Third-party research findings above are documented claims, not independently audited proofs.
