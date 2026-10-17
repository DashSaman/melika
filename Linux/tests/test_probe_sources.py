import importlib.util
import pathlib
import socket
import unittest
from unittest.mock import patch

PATH = pathlib.Path(__file__).resolve().parents[1] / 'scripts' / 'probe_sources.py'
if PATH.exists():
    spec = importlib.util.spec_from_file_location('probe_sources', PATH)
    probe = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(probe)
else:
    probe = None

class DeliveryTest(unittest.TestCase):
    def test_probe_implementation_exists(self):
        self.assertTrue(PATH.is_file(), 'Research probe implementation has not been created yet')

@unittest.skipIf(probe is None, 'implementation not created yet')
class ProbeTests(unittest.TestCase):
    def test_valid_https(self):
        p = probe.validate_url('https://mirror.example/ubuntu/file', ['mirror.example'])
        self.assertEqual(p.hostname, 'mirror.example')

    def test_disallowed_host(self):
        with self.assertRaises(ValueError):
            probe.validate_url('https://other.example/file', ['mirror.example'])

    def test_credentials_rejected(self):
        with self.assertRaises(ValueError):
            probe.validate_url('https://user:secret@mirror.example/file', ['mirror.example'])

    def test_query_rejected(self):
        with self.assertRaises(ValueError):
            probe.validate_url('https://mirror.example/file?token=secret', ['mirror.example'])

    def test_traversal_rejected(self):
        for path in ['/../secret', '/%2e%2e/secret', '/%252e%252e/secret', '/a\\b']:
            with self.subTest(path=path), self.assertRaises(ValueError):
                probe.validate_url('https://mirror.example' + path, ['mirror.example'])

    def test_http_requires_opt_in(self):
        with self.assertRaises(ValueError):
            probe.validate_url('http://mirror.example/file', ['mirror.example'])
        self.assertEqual(probe.validate_url('http://mirror.example/file', ['mirror.example'], True).scheme, 'http')

    def test_nonstandard_port_rejected(self):
        with self.assertRaises(ValueError):
            probe.validate_url('https://mirror.example:9000/file', ['mirror.example'])

    def test_private_and_special_addresses(self):
        for ip in ['127.0.0.1', '10.1.2.3', '169.254.169.254', '::1', 'fc00::1', '::ffff:127.0.0.1', '224.0.0.1']:
            self.assertFalse(probe.is_public(ip), ip)
        self.assertTrue(probe.is_public('1.1.1.1'))

    def test_mixed_dns_rejected(self):
        answers = [(socket.AF_INET, socket.SOCK_STREAM, 6, '', ('1.1.1.1', 443)),
                   (socket.AF_INET, socket.SOCK_STREAM, 6, '', ('127.0.0.1', 443))]
        with patch.object(probe.socket, 'getaddrinfo', return_value=answers), self.assertRaises(ValueError):
            probe.resolve_public('mirror.example', 443)

    def test_dns_public_result(self):
        answers = [(socket.AF_INET, socket.SOCK_STREAM, 6, '', ('1.1.1.1', 443))]
        with patch.object(probe.socket, 'getaddrinfo', return_value=answers):
            self.assertEqual(probe.resolve_public('mirror.example', 443), '1.1.1.1')

    def test_valid_range(self):
        r = probe.classify(206, {'content-range': 'bytes 0-3/10'}, b'abcd', 4)
        self.assertEqual(r['outcome'], 'reachable_sample')
        self.assertTrue(r['range_supported'])
        self.assertFalse(r['full_hash_verified'])

    def test_invalid_range(self):
        for header in ['bytes 2-5/10', 'bytes 0-9/5', 'bytes 0-7/20', 'invalid']:
            r = probe.classify(206, {'content-range': header}, b'abcd', 4)
            self.assertEqual(r['outcome'], 'unknown', header)
            self.assertFalse(r['range_supported'])

    def test_range_ignored(self):
        r = probe.classify(200, {'content-type': 'application/octet-stream'}, b'abcd', 4)
        self.assertEqual(r['outcome'], 'reachable_sample')
        self.assertFalse(r['range_supported'])

    def test_html_is_not_artifact(self):
        r = probe.classify(200, {'content-type': 'text/html'}, b'<html>login</html>', 4096)
        self.assertEqual(r['outcome'], 'unknown')

    def test_absent_vs_unknown(self):
        for status in [404, 410]:
            self.assertEqual(probe.classify(status, {}, b'', 4096)['outcome'], 'absent_at_candidate_url')
        for status in [403, 429, 500, 503]:
            self.assertEqual(probe.classify(status, {}, b'', 4096)['outcome'], 'unknown')

    def test_redirect_is_not_followed_or_verified(self):
        r = probe.classify(302, {'location': 'https://example.net/file?token=secret'}, b'', 4096)
        self.assertEqual(r['outcome'], 'redirect_unfollowed')
        self.assertFalse(r['full_hash_verified'])

    def test_pgp_prefix_is_not_signature_verification(self):
        r = probe.classify(200, {}, b'-----BEGIN PGP SIGNED MESSAGE-----\n', 4096)
        self.assertTrue(r['looks_like_inrelease'])
        self.assertFalse(r['signature_verified'])

if __name__ == '__main__':
    unittest.main()
