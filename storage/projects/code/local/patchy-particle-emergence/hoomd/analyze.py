"""Project a HOOMD trajectory into thermodynamic and structural observables."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any

import matplotlib.pyplot as plt
import numpy as np

from config import load_config
from metrics import structural_observables


THERMODYNAMIC_FIELDS = (
    "kinetic_temperature",
    "kinetic_energy",
    "translational_kinetic_energy",
    "rotational_kinetic_energy",
    "potential_energy",
    "pressure",
)


def first_passage_time(
    rows: list[dict[str, float]],
    field: str,
    threshold: float,
) -> float | None:
    """Return the first sampled time at or above ``threshold``."""

    return next(
        (row["time"] for row in rows if row[field] >= threshold),
        None,
    )


def first_joint_passage_time(
    rows: list[dict[str, float]],
    thresholds: dict[str, float],
) -> float | None:
    """Return the first time every declared threshold is reached together."""

    return next(
        (
            row["time"]
            for row in rows
            if all(row[field] >= threshold for field, threshold in thresholds.items())
        ),
        None,
    )


def scalar_log(frame: Any, quantity: str) -> float:
    log = frame.log or {}
    matches = [name for name in log if name.endswith(f"/{quantity}")]
    if not matches:
        return float("nan")
    value = np.asarray(log[matches[0]], dtype=float).squeeze()
    return float(value)


def analyze(
    config_path: Path,
    trajectory_path: Path,
    output_directory: Path,
) -> dict[str, object]:
    try:
        import gsd.hoomd
    except ImportError as error:
        raise SystemExit(
            "The GSD package is missing. Run this analysis through Pixi: "
            "`pixi run analyze`."
        ) from error

    config = load_config(config_path)
    output_directory.mkdir(parents=True, exist_ok=True)
    rows: list[dict[str, float]] = []
    with gsd.hoomd.open(name=str(trajectory_path), mode="r") as trajectory:
        for frame in trajectory:
            row = {
                "timestep": float(frame.configuration.step),
                "time": float(frame.configuration.step * config.dt),
                **{
                    field: scalar_log(frame, field)
                    for field in THERMODYNAMIC_FIELDS
                },
                **structural_observables(
                    np.asarray(frame.particles.position, dtype=float),
                    np.asarray(frame.particles.orientation, dtype=float),
                    frame.particles.typeid,
                    frame.particles.types,
                    config,
                ),
            }
            rows.append(row)
    if not rows:
        raise RuntimeError(f"trajectory contains no frames: {trajectory_path}")

    csv_path = output_directory / "observables.csv"
    with csv_path.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)

    times = np.asarray([row["time"] for row in rows])
    figure, axes = plt.subplots(2, 2, figsize=(11, 7), constrained_layout=True)
    axes[0, 0].plot(times, [row["potential_energy"] for row in rows], label="U")
    axes[0, 0].plot(times, [row["kinetic_energy"] for row in rows], label="K")
    axes[0, 0].set(title="Energy", xlabel="time", ylabel="reduced energy")
    axes[0, 0].legend()
    axes[0, 1].plot(times, [row["kinetic_temperature"] for row in rows])
    axes[0, 1].axhline(config.temperature, color="black", linestyle="--", alpha=0.5)
    axes[0, 1].set(title="Kinetic temperature", xlabel="time", ylabel="kT")
    axes[1, 0].plot(
        times,
        [row["largest_component_fraction"] for row in rows],
    )
    axes[1, 0].set(
        title="Largest patch-contact component",
        xlabel="time",
        ylabel="fraction of particles",
        ylim=(0.0, 1.05),
    )
    axes[1, 1].plot(times, [row["mean_degree"] for row in rows], label="degree")
    axes[1, 1].plot(
        times,
        [row["orientational_order"] for row in rows],
        label=f"|psi_{config.orientational_order}|",
    )
    axes[1, 1].plot(
        times,
        [row["local_bond_order_6"] for row in rows],
        label="local bond order |psi_6|",
    )
    axes[1, 1].plot(
        times,
        [row["coordination_3_fraction"] for row in rows],
        label="degree 3 fraction",
    )
    axes[1, 1].set(title="Structural order", xlabel="time")
    axes[1, 1].legend()
    if config.magnetic_field is not None and config.magnetic_start_step > 0:
        activation_time = config.magnetic_start_step * config.dt
        for axis in axes.flat:
            axis.axvline(
                activation_time,
                color="#674ea7",
                linestyle=":",
                alpha=0.75,
            )
    figure.suptitle("Cohesian emergence — HOOMD benchmark")
    figure_path = output_directory / "observables.png"
    figure.savefig(figure_path, dpi=180)
    plt.close(figure)

    peak = max(rows, key=lambda row: row["largest_component_fraction"])
    summary = {
        "frames": len(rows),
        "final_time": rows[-1]["time"],
        "final_largest_component_fraction": rows[-1][
            "largest_component_fraction"
        ],
        "maximum_largest_component_fraction": max(
            row["largest_component_fraction"] for row in rows
        ),
        "peak_component_time": peak["time"],
        "time_to_component_0_25": first_passage_time(
            rows, "largest_component_fraction", 0.25
        ),
        "time_to_component_0_50": first_passage_time(
            rows, "largest_component_fraction", 0.50
        ),
        "final_mean_degree": rows[-1]["mean_degree"],
        "final_orientational_order": rows[-1]["orientational_order"],
        "final_local_bond_order_6": rows[-1]["local_bond_order_6"],
        "final_global_bond_order_6": rows[-1]["global_bond_order_6"],
        "time_to_connected_global_order_0_50": first_joint_passage_time(
            rows,
            {
                "largest_component_fraction": 0.50,
                "global_bond_order_6": 0.50,
            },
        ),
        "final_coordination_3_fraction": rows[-1]["coordination_3_fraction"],
        "final_coordination_6_fraction": rows[-1]["coordination_6_fraction"],
        "final_local_bond_order_6": rows[-1]["local_bond_order_6"],
        "final_global_bond_order_6": rows[-1]["global_bond_order_6"],
        "final_coordination_3_fraction": rows[-1]["coordination_3_fraction"],
        "observables": str(csv_path.resolve()),
        "figure": str(figure_path.resolve()),
    }
    if config.magnetic_field is not None:
        activation_time = config.magnetic_start_step * config.dt
        activation_row = min(
            rows,
            key=lambda row: abs(row["time"] - activation_time),
        )
        summary.update(
            {
                "field_activation_time": activation_time,
                "global_bond_order_6_at_field_activation": activation_row[
                    "global_bond_order_6"
                ],
                "field_global_bond_order_6_change": (
                    rows[-1]["global_bond_order_6"]
                    - activation_row["global_bond_order_6"]
                ),
                "coordination_3_at_field_activation": activation_row[
                    "coordination_3_fraction"
                ],
                "field_coordination_3_change": (
                    rows[-1]["coordination_3_fraction"]
                    - activation_row["coordination_3_fraction"]
                ),
            }
        )
    (output_directory / "summary.json").write_text(
        json.dumps(summary, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(summary, indent=2))
    return summary


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, default=Path("experiment.toml"))
    parser.add_argument(
        "--trajectory",
        type=Path,
        default=Path("outputs/trajectory.gsd"),
    )
    parser.add_argument("--output", type=Path, default=Path("outputs"))
    return parser.parse_args()


if __name__ == "__main__":
    arguments = parse_args()
    analyze(arguments.config, arguments.trajectory, arguments.output)
