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
all_script = script_path.read_text(encoding="utf-8", errors="ignore") if script_path.exists() else ""

errors: list[str] = []
warnings: list[str] = []


def err(msg: str) -> None:
    errors.append("ERROR: " + msg)


def warn(msg: str) -> None:
    warnings.append("WARN: " + msg)


forbidden_in_tex = [
    "fig1_architecture_tikz",
    "fig0_application_scenario_tikz",
    "fig1_model_architecture",
    "draft block diagram",
    "paper-ready-v3",
    "outputs/paper_ready_v3",
    r"\resizebox{0.98\columnwidth}",
]
for pat in forbidden_in_tex:
    if pat in all_tex:
        err(f"forbidden in PDF source: {pat}")

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

if "fig1_application_scenario.pdf" not in all_tex:
    err("Fig.1 must reference figures/fig1_application_scenario.pdf")
if "fig2_architecture.pdf" not in all_tex:
    err("Fig.2 must reference figures/fig2_architecture.pdf")

fig1_pdf = root / "figures" / "fig1_application_scenario.pdf"
fig2_pdf = root / "figures" / "fig2_architecture.pdf"
if not fig1_pdf.exists():
    err(f"missing vector PDF: {fig1_pdf.name}")
if not fig2_pdf.exists():
    err(f"missing vector PDF: {fig2_pdf.name}")

if re.search(r"Fig\.\s+[123]\b", all_tex):
    err("hard-coded Fig. 1/2/3 numbering found; use \\ref{fig:...}")

if re.search(r"conca[\s\-\+]|fusion\]\[:5\]", all_script.lower()):
    err("cryptic result-figure label may remain in figure generation script")

if "Data and Code Availability" not in all_tex:
    warn("Data and Code Availability section not found in PDF source")

table_files = {
    "tab:cross_day_main": (root / "tables" / "table1_cross_day.tex", ["shown in bold"]),
    "tab:fusion_chirp": (root / "tables" / "table2_fusion_chirp.tex", ["shown in bold"]),
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
    if not re.search(r"\\caption\{", cap_text):
        err(f"caption missing in {path.name}")
        continue
    for needle in needles:
        if needle.lower() not in cap_text:
            err(f"{label}: caption must mention '{needle}' marking rule")

print("LAYOUT VISUAL AUDIT")
print("MANUAL FIGURE CHECK:")
print(" - Fig.1 must be a compact horizontal single-column scenario diagram.")
print(" - Fig.2 must be a vector PDF drawn with clean swimlanes and orthogonal connectors.")
print(" - No arrow may cross text or pass through a node.")
print(" - If Fig.2 still looks like a TikZ scratch diagram, reject v2 and revert to v1.")
print(" - Table emphasis must be visually checked in the compiled PDF.")
print("MANUAL CHECK REQUIRED:")
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
