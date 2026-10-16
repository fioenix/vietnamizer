"""Fixed-origin TypeSafe transport. Errors never include response bodies."""
import json
import os
import threading
import subprocess
import sys
import time
from pathlib import Path
import urllib.request
import urllib.error

MODEL = 'jev-1.14.0'
ENDPOINT = 'https://api.typesafe.ai/v1/systemone'
MAX_RESPONSE = 1024 * 1024


class ServiceError(Exception):
    def __init__(self, category):
        self.category = category
        super().__init__(category)


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def encoded(value):
    return json.dumps(value,ensure_ascii=False,allow_nan=False,separators=(',',':')).encode()


def _request_once(payload, key, timeout):
    req = urllib.request.Request(ENDPOINT, data=encoded(payload),
        headers={'Authorization':'Bearer '+key,'Content-Type':'application/json'}, method='POST')
    try:
        with urllib.request.build_opener(NoRedirect()).open(req,timeout=timeout) as reply:
            data = reply.read(MAX_RESPONSE+1)
        if len(data)>MAX_RESPONSE:
            raise ServiceError('invalid_response')
        try:
            return json.loads(data)
        except (ValueError, UnicodeError, RecursionError):
            raise ServiceError('invalid_response') from None
    except urllib.error.HTTPError as error:
        raise ServiceError('authentication_failed' if error.code in (401,403) else 'service_failed') from None
    except ServiceError:
        raise
    except (OSError, ValueError, TimeoutError):
        raise ServiceError('service_failed') from None


def _worker():
    # Only the bounded child performs I/O. Secrets/prose travel over stdin, never argv/files.
    try:
        envelope=json.load(sys.stdin)
        watchdog=threading.Timer(envelope['timeout'],lambda:os._exit(124))
        watchdog.daemon=True;watchdog.start()
        try:
            reply=_request_once(envelope['payload'],envelope['key'],envelope['timeout'])
            result={'reply':reply}
        finally:watchdog.cancel()
    except ServiceError as error:
        result={'error':error.category}
    except Exception:
        result={'error':'service_failed'}
    sys.stdout.buffer.write(encoded(result))


def request(payload, key, timeout):
    # A socket timeout measures inactivity. A killable process bounds DNS, TLS,
    # response headers and drip-fed bodies together, without leaving a live thread.
    started=time.monotonic()
    root=str(Path(__file__).resolve().parent.parent)
    command=[sys.executable,'-I','-B','-c',
        'import sys; sys.path.insert(0, sys.argv[1]); from jev.transport import _worker; _worker()',root]
    envelope=encoded({'payload':payload,'key':key,'timeout':timeout})
    try:
        with subprocess.Popen(command,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.DEVNULL) as child:
            try:
                remaining=timeout-(time.monotonic()-started)
                if remaining<=0: raise subprocess.TimeoutExpired(command,timeout)
                output,_=child.communicate(envelope,timeout=remaining)
            except subprocess.TimeoutExpired:
                child.kill()
                child.communicate()
                raise ServiceError('deadline_exceeded') from None
            except BaseException:
                child.kill();child.wait()
                raise
            if time.monotonic()-started>=timeout:
                raise ServiceError('deadline_exceeded')
            if child.returncode==124:raise ServiceError('deadline_exceeded')
            if child.returncode or len(output)>MAX_RESPONSE+1024:
                raise ServiceError('invalid_response')
        result=json.loads(output)
        if 'error' in result:
            category=result['error']
            raise ServiceError(category if category in ('authentication_failed','service_failed','invalid_response') else 'service_failed')
        return result['reply']
    except ServiceError:
        raise
    except (OSError,ValueError,KeyError,TypeError):
        raise ServiceError('service_failed') from None
