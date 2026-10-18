import importlib.util
import math
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
SPEC = importlib.util.find_spec('research')
if SPEC is not None:
    import research as r

class ResearchTests(unittest.TestCase):
    def setUp(self):
        self.assertIsNotNone(SPEC, 'research module has not been implemented')

    def test_range_exact(self):
        self.assertEqual(r.HIGH-r.LOW, 1180591620717411303424)
        self.assertEqual(hex(r.LOW), '0x400000000000000000')
        self.assertEqual(hex(r.HIGH-1), '0x7fffffffffffffffff')

    def test_identity(self):
        self.assertEqual(r.add(None, r.G), r.G)
        self.assertEqual(r.add(r.G, None), r.G)

    def test_inverse_point(self):
        self.assertIsNone(r.add(r.G, (r.G[0], (-r.G[1]) % r.P)))

    def test_order(self):
        self.assertIsNone(r.mul(r.ORDER))
        self.assertIsNone(r.mul(0))

    def test_double(self):
        self.assertEqual(r.add(r.G, r.G), r.mul(2))

    def test_public_key_vector(self):
        self.assertEqual(r.compress(r.mul(1)).hex(),
          '0279be667ef9dcbbac55a06295ce870b07029bfcdb2dce28d959f2815b16f81798')

    def test_addresses_known(self):
        self.assertEqual(r.address(1), '1BgGZ9tcN4rm9KBzDn7KprQz87SZ26SAMH')
        self.assertEqual(r.address(2), '1cMh228HTCiwS8ZsaakH8A8wze1JR5ZsP')
        self.assertEqual(r.address(3), '1CUNEBjYrCn2y1SdiUMohaKUi4wpP326Lb')

    def test_bad_scalar(self):
        for k in [0, -1, r.ORDER, True, 1.5]:
            with self.subTest(k=k), self.assertRaises(ValueError):
                r.address(k)

    def test_bad_multiply(self):
        with self.assertRaises(ValueError): r.mul(-1)

    def test_compress_infinity(self):
        with self.assertRaises(ValueError): r.compress(None)

    def test_roundtrip_target(self):
        self.assertEqual(r.encode_address(r.decode_address(r.TARGET)), r.TARGET)
        self.assertEqual(len(r.decode_address(r.TARGET)), 20)

    def test_bad_address(self):
        for a in ['', '0'*34, r.TARGET[:-1]+'V', 'bc1qwrong']:
            with self.subTest(a=a), self.assertRaises(ValueError):
                r.decode_address(a)

    def test_wrong_network(self):
        a = r.b58check(b'\x6f' + bytes(20))
        with self.assertRaises(ValueError): r.decode_address(a)

    def test_encode_bad_length(self):
        with self.assertRaises(ValueError): r.encode_address(bytes(19))

    def test_fixture_count_and_ranges(self):
        rows = r.fixtures()
        self.assertEqual(len(rows), 83)
        self.assertEqual([x[0] for x in rows], list(range(1,71))+list(range(75,136,5)))
        for n,k,a in rows:
            with self.subTest(puzzle=n):
                self.assertTrue(2**(n-1) <= k < 2**n)
                self.assertEqual(r.address(k), a)

    def test_incremental_path(self):
        for k in [1, 2, 31, 255, 256, 65535, r.LOW, r.HIGH-2]:
            self.assertEqual(r.add(r.mul(k), r.G), r.mul(k+1))

    def test_scan_hit_first(self):
        self.assertEqual(r.scan(r.address(3),3,5), (3,1))

    def test_scan_hit_last(self):
        self.assertEqual(r.scan(r.address(7),4,8), (7,4))

    def test_scan_no_hit(self):
        self.assertEqual(r.scan(r.address(7),4,7), (None,3))

    def test_scan_rejects_bad_interval(self):
        for a,b in [(0,4),(4,4),(7,4),(1,65538),(r.ORDER-1,r.ORDER+1)]:
            with self.subTest(a=a,b=b), self.assertRaises(ValueError):
                r.scan(r.TARGET,a,b)

    def test_probabilities_small(self):
        out=r.estimates(1,4)
        self.assertAlmostEqual(out['sweep_seconds'],4)
        self.assertAlmostEqual(out['without_replacement_mean_seconds'],2.5)
        self.assertAlmostEqual(out['replacement_median_seconds'],math.log(.5)/math.log(.75))
        self.assertAlmostEqual(r.hit_probability(1,4),.25)
        self.assertAlmostEqual(r.hit_probability(2,4),.4375)

    def test_tiny_probability_nonzero(self):
        self.assertGreater(r.hit_probability(4096,r.HIGH-r.LOW),0)
        self.assertAlmostEqual(r.hit_probability(4096,r.HIGH-r.LOW)/(4096/(r.HIGH-r.LOW)),1)

    def test_probability_bad_inputs(self):
        for m,n in [(-1,4),(1,0),(1,1),(1.2,4),(True,4)]:
            with self.subTest(m=m,n=n), self.assertRaises(ValueError):
                r.hit_probability(m,n)
        for rate in [0,-1,float('inf'),float('nan'),True]:
            with self.subTest(rate=rate), self.assertRaises(ValueError):
                r.estimates(rate)

    def test_chain_summary_valid(self):
        s={'funded_txo_count':70,'funded_txo_sum':710192391,
           'spent_txo_count':0,'spent_txo_sum':0,'tx_count':70}
        self.assertEqual(r.chain_summary({'address':r.TARGET,'chain_stats':s}),
            {'balance_sats':710192391,'utxo_count':70,'spent_txo_count':0,'tx_count':70})

    def test_chain_summary_rejects_wrong_address(self):
        with self.assertRaises(ValueError):
            r.chain_summary({'address':'wrong','chain_stats':{}})

    def test_chain_summary_rejects_missing_and_inconsistent(self):
        s={'funded_txo_count':1,'funded_txo_sum':10,
           'spent_txo_count':2,'spent_txo_sum':11,'tx_count':1}
        for val in [{}, {'address':r.TARGET,'chain_stats':s}]:
            with self.subTest(val=val), self.assertRaises(ValueError):
                r.chain_summary(val)

    def test_statistics_deterministic(self):
        a=r.pattern_diagnostics(r.fixtures(),replicates=100,seed=71)
        b=r.pattern_diagnostics(r.fixtures(),replicates=100,seed=71)
        self.assertEqual(a,b)
        self.assertEqual(a['sample_size'],63)
        self.assertEqual(len(a['tests']),3)
        for x in a['tests']:
            self.assertTrue(0 < x['p_mc'] <= x['p_bonferroni'] <= 1)

if __name__=='__main__': unittest.main()
