#!/usr/bin/env python3
"""Render README figures from existing reports; never call a model/provider.

--check-data needs only the standard library. Rendering uses the optional,
hash-locked environment documented in README.md in this directory.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
REPORTS = (
    "specs/018-mr-version-comparison/results.md",
    "specs/025-section-voice-pilot/results.md",
)


def source_data():
    texts = [(ROOT / name).read_text() for name in REPORTS]
    cases = []
    for line in texts[0].splitlines():
        if not re.match(r"^\| MR\d{2} \|", line):
            continue
        cells = [s.strip().replace("**", "") for s in line.split("|")[1:-1]]
        assert cells[2] in ("Đạt", "Chưa đạt") and cells[3] in ("Đạt", "Chưa đạt")
        cases.append({"id": cells[0], "baseline_pass": cells[2] == "Đạt",
                      "revised_pass": cells[3] == "Đạt"})
    assert [x["id"] for x in cases] == [f"MR{i:02}" for i in range(1, 13)]
    judges = []
    for line in texts[1].splitlines():
        if not re.match(r"^\| D-C \|", line):
            continue
        cells = [s.strip() for s in line.split("|")[1:-1]]
        observed, planned = map(int, cells[2].split("/"))
        win, tie, loss = map(int, cells[3:6])
        assert win + tie + loss == observed <= planned
        judges.append({"judge": cells[1], "planned": planned, "observed": observed,
                       "win": win, "tie": tie, "loss": loss, "missing": planned - observed})
    assert [x["judge"] for x in judges] == ["Codex", "Gemini"]
    return {
        "schema": "readme-evidence-v1",
        "sources": [{"path": name, "sha256": hashlib.sha256((ROOT / name).read_bytes()).hexdigest()}
                    for name in REPORTS],
        "regression": {"editor": "Codex", "baseline": "0.12.0", "revised": "0.12.1",
                       "situations": 14, "outputs": 28, "cases": cases},
        "voice": {"editor": "Codex", "version": "0.13.2", "comparison": "D-C",
                  "criterion": "paired reference-voice preference", "judges": judges},
        "limits": ["development data, not holdout", "one generation per condition",
                   "model/agent labels, not independent human ratings",
                   "missing judgment is not imputed", "no population effect or p-value claim"],
    }


def render(data, export_dir=None):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.patches import Patch

    theme = json.loads((HERE / "brand-tokens.json").read_text())["colors"]
    plt.rcParams.update({
        "font.family": "DejaVu Sans", "font.size": 12,
        "text.color": theme["ink"], "axes.labelcolor": theme["ink"],
        "xtick.color": theme["muted"], "ytick.color": theme["ink"],
        "axes.spines.top": False, "axes.spines.right": False,
        "axes.spines.left": False, "axes.spines.bottom": False,
        "svg.hashsalt": "vietnamizer-readme-026", "svg.fonttype": "path",
        "hatch.linewidth": 0.7,
    })

    def save(fig, name, description):
        fig.savefig(HERE / (name + ".svg"), facecolor=theme["paper"],
                    metadata={"Date": None, "Description": description})
        # Matplotlib leaves line-end spaces in path attributes. Keep generated
        # output Git-clean without changing coordinates or path separators.
        svg = HERE / (name + ".svg")
        svg.write_text("\n".join(line.rstrip() for line in svg.read_text().splitlines()) + "\n")
        if export_dir:
            export_dir.mkdir(parents=True, exist_ok=True)
            fig.savefig(export_dir / (name + ".png"), dpi=300, facecolor=theme["paper"])
            fig.savefig(export_dir / (name + ".pdf"), facecolor=theme["paper"],
                        metadata={"CreationDate": None, "ModDate": None})
        plt.close(fig)

    def regression_figure(mobile=False):
        regression = data["regression"]
        cases = regression["cases"]
        counts = [sum(c[key] for c in cases) for key in ("baseline_pass", "revised_pass")]
        total = len(cases)
        fig, ax = plt.subplots(figsize=(4.2, 4.4) if mobile else (6.5, 3.9))
        fig.subplots_adjust(left=.21 if mobile else .16, right=.95, top=.64 if mobile else .69, bottom=.40 if mobile else .31)
        title = "Hồi quy: giữ câu đúng,\nsửa lỗi cụ thể" if mobile else "Hồi quy: giữ câu đúng, sửa lỗi cụ thể"
        fig.text(.07, .93 if mobile else .92, title, fontsize=15 if mobile else 16, weight="bold", va="top" if mobile else "baseline")
        fig.text(.07, .75 if mobile else .83, "Cùng Codex · 12 ca phát triển · 28 đầu ra", fontsize=9.5 if mobile else 11)
        for y, count in enumerate(counts):
            ax.barh(y, count, color=theme["violet"], height=.45)
            if count < total:
                ax.barh(y, total - count, left=count, color=theme["quiet"], height=.45)
            ax.text(count / 2, y, f"{count}/{total}", ha="center", va="center", fontsize=16, color=theme["paper"], weight="bold")
        ax.set(yticks=[0, 1], yticklabels=[regression["baseline"], regression["revised"]], xlim=(0, total),
               xticks=range(0, total + 1, 4 if mobile else 2), xlabel="Số ca đạt tiêu chí đã khóa")
        ax.invert_yaxis()
        ax.tick_params(axis="both", length=0, pad=8, labelsize=11 if mobile else 12)
        ax.set_axisbelow(True)
        ax.xaxis.grid(True, color=theme["quiet"], linewidth=.5)
        fig.text(.07, .16, "MR05 và MR12 chuyển sang đạt.\nKhông ca chuyển ngược." if mobile else "MR05 và MR12 chuyển sang đạt; không ca chuyển ngược.", fontsize=10)
        fig.text(.07, .05 if mobile else .07, "Một lượt/điều kiện. Nhãn agent + reviewer;\nkhông phải chấm người độc lập." if mobile else "Một lượt/điều kiện. Nhãn agent + reviewer; không phải chấm người độc lập.", fontsize=8.5 if mobile else 8.7)
        save(fig, "regression-cases" + ("-mobile" if mobile else ""), "Development regression only: 0.12.0 10/12, 0.12.1 12/12. Not population accuracy.")

    def voice_figure(mobile=False):
        rows = data["voice"]["judges"]
        fig, ax = plt.subplots(figsize=(4.2, 5.8) if mobile else (6.5, 4.6))
        fig.subplots_adjust(left=.22 if mobile else .20, right=.95, top=.65 if mobile else .68, bottom=.40)
        fig.text(.06, .94 if mobile else .93, "Theo giọng mẫu:\nkết quả còn trái chiều" if mobile else "Theo giọng mẫu: kết quả còn trái chiều", fontsize=15 if mobile else 16, weight="bold", va="top" if mobile else "baseline")
        fig.text(.06, .79 if mobile else .85, "Vietnamizer 0.13.2\nso với prompt + cùng mẫu" if mobile else "Vietnamizer 0.13.2 so với prompt + cùng mẫu", fontsize=10.5 if mobile else 11)
        fig.text(.06, .70 if mobile else .79, "Cùng Codex biên tập · hai model chấm ẩn nhãn", fontsize=8.5 if mobile else 10)
        categories = [("win", "Ưu tiên Vietnamizer" if mobile else "Vietnamizer được ưu tiên", theme["violet"]),
                      ("tie", "Hòa", theme["quiet"]),
                      ("loss", "Ưu tiên prompt" if mobile else "Prompt được ưu tiên", theme["mint"]),
                      ("missing", "Thiếu phiếu", theme["paper"])]
        for y, row in enumerate(rows):
            left = 0
            for key, label, color in categories:
                count = row[key]
                if count:
                    ax.barh(y, count, left=left, height=.46, color=color, hatch="////" if key == "missing" else None, edgecolor=theme["muted"], linewidth=0)
                    ax.text(left + count / 2, y, str(count), ha="center", va="center", color=theme["paper"] if key == "win" else theme["ink"], fontsize=16, weight="bold")
                left += count
            assert left == row["planned"]
        ax.set(yticks=range(len(rows)), yticklabels=[f"{r['judge']}\n{r['observed']}/{r['planned']} phiếu" for r in rows],
               xticks=range(0, 9, 2 if mobile else 1), xlim=(0, 8), xlabel="Số nguồn (8 dự kiến)" if mobile else "Số nguồn trong 8 nguồn dự kiến")
        ax.invert_yaxis()
        ax.tick_params(axis="both", length=0, pad=8, labelsize=10.5 if mobile else 12)
        handles = [Patch(facecolor=color, edgecolor=theme["muted"] if key == "missing" else "none", hatch="////" if key == "missing" else None, label=label) for key, label, color in categories]
        fig.legend(handles=handles, loc="lower left", bbox_to_anchor=(.04, .16), ncol=2, frameon=False, fontsize=9.2 if mobile else 10, handlelength=1.2, columnspacing=1.0)
        fig.text(.06, .06, "Tập phát triển; không phải tác giả chấm.\nV2–Gemini bị loại do trích sai.", fontsize=9)
        save(fig, "reference-voice" + ("-mobile" if mobile else ""), "Same Codex editor, paired model-judge preferences. Codex 5/3/0/0; Gemini 3/1/3/1 win/tie/loss/missing. Development data.")

    for mobile in (False, True):
        regression_figure(mobile)
        voice_figure(mobile)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--refresh-data", action="store_true")
    parser.add_argument("--check-data", action="store_true")
    parser.add_argument("--export-dir", type=Path)
    args = parser.parse_args()
    expected = source_data()
    target = HERE / "evidence.json"
    if args.refresh_data:
        target.write_text(json.dumps(expected, ensure_ascii=False, indent=2) + "\n")
    if json.loads(target.read_text()) != expected:
        raise SystemExit("Figure data/report hash drift; inspect source changes before --refresh-data")
    if args.check_data:
        print("Figure data matches both reports; all planned/missing outcome counts reconcile.")
        return
    render(expected, args.export_dir)


if __name__ == "__main__":
    main()
