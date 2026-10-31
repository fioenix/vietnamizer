"""Offline candidate/routing evidence format checks; no model or semantic grading.

A supplied receipt list can be checked for order/hash, not authenticated as actual
agent tool use. This module never calls Git, a model, a service, or an evaluator.
"""
import hashlib
import json
from pathlib import Path, PurePosixPath


def digest(value):
    if not isinstance(value, bytes):
        value = json.dumps(value, ensure_ascii=False, sort_keys=True).encode()
    return hashlib.sha256(value).hexdigest()


def prepare(case, root, candidate):
    """Bind the current candidate bytes and explicit expected reads, not HEAD."""
    root = Path(root).resolve()
    reads = []
    for name in case['required_reads']:
        path = PurePosixPath(name)
        if path.is_absolute() or '..' in path.parts or '\\' in name:
            raise ValueError('read path outside authorized root')
        target = (root / name).resolve()
        if not target.is_relative_to(root):
            raise ValueError('read target outside authorized root')
        reads.append({'path': name, 'sha256': digest(target.read_bytes())})
    packet = {'schema': 'vietnamizer-review-v1', 'case_id': case['id'],
              'task': case['task'], 'source': case['source'],
              'candidate': candidate.decode('utf-8'), 'candidate_sha256': digest(candidate),
              'required_reads': reads}
    packet['packet_sha256'] = digest(packet)
    return packet


def check(packet, report, current_candidate, trace=None):
    """Reject stale artifacts/fabricated quotes; leave judgment truth ungraded."""
    unsigned = {k: v for k, v in packet.items() if k != 'packet_sha256'}
    if digest(unsigned) != packet['packet_sha256'] or report.get('packet_sha256') != packet['packet_sha256']:
        raise ValueError('wrong or altered review packet')
    current_hash = digest(current_candidate)
    if (current_hash != packet['candidate_sha256'] or current_hash != report.get('candidate_sha256')
            or current_candidate.decode('utf-8') != packet['candidate']):
        raise ValueError('candidate changed; review current bytes in a new packet')
    if 'overall_score' in report or 'combined_score' in report:
        raise ValueError('meaning and style are separate judgments')
    for axis in ('meaning', 'style'):
        judgment = report.get(axis, {})
        if judgment.get('status') not in {'clear', 'issue', 'uncertain', 'not_assessed'}:
            raise ValueError('missing independent ' + axis + ' judgment')
        findings = judgment.get('findings', [])
        if (not isinstance(findings, list) or judgment['status'] == 'issue' and not findings
                or judgment['status'] in {'clear', 'not_assessed'} and findings):
            raise ValueError('verdict and findings must be consistent')
        for finding in findings:
            source_quote = finding.get('source_quote', '')
            candidate_quote = finding.get('candidate_quote', '')
            if (not isinstance(source_quote, str) or source_quote not in packet['source']
                    or not isinstance(candidate_quote, str) or not candidate_quote
                    or candidate_quote not in packet['candidate'] or not finding.get('reason')):
                raise ValueError('finding quote or reason is not supported by packet text')
    routing = 'absent'
    if trace is not None:
        if not isinstance(trace, list) or any(not isinstance(e, dict) for e in trace):
            raise ValueError('trace must be an event list')
        positions = [i for i, e in enumerate(trace) if e.get('event') == 'review']
        if len(positions) != 1 or trace[positions[0]].get('candidate_sha256') != current_hash:
            raise ValueError('trace needs one review of the bound candidate')
        before_review = {e.get('path'): e.get('sha256') for e in trace[:positions[0]] if e.get('event') == 'read'}
        if any(before_review.get(f['path']) != f['sha256'] for f in packet['required_reads']):
            raise ValueError('required rubric/reference was not read before review in supplied trace')
        routing = 'ordered_receipts_match_packet'
    return {'candidate_binding': 'verified', 'meaning_status': report['meaning']['status'],
            'style_status': report['style']['status'], 'provided_trace': routing,
            'actual_agent_reads': 'not_attested', 'semantic_correctness': 'not_evaluated'}
