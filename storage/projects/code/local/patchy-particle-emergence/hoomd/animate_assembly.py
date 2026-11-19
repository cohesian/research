"""Render the synchronized isotropic, directional, and field experiment."""

from __future__ import annotations

import argparse
from pathlib import Path

from matplotlib import animation
from matplotlib.collections import LineCollection
import matplotlib.pyplot as plt
import numpy as np

from animate import (
    BACKGROUND,
    GRID,
    MUTED,
    PANEL,
    TEXT,
    edge_segments,
    load_frames,
    patch_segments,
)
from config import ExperimentConfig, load_config


CONDITIONS = (
    ("isotropic", "ISOTROPIC", "compact local packing", "#ef8354"),
    ("three-patch", "DIRECTIONAL", "three patches · open network", "#a78bfa"),
    (
        "three-patch--delayed-field",
        "DIRECTIONAL + FIELD",
        "same rules · external torque after t=180",
        "#5eead4",
    ),
)


def sequence(frame_count: int, field_frame: int, fps: int) -> list[int]:
    sampled = list(range(0, frame_count, 2))
    if sampled[-1] != frame_count - 1:
        sampled.append(frame_count - 1)
    result = [0] * round(0.6 * fps)
    for index in sampled:
        result.append(index)
        if abs(index - field_frame) <= 1:
            result.extend([index] * round(0.65 * fps))
    result.extend([frame_count - 1] * round(0.9 * fps))
    return result


def render_comparison(
    root: Path,
    output: Path,
    *,
    fps: int,
    dpi: int,
) -> None:
    configs: list[ExperimentConfig] = []
    trajectories = []
    for slug, _, _, _ in CONDITIONS:
        run = root / slug / "seed-0041"
        config = load_config(run / "resolved.toml")
        configs.append(config)
        trajectories.append(load_frames(run / "trajectory.gsd", config))
    frame_count = min(len(frames) for frames in trajectories)
    field_config = configs[-1]
    field_time = field_config.magnetic_start_step * field_config.dt
    field_frame = min(
        range(frame_count),
        key=lambda index: abs(trajectories[-1][index].time - field_time),
    )
    frames_to_render = sequence(frame_count, field_frame, fps)

    figure, axes = plt.subplots(1, 3, figsize=(19.2, 10.8), facecolor=BACKGROUND)
    figure.subplots_adjust(left=0.025, right=0.985, top=0.79, bottom=0.15, wspace=0.08)
    figure.suptitle(
        "One initial state. Three interaction rules.",
        color=TEXT,
        fontsize=25,
        fontweight="bold",
        y=0.965,
    )
    subtitle = figure.text(
        0.5,
        0.905,
        "No particle receives a target shape.",
        color=MUTED,
        fontsize=14,
        ha="center",
    )
    time_text = figure.text(
        0.5,
        0.055,
        "",
        color=TEXT,
        fontsize=14,
        ha="center",
        family="monospace",
    )

    artists = []
    for axis, config, frames, (_, title, description, accent) in zip(
        axes,
        configs,
        trajectories,
        CONDITIONS,
        strict=True,
    ):
        first = frames[0]
        axis.set_facecolor(PANEL)
        bound = config.wall_half_extent
        axis.set(
            xlim=(-bound, bound),
            ylim=(-bound, bound),
            aspect="equal",
            xticks=(),
            yticks=(),
        )
        for spine in axis.spines.values():
            spine.set_color(GRID)
            spine.set_linewidth(1.2)
        axis.set_title(title, color=accent, fontsize=14, fontweight="bold", pad=29)
        axis.text(
            0.5,
            1.035,
            description,
            transform=axis.transAxes,
            color=MUTED,
            fontsize=10.5,
            ha="center",
        )
        ordinary_edges = LineCollection(
            [],
            colors="#59677a",
            linewidths=0.65,
            alpha=0.45,
            zorder=1,
        )
        component_edges = LineCollection(
            [],
            colors=accent,
            linewidths=1.7,
            alpha=0.88,
            zorder=2,
        )
        axis.add_collection(ordinary_edges)
        axis.add_collection(component_edges)
        particles = axis.scatter(
            first.positions[:, 0],
            first.positions[:, 1],
            s=90,
            facecolors="#f28c64",
            edgecolors="#111820",
            linewidths=0.55,
            zorder=3,
        )
        patches = LineCollection(
            [],
            colors="#111820",
            linewidths=0.9,
            zorder=4,
        )
        axis.add_collection(patches)
        metric = axis.text(
            0.03,
            0.035,
            "",
            transform=axis.transAxes,
            color=TEXT,
            fontsize=10,
            family="monospace",
            bbox={"facecolor": BACKGROUND, "alpha": 0.72, "edgecolor": "none", "pad": 4},
            zorder=5,
        )
        field_label = axis.text(
            0.5,
            0.955,
            "B  →",
            transform=axis.transAxes,
            color="#5eead4",
            fontsize=15,
            fontweight="bold",
            ha="center",
            va="top",
            visible=False,
            zorder=6,
        )
        artists.append(
            {
                "particles": particles,
                "patches": patches,
                "ordinary_edges": ordinary_edges,
                "component_edges": component_edges,
                "metric": metric,
                "field_label": field_label,
            }
        )

    def update(render_index: int):
        index = frames_to_render[render_index]
        time = trajectories[0][index].time
        time_text.set_text(f"simulation time  t = {time:6.1f}")
        field_active = time >= field_time
        subtitle.set_text(
            "An external torque is now competing with local bonds."
            if field_active
            else "No particle receives a target shape."
        )
        changed = [time_text, subtitle]
        for condition_index, (config, frames, group) in enumerate(
            zip(configs, trajectories, artists, strict=True)
        ):
            frame = frames[index]
            group["particles"].set_offsets(frame.positions[:, :2])
            group["ordinary_edges"].set_segments(
                edge_segments(frame, highlighted=False)
            )
            group["component_edges"].set_segments(
                edge_segments(frame, highlighted=True)
            )
            group["patches"].set_segments(
                [] if config.interaction_mode == "isotropic" else patch_segments(frame, config)
            )
            group["metric"].set_text(
                f"largest={frame.largest_fraction:0.2f}\n"
                f"mean degree={frame.mean_degree:0.2f}\n"
                f"global ψ₆={frame.global_bond_order_6:0.2f}"
            )
            group["field_label"].set_visible(condition_index == 2 and field_active)
            changed.extend(group.values())
        return changed

    output.parent.mkdir(parents=True, exist_ok=True)
    movie = animation.FuncAnimation(
        figure,
        update,
        frames=len(frames_to_render),
        interval=1000 / fps,
        blit=False,
    )
    writer = animation.FFMpegWriter(
        fps=fps,
        codec="libx264",
        bitrate=5000,
        extra_args=["-pix_fmt", "yuv420p", "-movflags", "+faststart"],
    )
    movie.save(output, writer=writer, dpi=dpi)
    plt.close(figure)
    print(f"assembly comparison: {output}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path("outputs/assembly"))
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("outputs/assembly/assembly-comparison.mp4"),
    )
    parser.add_argument("--fps", type=int, default=30)
    parser.add_argument("--dpi", type=int, default=100)
    return parser.parse_args()


if __name__ == "__main__":
    arguments = parse_args()
    render_comparison(
        arguments.root,
        arguments.output,
        fps=arguments.fps,
        dpi=arguments.dpi,
    )
