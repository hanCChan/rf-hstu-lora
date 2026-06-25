#!/usr/bin/env python3
"""Generate IoTJ Fig.1 (scenario) and Fig.2 (architecture) as vector PDFs."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

ROOT = Path(__file__).resolve().parent


def _box(ax, cx, cy, w, h, lines, fc="#ffffff", ec="#333333", lw=1.0, fontsize=7.5):
    x, y = cx - w / 2, cy - h / 2
    ax.add_patch(
        FancyBboxPatch(
            (x, y),
            w,
            h,
            boxstyle="round,pad=0.02,rounding_size=0.04",
            linewidth=lw,
            edgecolor=ec,
            facecolor=fc,
            zorder=2,
        )
    )
    ax.text(
        cx,
        cy,
        "\n".join(lines),
        ha="center",
        va="center",
        fontsize=fontsize,
        color="#111111",
        zorder=3,
        linespacing=1.15,
    )
    return {"left": x, "right": x + w, "top": y + h, "bottom": y, "cx": cx, "cy": cy}


def _seg(ax, x0, y0, x1, y1, lw=0.9, arrow_end=False):
    style = "-|>" if arrow_end else "-"
    ax.add_patch(
        FancyArrowPatch(
            (x0, y0),
            (x1, y1),
            arrowstyle=style,
            mutation_scale=8,
            linewidth=lw,
            color="#222222",
            shrinkA=0,
            shrinkB=0,
            zorder=1,
        )
    )


def _ortho(ax, pts, arrow_end=True):
    for i, ((x0, y0), (x1, y1)) in enumerate(zip(pts[:-1], pts[1:])):
        last = i == len(pts) - 2
        _seg(ax, x0, y0, x1, y1, arrow_end=arrow_end and last)


def fig1_scenario(out: Path) -> None:
    fig, ax = plt.subplots(figsize=(3.45, 0.95))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 2)
    ax.axis("off")

    xs = [1.0, 3.0, 5.0, 7.0, 9.0]
    cy = 1.0
    specs = [
        (1.55, 1.05, ["LoRa TXs", "(enrolled / rogue)"]),
        (1.75, 1.05, ["Deployment", "shifts"]),
        (1.75, 1.05, ["Gateway RF", "capture"]),
        (1.75, 1.05, ["OOB-guided", "RF-HSTU"]),
        (1.35, 1.05, ["ID / alert"]),
    ]
    boxes = [_box(ax, x, cy, w, h, lab) for x, (w, h, lab) in zip(xs, specs)]

    ax.text(3.0, 0.35, "day / distance / location / config / receiver", ha="center", fontsize=6, color="#444444")
    ax.text(5.0, 0.35, "IQ + OOB spectrum", ha="center", fontsize=6, color="#444444")

    for i in range(len(boxes) - 1):
        _seg(ax, boxes[i]["right"] + 0.03, cy, boxes[i + 1]["left"] - 0.03, cy, arrow_end=True)

    fig.savefig(out, bbox_inches="tight", pad_inches=0.04)
    plt.close(fig)


def fig2_architecture(out: Path) -> None:
    fig, ax = plt.subplots(figsize=(7.0, 2.35))
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 4.2)
    ax.axis("off")

    ax.add_patch(
        FancyBboxPatch((0.15, 2.55), 13.7, 1.05, boxstyle="square,pad=0", facecolor="#f0f0f0", edgecolor="none", zorder=0)
    )
    ax.add_patch(
        FancyBboxPatch((0.15, 1.35), 13.7, 0.95, boxstyle="square,pad=0", facecolor="#e8e8e8", edgecolor="none", zorder=0)
    )
    ax.text(0.25, 3.45, "Main RF branch", fontsize=7, fontweight="bold", va="center")
    ax.text(0.25, 2.25, "OOB branch", fontsize=7, fontweight="bold", va="center")

    y_main = 3.05
    main_specs = [
        (1.0, ["IQ/FFT/AP"]),
        (2.5, ["CNN stem"]),
        (4.0, ["Main tokens", r"$T_m$"]),
        (5.5, ["Pos./chirp"]),
        (7.2, ["Fusion"]),
        (8.7, ["RF-HSTU"]),
        (10.2, ["Window", "logits"]),
        (11.7, ["Mean $K$", "windows"]),
        (13.0, ["File-level", r"$\hat{y}$"]),
    ]
    main_boxes = []
    for x, lab in main_specs:
        fc = "#dddddd" if lab == ["Fusion"] else "#ffffff"
        ec = "#555555" if lab == ["Fusion"] else "#333333"
        lw = 1.2 if lab == ["Fusion"] else 1.0
        main_boxes.append(_box(ax, x, y_main, 1.05, 0.72, lab, fc=fc, ec=ec, lw=lw, fontsize=7))

    for i in range(len(main_boxes) - 1):
        a, b = main_boxes[i], main_boxes[i + 1]
        _seg(ax, a["right"] + 0.03, y_main, b["left"] - 0.03, y_main, arrow_end=True)

    y_oob = 1.85
    oob_specs = [(1.0, ["OOB spectrum"]), (2.8, ["OOB tokenizer"]), (4.6, ["OOB tokens", r"$T_o$"])]
    oob_boxes = [_box(ax, x, y_oob, 1.15, 0.68, lab, fontsize=7) for x, lab in oob_specs]
    for i in range(len(oob_boxes) - 1):
        a, b = oob_boxes[i], oob_boxes[i + 1]
        _seg(ax, a["right"] + 0.03, y_oob, b["left"] - 0.03, y_oob, arrow_end=True)

    fusion = main_boxes[4]
    tm, to = main_boxes[2], oob_boxes[2]
    fx = fusion["cx"]

    ax.text(tm["cx"], 2.58, r"$Q$", fontsize=7, ha="center", color="#222222")
    _ortho(ax, [(tm["cx"], tm["bottom"] - 0.02), (tm["cx"], 2.48), (fx, 2.48), (fx, fusion["top"] + 0.02)])

    ax.text(6.0, 2.12, r"$K,V$", fontsize=7, ha="center", color="#222222")
    _ortho(ax, [(to["right"] + 0.02, y_oob), (6.0, y_oob), (6.0, 2.48), (fx, 2.48)])

    ax.add_patch(
        FancyBboxPatch(
            (5.6, 0.15),
            4.8,
            0.95,
            boxstyle="round,pad=0.03,rounding_size=0.06",
            linewidth=1.0,
            edgecolor="#666666",
            facecolor="#fafafa",
            linestyle="--",
            zorder=2,
        )
    )
    ax.plot([fx, fx], [fusion["bottom"] - 0.02, 1.12], color="#666666", lw=0.8, linestyle="--", zorder=1)
    ax.text(
        8.0,
        0.62,
        "OOB-guided fusion\n"
        r"$Q = T_m,\; K,V = T_o$" + "\n"
        r"$A = \mathrm{MHA}(Q,K,V)$" + "\n"
        r"$T_f = \mathrm{LN}(T_m + G \odot AW_o)$",
        ha="center",
        va="center",
        fontsize=7,
        linespacing=1.2,
        zorder=3,
    )
    ax.text(13.0, 0.25, r"$P{=}32,\; D{=}64$", ha="right", fontsize=6.5, color="#555555")

    fig.savefig(out, bbox_inches="tight", pad_inches=0.05)
    plt.close(fig)


def main() -> None:
    plt.rcParams["font.family"] = "DejaVu Sans"
    plt.rcParams["pdf.fonttype"] = 42
    plt.rcParams["ps.fonttype"] = 42
    fig1_scenario(ROOT / "fig1_application_scenario.pdf")
    fig2_architecture(ROOT / "fig2_architecture.pdf")
    print("Wrote:", ROOT / "fig1_application_scenario.pdf")
    print("Wrote:", ROOT / "fig2_architecture.pdf")


if __name__ == "__main__":
    main()
