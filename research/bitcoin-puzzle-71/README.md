# Bitcoin Puzzle #71 — persistent research handoff

**CP01 · 2026-10-18 · No #71 key recovered; no transaction constructed, signed or broadcast.**

این پوشه حافظهٔ مرجع این تحقیق در ریپوی عمومی ملیکا است. از صفر شروع نکنید: ابتدا [راهنمای ایجنت](AGENTS.md)، [وضعیت ماشینی](STATUS.json)، [گزارش فعلی](CURRENT.md) و [دفتر کار](WORK_LOG.md) را بخوانید. منابع و محدودیت‌های دسترسی در [SOURCES.md](SOURCES.md) ثبت شده‌اند.

**مسیر واحد:** `research/bitcoin-puzzle-71/`؛ پوشهٔ موازی در ریشه نسازید. پروژه‌های روان‌شناسی و Linux را تغییر ندهید.

## What was actually executed

83 published historical scalar/address pairs validated; 83 compressed public keys cross-checked with the independent `cryptography` curve backend; 27 unit tests passed. Bounded searches recovered public fixtures #8, #12 and #16. A single 4,096-candidate #71 probe found nothing. Three exploratory diagnostics on real solved keys, with 10,000 matched-null simulations, found no significant result after correction. These are not blind predictions or proof that no weakness exists.

Two explorer address responses agreed on 710,192,391 satoshis and zero spent outputs. Their separately fetched tips differed by 143 blocks: current synchronized balance and complete UTXO reconciliation remain unverified. See [captured evidence](evidence/chain_observations.json).

## Reproduce offline

From this directory, use Python 3.10+ with RIPEMD-160 support:

```sh
python -m unittest discover -s tests -v
python run_experiments.py > /tmp/puzzle71-new-experiments.json
```

The standard library runs the reference checks. An already-installed `cryptography` package enables the independent curve check; absence is reported, not silently treated as a pass. No automatic installation, network calls, cloud spending, mining or wallet transactions occur. Default execution does **not** search #71. `--probe71` deliberately repeats the small recorded prefix and should not be used merely to claim new coverage. Output timings vary by host.

## Files and safety

[Mission](MISSION.md) · [Plan](PLAN.md) · [Results](evidence/experiments.json) · [Tests](tests/test_research.py) · [Public fixtures](data/solved_puzzles.csv) · [Reference code](research.py).

Published historical scalars are test data, not personal wallet secrets. Never fund their addresses. Newly discovered live scalars, seeds, receiving-wallet details and signed transactions must stay outside Git, issues, chats and telemetry. No receiving address has been supplied. Any eventual signing and submission belong to the user-controlled wallet workflow described in CURRENT.md.

## Earlier checkpoint retained unchanged

The files `experiment.py`, `results.json`, `report.md`, `research_matrix.md` and `hypotheses.md` belong to the earlier AI-only audit at commit `41ff401c1b3a3b17406b74b476c6ce80b67ff9da`. Its synthetic control remains historical evidence, not a real-key prediction test. Statements there that real-fixture ingestion or a bounded search had not run describe that earlier checkpoint; consult CURRENT.md and STATUS.json for this added work. We do not claim to have rerun or independently audited every external project cited in the older matrix.
