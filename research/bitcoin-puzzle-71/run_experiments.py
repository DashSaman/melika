"""Offline public-fixture experiments; an optional, capped #71 probe.

Run from this directory. Output contains only public data and failed-search
ranges. If a live scalar is recovered, reporting aborts and the scalar is saved
outside the repository with owner-only permissions. No transaction code exists.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import os
import platform
import statistics
import sys
import tempfile
import time
from pathlib import Path
import research as r


def run(live_probe: bool = False, replicates: int = 10000) -> dict:
    rows = r.fixtures()
    started = time.perf_counter()
    for n, k, a in rows:
        if not (1 << (n-1)) <= k < (1 << n) or r.address(k) != a:
            raise RuntimeError(f'public fixture validation failed: puzzle {n}')
    validated_seconds = time.perf_counter() - started
    independent = {'available': False, 'public_keys_matched': 0}
    try:
        import cryptography
        from cryptography.hazmat.primitives.asymmetric import ec
        from cryptography.hazmat.primitives.serialization import Encoding, PublicFormat
    except ImportError:
        independent['reason'] = 'optional cryptography package unavailable; no installation attempted'
    else:
        for n, k, _ in rows:
            point = ec.derive_private_key(k, ec.SECP256K1()).public_key()
            encoded = point.public_bytes(Encoding.X962, PublicFormat.CompressedPoint)
            if encoded != r.compress(r.mul(k)):
                raise RuntimeError(f'independent curve mismatch: public puzzle {n}')
        independent = {'available': True, 'version': cryptography.__version__,
                       'public_keys_matched': len(rows),
                       'scope': 'independent curve backend; address hashing checked against published fixtures'}
    recovered = []
    by_number = {n: (k, a) for n, k, a in rows}
    for n in [8, 12, 16]:
        expected, target = by_number[n]
        t = time.perf_counter()
        found, count = r.scan(target, 1 << (n-1), 1 << n)
        elapsed = time.perf_counter() - t
        if found != expected:
            raise RuntimeError(f'bounded fixture recovery failed: puzzle {n}')
        recovered.append({'puzzle': n, 'success': True, 'candidates_checked': count,
                          'seconds': elapsed, 'public_historical_fixture': True})
    benchmark_rates = []
    for _ in range(3):
        t = time.perf_counter()
        found, count = r.scan(by_number[16][1], 1, 4097)
        elapsed = time.perf_counter()-t
        if found is not None or count != 4096:
            raise RuntimeError('unexpected benchmark result')
        benchmark_rates.append(count / elapsed)
    probe = {'executed': False, 'counted_as_coverage': 0}
    if live_probe:
        t = time.perf_counter()
        found, count = r.scan(r.TARGET, r.LOW, r.LOW+4096)
        elapsed = time.perf_counter()-t
        if found is not None:
            directory = Path(tempfile.mkdtemp(prefix='puzzle71-private-'))
            os.chmod(directory, 0o700)
            secret = directory / 'candidate.txt'
            fd = os.open(secret, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
            with os.fdopen(fd, 'w') as f:
                f.write(format(found, '064x') + '\n')
            raise RuntimeError('LIVE MATCH: publication stopped. Review owner-only puzzle71-private-* temporary directory locally. No transaction performed.')
        probe = {'executed': True, 'found': False, 'candidates_checked': count,
                 'counted_as_coverage': count, 'start_hex': format(r.LOW, 'x'),
                 'stop_exclusive_hex': format(r.LOW+4096, 'x'), 'seconds': elapsed,
                 'fraction_of_full_interval': count/(r.HIGH-r.LOW)}
    return {
        'schema': 1, 'run_label': 'CP01',
        'python': platform.python_version(), 'platform': platform.platform(),
        'gpu_device_nodes_detected': [str(p) for p in Path('/dev').glob('nvidia*')],
        'gpu_benchmark_executed': False, 'native_optimized_benchmark_executed': False,
        'dataset_sha256': hashlib.sha256((Path(__file__).parent/'data/solved_puzzles.csv').read_bytes()).hexdigest(),
        'fixture_validation': {'matched': len(rows), 'seconds': validated_seconds},
        'independent_backend': independent, 'small_recoveries': recovered,
        'reference_python_benchmark': {'candidates_per_run': 4096,
            'keys_per_second_runs': benchmark_rates,
            'median_keys_per_second': statistics.median(benchmark_rates),
            'scope': 'affine incremental CPU Python; not a CUDA or native-performance estimate'},
        'pattern_diagnostics': r.pattern_diagnostics(rows, replicates, 71),
        'hypothetical_rates_not_benchmarks': {str(rate): r.estimates(rate) for rate in [1000000,100000000,1000000000]},
        'target_hash160': r.decode_address(r.TARGET).hex(), 'probe71': probe,
        'puzzle71_solved': False, 'transaction_constructed': False,
        'transaction_signed': False, 'transaction_broadcast': False,
        'paid_resources_used': False,
    }


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--probe71', action='store_true', help='opt in to one 4096-candidate #71 probe')
    args = parser.parse_args()
    print(json.dumps(run(args.probe71), indent=2, ensure_ascii=False))
