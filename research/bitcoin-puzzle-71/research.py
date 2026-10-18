"""Bounded public-puzzle research. No network, signing, broadcasting or secret storage.

Reference affine arithmetic is not constant-time and is NOT a production wallet.
All scalars in data/solved_puzzles.csv are already-public historical fixtures.
"""
from __future__ import annotations
import csv
import hashlib
import math
import random
from pathlib import Path

P = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F
ORDER = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141
G = (0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798,
     0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8)
LOW, HIGH = 1 << 70, 1 << 71
TARGET = '1PWo3JeB9jrGwfHDNpdGK54CRas7fsVzXU'
ALPHABET = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'
Point = tuple[int, int] | None


def integer(x: object, minimum: int = 0) -> int:
    if type(x) is not int or x < minimum:
        raise ValueError('expected an integer within the allowed range')
    return x


def add(a: Point, b: Point) -> Point:
    """Add internally generated, trusted curve points (None is infinity)."""
    if a is None:
        return b
    if b is None:
        return a
    x, y = a
    u, v = b
    if x == u:
        if (y + v) % P == 0:
            return None
        slope = (3 * x * x) * pow(2 * y, -1, P) % P
    else:
        slope = (v - y) * pow((u - x) % P, -1, P) % P
    z = (slope * slope - x - u) % P
    return z, (slope * (x - z) - y) % P


def mul(k: int) -> Point:
    k = integer(k) % ORDER
    out, base = None, G
    while k:
        if k & 1:
            out = add(out, base)
        base = add(base, base)
        k >>= 1
    return out


def compress(point: Point) -> bytes:
    if point is None:
        raise ValueError('infinity has no compressed public-key encoding')
    x, y = point
    return bytes([2 + (y & 1)]) + x.to_bytes(32, 'big')


def hash160(data: bytes) -> bytes:
    return hashlib.new('ripemd160', hashlib.sha256(data).digest()).digest()


def b58check(payload: bytes) -> str:
    checksum = hashlib.sha256(hashlib.sha256(payload).digest()).digest()[:4]
    raw = payload + checksum
    n, out = int.from_bytes(raw, 'big'), ''
    while n:
        n, rem = divmod(n, 58)
        out = ALPHABET[rem] + out
    return '1' * (len(raw) - len(raw.lstrip(b'\0'))) + out


def encode_address(digest: bytes) -> str:
    if not isinstance(digest, bytes) or len(digest) != 20:
        raise ValueError('HASH160 must contain 20 bytes')
    return b58check(b'\0' + digest)


def decode_address(text: str) -> bytes:
    if not isinstance(text, str) or not 26 <= len(text) <= 35:
        raise ValueError('expected a mainnet P2PKH address')
    n = 0
    try:
        for ch in text:
            n = n * 58 + ALPHABET.index(ch)
    except ValueError:
        raise ValueError('invalid Base58 alphabet') from None
    raw = b'\0' * (len(text) - len(text.lstrip('1'))) + n.to_bytes((n.bit_length()+7)//8, 'big')
    if len(raw) != 25 or raw[0] != 0 or b58check(raw[:-4]) != text:
        raise ValueError('invalid checksum, network or payload length')
    return raw[1:-4]


def address(k: int) -> str:
    if integer(k, 1) >= ORDER:
        raise ValueError('scalar outside secp256k1 range')
    return encode_address(hash160(compress(mul(k))))


def fixtures() -> list[tuple[int, int, str]]:
    path = Path(__file__).resolve().parent / 'data' / 'solved_puzzles.csv'
    with path.open(encoding='utf-8', newline='') as f:
        return [(int(x['puzzle']), int(x['public_solved_scalar_hex'], 16), x['address'])
                for x in csv.DictReader(f)]


def scan(target: str, start: int, stop: int) -> tuple[int | None, int]:
    """Scan one bounded half-open interval, at most 65,536 candidates.

    Returns a scalar in memory on a hit. Callers must never log or publish a
    newly recovered live scalar. This function does not save results.
    """
    integer(start, 1)
    integer(stop, 1)
    if not start < stop <= ORDER or stop - start > 65536:
        raise ValueError('invalid interval or exceeded 65,536-candidate safety cap')
    digest, point = decode_address(target), mul(start)
    for checked, k in enumerate(range(start, stop), 1):
        if hash160(compress(point)) == digest:
            return k, checked
        point = add(point, G)
    return None, stop-start


def hit_probability(draws: int, width: int) -> float:
    """IID uniform draws WITH replacement; not a guaranteed personal payoff."""
    integer(draws)
    integer(width, 2)
    return -math.expm1(draws * math.log1p(-1 / width))


def estimates(rate: float, width: int = HIGH-LOW) -> dict:
    integer(width, 2)
    if isinstance(rate, bool) or not isinstance(rate, (int, float)) or not math.isfinite(rate) or rate <= 0:
        raise ValueError('rate must be positive and finite')
    return {'sweep_seconds': width / rate,
            'without_replacement_mean_seconds': (width+1) / (2*rate),
            'replacement_median_seconds': math.log(.5) / (math.log1p(-1/width) * rate)}


def chain_summary(obj: dict) -> dict:
    """Validate returned confirmed statistics; this does not prove freshness."""
    try:
        if obj['address'] != TARGET:
            raise ValueError('wrong target address')
        s = obj['chain_stats']
        for field in ['funded_txo_count', 'funded_txo_sum', 'spent_txo_count', 'spent_txo_sum', 'tx_count']:
            integer(s[field])
        if s['spent_txo_count'] > s['funded_txo_count'] or s['spent_txo_sum'] > s['funded_txo_sum']:
            raise ValueError('inconsistent confirmed statistics')
        return {'balance_sats': s['funded_txo_sum']-s['spent_txo_sum'],
                'utxo_count': s['funded_txo_count']-s['spent_txo_count'],
                'spent_txo_count': s['spent_txo_count'], 'tx_count': s['tx_count']}
    except (KeyError, TypeError):
        raise ValueError('missing or invalid address statistics') from None


def _statistics(x: list[float]) -> tuple[float, float, float]:
    n = len(x)
    mean_distance = abs(sum(x)/n - .5)
    ordered = sorted(x)
    ecdf = max(max((i+1)/n-v, v-i/n) for i, v in enumerate(ordered))
    a, b = x[:-1], x[1:]
    ma, mb = sum(a)/len(a), sum(b)/len(b)
    numerator = sum((u-ma)*(v-mb) for u, v in zip(a, b))
    denominator = math.sqrt(sum((u-ma)**2 for u in a)*sum((v-mb)**2 for v in b))
    corr = abs(numerator/denominator) if denominator else 0.0
    return mean_distance, ecdf, corr


def pattern_diagnostics(rows: list[tuple[int, int, str]], replicates: int = 10000, seed: int = 71) -> dict:
    """Exploratory checks, not a predictor or proof of a secure generator.

    Data had been visible before this protocol was fixed. Null samples match
    each puzzle's discrete width; Monte Carlo p-values use plus-one correction.
    """
    integer(replicates, 1)
    integer(seed)
    selected = [(n, k) for n, k, _ in rows if 8 <= n <= 70]
    if [n for n, _ in selected] != list(range(8, 71)):
        raise ValueError('requires every puzzle 8 through 70 in ascending order')
    widths = [1 << (n-1) for n, _ in selected]
    for (_, k), w in zip(selected, widths):
        if not w <= k < 2*w:
            raise ValueError('historical scalar outside its declared interval')
    observed = _statistics([(k-w)/w for (_, k), w in zip(selected, widths)])
    counts, rng = [0, 0, 0], random.Random(seed)
    for _ in range(replicates):
        simulated = _statistics([rng.randrange(w)/w for w in widths])
        for i in range(3):
            counts[i] += simulated[i] >= observed[i]
    names = ['absolute_mean_minus_half', 'uniform_ecdf_distance', 'absolute_lag1_correlation']
    return {'sample_size': len(selected), 'replicates': replicates, 'seed': seed,
            'protocol': 'exploratory; observed data available before protocol freeze; three tests',
            'tests': [{'name': name, 'statistic': stat, 'p_mc': (c+1)/(replicates+1),
                       'p_bonferroni': min(1.0, 3*(c+1)/(replicates+1))}
                      for name, stat, c in zip(names, observed, counts)]}
