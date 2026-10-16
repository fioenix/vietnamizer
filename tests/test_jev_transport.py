import json
import os
import tempfile
from pathlib import Path
import unittest
import subprocess
import sys
import time
import urllib.error
import urllib.request
from unittest.mock import patch

from jev.transport import NoRedirect, ServiceError, request as bounded_request, _request_once as request


class Reply:
    def __init__(self, data): self.data = data
    def __enter__(self): return self
    def __exit__(self, *_): return False
    def read(self, size): return self.data[:size]


class TransportTest(unittest.TestCase):
    def test_invalid_json_is_invalid_response_not_service_outage(self):
        class Opener:
            def open(self, req, timeout): return Reply(b'not-json PRIVATE')
        with patch('urllib.request.build_opener', return_value=Opener()):
            with self.assertRaises(ServiceError) as caught:
                request({'model': 'jev-1.14.0'}, 'test-key', 1)
        self.assertEqual(caught.exception.category, 'invalid_response')
        self.assertNotIn('PRIVATE', str(caught.exception))

    def test_fixed_origin_auth_and_bounded_response(self):
        seen = []
        class Opener:
            def open(self, req, timeout):
                seen.append((req.full_url, req.get_header('Authorization'), timeout))
                return Reply(json.dumps({'model': 'jev-1.14.0'}).encode())
        with patch('urllib.request.build_opener', return_value=Opener()):
            self.assertEqual(request({'model': 'jev-1.14.0'}, 'test-key', 2)['model'], 'jev-1.14.0')
        self.assertEqual(seen, [('https://api.typesafe.ai/v1/systemone', 'Bearer test-key', 2)])
        class HugeOpener:
            def open(self, req, timeout): return Reply(b'x' * (1024*1024+1))
        with patch('urllib.request.build_opener', return_value=HugeOpener()):
            with self.assertRaises(ServiceError) as caught: request({}, 'test-key', 1)
        self.assertEqual(caught.exception.category, 'invalid_response')

    def test_planner_and_http_use_identical_bytes(self):
        from jev.core import encoded
        seen = []
        class Opener:
            def open(self, req, timeout):
                seen.append(req.data)
                return Reply(b'{}')
        payload = {'state': {'text': 'Tiếng Việt'}, 'questions': {'x': {'type': 'noul'}}}
        with patch('urllib.request.build_opener', return_value=Opener()):
            request(payload, 'test-key', 1)
        self.assertEqual(seen, [encoded(payload)])

    def test_absolute_deadline_kills_stalled_and_dripping_worker(self):
        real_popen = subprocess.Popen
        for script in ('import time; time.sleep(30)',
                       'import sys,time\nwhile True:\n sys.stdout.write("x"); sys.stdout.flush(); time.sleep(.03)'):
            children = []
            def stalled(*args, **kwargs):
                child = real_popen([sys.executable, '-c', script], **kwargs)
                children.append(child)
                return child
            started = time.monotonic()
            with patch('jev.transport.subprocess.Popen', side_effect=stalled):
                with self.assertRaises(ServiceError) as caught:
                    bounded_request({}, 'test-key', .15)
            self.assertEqual(caught.exception.category, 'deadline_exceeded')
            self.assertLess(time.monotonic()-started, 2)
            self.assertIsNotNone(children[0].poll())

    def test_worker_ignores_hostile_cwd_imports(self):
        real_popen=subprocess.Popen
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory);marker=root/'imported'
            (root/'json.py').write_text('from pathlib import Path; Path('+repr(str(marker))+').touch(); raise RuntimeError("hostile")')
            def harmless(command,**kwargs):
                command=list(command)
                command[command.index('-c')+1]='import sys; sys.path.insert(0,sys.argv[1]); import jev.transport as t; sys.stdout.buffer.write(t.encoded({"reply":{}}))'
                return real_popen(command,cwd=directory,**kwargs)
            with patch('jev.transport.subprocess.Popen',side_effect=harmless):
                self.assertEqual(bounded_request({},'fixture',2),{})
            self.assertFalse(marker.exists())

    def test_keyboard_interrupt_collects_child(self):
        real_popen=subprocess.Popen;children=[]
        def interrupt(*args,**kwargs):
            child=real_popen([sys.executable,'-c','import time; time.sleep(30)'],**kwargs)
            child.communicate=lambda *a,**k: (_ for _ in ()).throw(KeyboardInterrupt())
            children.append(child);return child
        try:
            with patch('jev.transport.subprocess.Popen',side_effect=interrupt):
                with self.assertRaises(KeyboardInterrupt):bounded_request({},'fixture',2)
            self.assertIsNotNone(children[0].poll())
        finally:
            if children and children[0].poll() is None:children[0].kill();children[0].wait()

    def test_worker_has_own_absolute_watchdog(self):
        root=str(Path(__file__).resolve().parents[1])
        command=[sys.executable,'-I','-B','-c','import sys,time; sys.path.insert(0,sys.argv[1]); import jev.transport as t; t._request_once=lambda *a:time.sleep(30); t._worker()',root]
        with subprocess.Popen(command,stdin=subprocess.PIPE,stdout=subprocess.PIPE) as child:
            try:
                child.communicate(json.dumps({'payload':{},'key':'fixture','timeout':.15}).encode(),timeout=2)
                self.assertEqual(child.returncode,124)
            except subprocess.TimeoutExpired:
                child.kill();child.wait();self.fail('worker survived its own deadline')

    def test_redirect_cannot_forward_authorization(self):
        req = urllib.request.Request('https://api.typesafe.ai/v1/systemone', headers={'Authorization':'Bearer test-key'})
        result = NoRedirect().redirect_request(req, None, 302, 'moved', {}, 'https://other.invalid/')
        self.assertIsNone(result)

    def test_authentication_failure_never_echoes_error_body(self):
        class Opener:
            def open(self, req, timeout):
                raise urllib.error.HTTPError(req.full_url, 401, 'PRIVATE test-key', {}, None)
        with patch('urllib.request.build_opener', return_value=Opener()):
            with self.assertRaises(ServiceError) as caught: request({}, 'test-key', 1)
        self.assertEqual(str(caught.exception), 'authentication_failed')
