#!/usr/bin/env python3
"""Low-volume research probe. Never establishes country, retention or full integrity.

Input is an operator-reviewed JSON list, not a public URL endpoint. Redirects are
reported but never followed. DNS is checked then pinned; TLS SNI stays original.
Only up to 4096 body bytes are read. No credentials or environment proxy support.
"""
import argparse
import datetime as dt
import hashlib
import http.client
import ipaddress
import json
from pathlib import Path
import re
import socket
import ssl
import time
from urllib.parse import unquote, urlsplit

LIMIT = 4096


def validate_url(url, allowed_hosts, allow_http=False):
    if not isinstance(url, str) or len(url) > 2048 or any(ord(c) <= 32 for c in url):
        raise ValueError('invalid_url')
    p = urlsplit(url)
    schemes = {'https', 'http'} if allow_http else {'https'}
    if p.scheme not in schemes or p.hostname not in set(allowed_hosts):
        raise ValueError('unapproved_scheme_or_host')
    if p.username is not None or p.password is not None or p.query or p.fragment:
        raise ValueError('credentials_query_fragment_not_allowed')
    if p.port not in (None, 443 if p.scheme == 'https' else 80):
        raise ValueError('nonstandard_port')
    decoded = unquote(p.path)
    if '%' in decoded or '\\' in decoded or '..' in decoded.split('/') or any(ord(c) < 32 for c in decoded):
        raise ValueError('ambiguous_or_traversing_path')
    return p


def is_public(value):
    try:
        ip = ipaddress.ip_address(value)
        if isinstance(ip, ipaddress.IPv6Address) and ip.ipv4_mapped:
            ip = ip.ipv4_mapped
        return ip.is_global and not ip.is_multicast and not ip.is_reserved
    except ValueError:
        return False


def resolve_public(host, port):
    answers = socket.getaddrinfo(host, port, type=socket.SOCK_STREAM)
    ips = sorted({answer[4][0] for answer in answers})
    if not ips or not all(is_public(ip) for ip in ips):
        raise ValueError('nonpublic_or_mixed_dns')
    return ips[0]


class PinnedHTTP(http.client.HTTPConnection):
    def __init__(self, host, port, ip, timeout):
        super().__init__(host, port=port, timeout=timeout)
        self.pinned_ip = ip

    def connect(self):
        self.sock = socket.create_connection((self.pinned_ip, self.port), self.timeout)


class PinnedHTTPS(http.client.HTTPSConnection):
    def __init__(self, host, port, ip, timeout):
        super().__init__(host, port=port, timeout=timeout, context=ssl.create_default_context())
        self.pinned_ip = ip

    def connect(self):
        raw = socket.create_connection((self.pinned_ip, self.port), self.timeout)
        try:
            self.sock = self._context.wrap_socket(raw, server_hostname=self.host)
        except Exception:
            raw.close()
            raise


def classify(status, headers, body, limit=LIMIT):
    h = {key.lower(): value for key, value in headers.items()}
    result = {'outcome': 'unknown', 'range_supported': False,
              'full_hash_verified': False, 'signature_verified': False,
              'looks_like_inrelease': body.startswith(b'-----BEGIN PGP SIGNED MESSAGE-----')}
    if status in (404, 410):
        result['outcome'] = 'absent_at_candidate_url'
        return result
    if 300 <= status < 400:
        result['outcome'] = 'redirect_unfollowed'
        return result
    html = 'text/html' in h.get('content-type', '').lower() or body.lstrip().lower().startswith((b'<html', b'<!doctype html'))
    if html or status not in (200, 206) or not body:
        return result
    if status == 206:
        match = re.fullmatch(r'bytes 0-(\d+)/(\d+)', h.get('content-range', ''))
        if not match:
            return result
        end, total = map(int, match.groups())
        if total <= 0 or end != min(limit, total) - 1 or len(body) != end + 1:
            return result
        result['range_supported'] = True
    result['outcome'] = 'reachable_sample'
    return result


def probe_target(target, vantage):
    record = {'source_id': target.get('id'), 'url': None,
              'checked_at': dt.datetime.now(dt.timezone.utc).isoformat(),
              'vantage': vantage, 'vantage_is_operator_supplied': True,
              'country_verified': False, 'outage_tested': False,
              'full_hash_verified': False, 'signature_verified': False,
              'tls_verified': None, 'range_supported': None, 'http_status': None}
    started = time.monotonic()
    connection = None
    try:
        p = validate_url(target['url'], target['allowed_hosts'], target.get('allow_http', False))
        record['url'] = target['url']  # validated: no credentials or query tokens
        port = p.port or (443 if p.scheme == 'https' else 80)
        ip = resolve_public(p.hostname, port)
        record['connected_ip'] = ip
        cls = PinnedHTTPS if p.scheme == 'https' else PinnedHTTP
        connection = cls(p.hostname, port, ip, 10)
        connection.request('GET', p.path or '/', headers={
            'Range': f'bytes=0-{LIMIT-1}', 'Accept-Encoding': 'identity',
            'User-Agent': 'MelikaMirrorResearch/1.0 bounded-probe', 'Connection': 'close'})
        response = connection.getresponse()
        headers = {k.lower(): v for k, v in response.getheaders()}
        body = response.read(LIMIT)
        record.update(classify(response.status, headers, body))
        record.update({'http_status': response.status, 'sample_bytes': len(body),
                       'sample_sha256': hashlib.sha256(body).hexdigest(),
                       'tls_verified': p.scheme == 'https',
                       'content_type': headers.get('content-type'),
                       'content_range': headers.get('content-range'),
                       'retry_after': headers.get('retry-after')})
        # Do not persist signed Location URLs; only the hostname, without following.
        location = headers.get('location')
        record['redirect_host'] = urlsplit(location).hostname if location else None
    except (ValueError, KeyError, OSError, http.client.HTTPException) as exc:
        record.update({'outcome': 'unknown', 'error_type': type(exc).__name__})
    finally:
        if connection is not None:
            connection.close()
        record['duration_ms'] = round((time.monotonic() - started) * 1000, 2)
    return record


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--targets', type=Path, required=True)
    parser.add_argument('--vantage', required=True, help='Nonpersonal operator-supplied location label')
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    try:
        targets = json.loads(args.targets.read_text(encoding='utf-8'))
        if not isinstance(targets, list) or not 1 <= len(targets) <= 100:
            raise ValueError('targets must contain 1 to 100 reviewed entries')
        if not all(isinstance(t, dict) for t in targets):
            raise ValueError('each target must be an object')
        results = []
        for index, target in enumerate(targets):
            if index:
                time.sleep(1)
            results.append(probe_target(target, args.vantage))
        payload = {'schema_version': 1, 'probe_version': '1.0',
                   'scope': 'bounded transport observations only; no signature/full-hash/country proof',
                   'results': results}
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
        print(f'Recorded {len(results)} observations in {args.output}')
    except (OSError, ValueError, TypeError) as exc:
        parser.error(str(exc))


if __name__ == '__main__':
    main()
