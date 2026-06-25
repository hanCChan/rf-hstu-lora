#!/usr/bin/env python3
"""Audit PDF-source layout rules: figures, forbidden labels, table marking notes."""

from __future__ import annotations

import re
import sys
from pathlib import Path

root = Path(__file__).resolve().parent

tex_paths = [root / "main.tex"] + list((root / "sections").glob("*.tex")) + list((root / "tables").glob("*.tex"))
script_path = root.parents[1] / "scripts" / "paper" / "generate_final_figures.py"

texts: list[tuple[Path, str]] = []
for p in tex_paths:
    if p.exists():
        texts.append((p, p.read_text(encoding="utf-8", errors="ignore")))
all_tex = "\n".join(t for p, t in texts if p.suffix == ".tex")
tables_tex = "\n".join(t for p, t in texts if p.parent.name == "tables")
all_script = script_path.read_text(encoding="utf-8", errors="ignore") if script_path.exists() else ""

errors: list[str] = []
warnings: list[str] = []


def err(msg: str) -> None:
    errors.append("ERROR: " + msg)


def warn(msg: str) -> None:
    warnings.append("WARN: " + msg)


forbidden_text = [
    ("draft block diagram", "draft block diagram remains"),
    ("fig1_model_architecture", "old matplotlib Fig.1 should not be referenced in PDF source"),
    ("paper-ready-v3", "branch name should not appear in PDF source"),
    ("outputs/paper_ready_v3", "internal output path should not appear in PDF source"),
    ("PAPER_RESULTS_SUMMARY", "internal results summary path should not appear in PDF source"),
    (r"\resizebox{0.98\columnwidth}", "resizebox 0.98 columnwidth remains"),
]
figures_tex = "\n".join(
    p.read_text(encoding="utf-8", errors="ignore")
    for p in (root / "figures").glob("*.tex")
    if p.exists()
)
if re.search(r"shift/\.style", figures_tex):
    err('TikZ style name "shift" conflicts with /tikz/shift; rename to factorlbl or similar')

for pat, msg in forbidden_text:
    if pat in all_tex:
        err(msg)

forbidden_labels = [
    "fig:cross_receiver_stress",
    "fig:cross_day_seed_bars",
    "fig:fusion_chirp_ablation",
    "fig:distance_shift",
]
for label in forbidden_labels:
    if label in all_tex:
        err(f"forbidden figure label remains: {label}")

if re.search(r"\\texttt\{paper-ready", all_tex):
    err("branch name in texttt should not appear in PDF source")

if re.search(r"\\appendices[\s\S]*?\\section\{Reproducibility\}", all_tex):
    err("Appendix Reproducibility section must be removed")
if re.search(r"\\section\{Reproducibility\}", all_tex):
    err("Raw Reproducibility section must be replaced by Data and Code Availability")

required_labels = [
    "fig:application_scenario",
    "fig:architecture",
    "fig:results_summary",
]
for label in required_labels:
    if label not in all_tex:
        err(f"required figure label missing: {label}")

if "fig0_application_scenario_tikz" not in all_tex:
    err("application scenario TikZ source not referenced")

if "fig1_architecture_tikz" not in all_tex:
    err("TikZ architecture figure source not referenced")

if re.search(r"Fig\.\s+[123]\b", all_tex):
    err("hard-coded Fig. 1/2/3 numbering found; use \\ref{fig:...}")

if re.search(r"conca[\s\-\+]|fusion\]\[:5\]", all_script.lower()):
    err("cryptic result-figure label may remain in figure generation script")

if "Data and Code Availability" not in all_tex:
    warn("Data and Code Availability section not found in PDF source")

# Table marking caption checks (per-table file to avoid nested-brace caption parsing issues)
table_files = {
    "tab:cross_day_main": (root / "tables" / "table1_cross_day.tex", ["best", "second"]),
    "tab:fusion_chirp": (root / "tables" / "table2_fusion_chirp.tex", ["best", "second"]),
    "tab:deployment_shift": (root / "tables" / "table3_deployment_shift.tex", ["higher value in each row"]),
    "tab:cross_receiver": (root / "tables" / "table4_cross_receiver.tex", ["higher value in each transfer direction"]),
}
for label, (path, needles) in table_files.items():
    if not path.exists():
        err(f"table file missing for {label}")
        continue
    cap_text = path.read_text(encoding="utf-8").lower()
    if f"\\label{{{label}}}" not in cap_text:
        err(f"label missing in {path.name}: {label}")
    cap_match = re.search(r"\\caption\{", cap_text)
    if not cap_match:
        err(f"caption missing in {path.name}")
        continue
    for needle in needles:
        if needle.lower() not in cap_text:
            err(f"{label}: caption must mention '{needle}' marking rule")

print("LAYOUT VISUAL AUDIT")
print("MANUAL CHECK REQUIRED:")
print(" - Fig.1 application scenario: professional, deployment shifts visible, no cartoon style.")
print(" - Fig.2 architecture/modules: (a) overall, (b) CNN inset, (c) cross-attention inset readable.")
print(" - Fig.3 results: legend not overlapping; y ticks visible in all panels.")
print(" - Cross-receiver figure removed; Table VI retained.")
for w in warnings:
    print(" - " + w)
for e in errors:
    print(" - " + e)

if errors:
    print("LAYOUT VISUAL AUDIT: FAIL")
    sys.exit(1)
print("LAYOUT VISUAL AUDIT: PASS")
