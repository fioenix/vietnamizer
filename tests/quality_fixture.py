"""Synthetic quality-review inputs; never load the owner's research archive.

The historical Jev recovery verifier is outside these annotation tests. Its
boundary is stubbed for this generated cohort only; packet/raw/manifest checks
in quality_review and quality_review_v2 remain real and unmodified.
"""
from contextlib import ExitStack, contextmanager
import json
from pathlib import Path
import tempfile
from types import SimpleNamespace
from unittest.mock import patch

from benchmarks import quality_review as q


def stream(payload):
    return "\n".join(json.dumps(event, ensure_ascii=False) for event in (
        {"type": "item.completed", "item": {"type": "agent_message",
         "text": json.dumps({"payload": json.dumps(payload, ensure_ascii=False)})}},
        {"type": "turn.completed", "usage": {}},
    ))


@contextmanager
def quality_cohort(inherited=False):
    from benchmarks import jev_finish as finish
    from benchmarks import quality_review_v2 as v

    with tempfile.TemporaryDirectory(prefix="quality-synthetic-") as folder, ExitStack() as stack:
        root = Path(folder)
        recovery, epoch = root / "recovery", root / "epoch"
        cases = [{"id": f"P{i:02}", "source": f"Tôi đã viết đoạn {i}.",
                  "audience": "Bạn đọc", "purpose": "Kiểm thử tổng hợp"}
                 for i in range(1, 21)]
        q.save(root / "frozen-corpus.json", {"cases": cases})
        rows, key = [], {}
        for case in cases:
            for arm in q.ARMS:
                ident = f"R{len(rows) + 1:03}"
                cell = f"codex/{case['id']}/{arm}"
                target = epoch / "attempts" / f"codex-{case['id']}-{arm}"
                target.mkdir(parents=True)
                raw = "\n".join(json.dumps(event, ensure_ascii=False) for event in (
                    {"type": "item.completed", "item": {"type": "agent_message",
                     "text": json.dumps({"text": case["source"]}, ensure_ascii=False)}},
                    {"type": "turn.completed", "usage": {}},
                ))
                (target / "stdout.txt").write_text(raw)
                q.save(target / "result.json", {"cell": cell, "status": "completed",
                       "text": case["source"], "stdout_digest": q.digest(raw.encode())})
                rows.append({"review_id": ident, **case, "output": case["source"]})
                key[ident] = {"cell": cell, "epoch": str(epoch)}
        q.save(recovery / "finish-blinded-review.json", rows)
        q.save(recovery / "finish-review-key.json", key)
        q.save(recovery / "finish-report.json", {"completed": 20, "answered_jev_cases": 20})
        q.save(recovery / "manifest.json", {"origin": str(root)})
        stack.enter_context(patch.object(q, "RECOVERY", recovery))
        stack.enter_context(patch.object(q, "grade_prompt", q.grade_prompt))

        def synthetic_recovery_only(path):
            if Path(path) != recovery:
                raise AssertionError("Unexpected historical recovery access")
            return {"fixture": "synthetic annotation cohort"}

        stack.enter_context(patch.object(finish, "verify", side_effect=synthetic_recovery_only))
        stack.enter_context(patch.object(q.base, "execute", side_effect=AssertionError("No live model calls in tests")))
        if inherited:
            parent = root / "parent-review"
            q.prepare(parent)
            packet = q.read(parent / "packets/M1.json")
            inventory = {"sources": [{"id": p["id"], "uncertain": False, "issues": []}
                                     for p in packet]}
            with patch.object(q.base, "execute", return_value=SimpleNamespace(
                    stdout=stream(inventory), stderr="", returncode=0)):
                q.call_model(parent, "M1", "sources", q.inventory_prompt(packet),
                             lambda reply: q.validate_inventory(packet, reply))
            with patch.object(q.base, "execute", return_value=SimpleNamespace(
                    stdout=stream({"invalid_fixture_grade": True}), stderr="", returncode=0)):
                try:
                    q.call_model(parent, "M1", "Q001", q.grade_prompt(packet[0], inventory["sources"][0]),
                                 lambda reply: q.validate_grade(packet[0], inventory["sources"][0], reply))
                except ValueError:
                    pass
                else:
                    raise AssertionError("Invalid synthetic grade must remain failed")
            q.verify(parent)
            stack.enter_context(patch.object(v, "ORIGIN", parent))
        yield
