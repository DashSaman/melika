# Work log — append only

## CP01 — 2026-10-18 — independent validation and handoff

Prior repository head inspected: `41ff401c1b3a3b17406b74b476c6ce80b67ff9da`; tree `26b802602d09eff0884189880fd094d9fc172162`.

The repository acquired an earlier Bitcoin audit while this investigation was running. Its existing `research/bitcoin-puzzle-71/` folder was adopted instead of creating a competing root folder. Its five non-README files are preserved unchanged. Root seminar/Linux files are outside scope. README now points to the added checkpoint; older reports retain their historical limitations.

Executed work:
- Read the target operator description, primary Bitcoin documentation, Kangaroo prerequisites and the forum claimant's post. Captured two explorer address summaries and separately fetched inconsistent tip heights; explicitly declined to call them synchronized live proof. UTXO extraction was incomplete.
- Transcribed 83 public historical pairs; corrected the stale upstream README count by inspecting the data. Dataset identity is hashed in evidence/experiments.json.
- Wrote 27 tests before research.py. First run: 27 expected failures because the module did not yet exist; process returned 1. Implemented reference arithmetic, encodings, guarded scanning, numerical models and exploratory diagnostics. Next run: 27 passed, process returned 0. Full original red trace is retained in the session workspace, not duplicated as a long public log.
- Ran `python run_experiments.py --probe71`: all 83 fixture pairs matched, all 83 public points matched cryptography 46.0.4, three public small puzzles recovered, reference CPU timings measured, three diagnostics evaluated with 10,000 null simulations, and 4,096 #71 candidates tested with no hit. Raw numeric results are preserved in evidence/experiments.json.
- No live scalar, receiving address or credentials were acquired. No GPU/native solver or paid infrastructure used. No transaction built, signed, broadcast, or monitored.

This is a completed bounded evidence checkpoint, not all six mission phases. Preserved earlier results and this checkpoint are not interchangeable. Tests cover this isolated added module; no claim is made about unrelated repository projects. Final read-back verification is associated with the resulting Git commit and the delivery response, avoiding a self-referential commit SHA in this log.

Pending evidence: synchronized chain state and every UTXO; authenticated #71 full public key or exact generator provenance; prospective prediction; native/GPU code and benchmark audit; user-controlled reward procedure only after a real recovery.
