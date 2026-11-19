"""Run the isotropic, directional, field, and size assembly experiment."""

from __future__ import annotations

import argparse
from dataclasses import asdict, replace
import hashlib
import json
import math
from pathlib import Path
import tomllib

from analyze import analyze
from config import ExperimentConfig, load_config, write_config
from simulate import run


def resolved_config(
    base: ExperimentConfig,
    specification: dict[str, object],
    *,
    seed: int,
    reference_count: int,
    quick: bool,
) -> ExperimentConfig:
    count = int(specification["particle_count"])
    scale = math.sqrt(count / reference_count)
    wall_half_extent = base.wall_half_extent * scale
    field_strength = float(specification.get("field_strength", 0.0))
    steps = min(base.steps, 12000) if quick else base.steps
    start_fraction = float(specification.get("field_start_fraction", 0.0))
    return replace(
        base,
        seed=seed,
        steps=steps,
        write_period=min(base.write_period, 200) if quick else base.write_period,
        population={"P3": count},
        wall_half_extent=wall_half_extent,
        box_length=2.0 * wall_half_extent + 2.0,
        interaction_mode=str(specification["interaction"]),
        pair_attraction={},
        magnetic_field=(field_strength, 0.0, 0.0) if field_strength else None,
        magnetic_moment=(1.0, 0.0, 0.0) if field_strength else None,
        magnetic_start_step=round(steps * start_fraction) if field_strength else 0,
    )


def run_assembly_study(
    study_path: Path,
    output: Path,
    *,
    quick: bool = False,
    force: bool = False,
    reanalyze: bool = False,
    selected_condition: str | None = None,
) -> None:
    with study_path.open("rb") as stream:
        raw = tomllib.load(stream)
    study = raw["study"]
    base_path = study_path.parent / str(study["base_config"])
    base = load_config(base_path)
    seeds = [int(seed) for seed in study["seeds"]]
    reference_count = int(study["reference_count"])
    output.mkdir(parents=True, exist_ok=True)

    manifest_runs: list[dict[str, object]] = []
    for specification in raw["run"]:
        condition = str(specification["name"])
        if selected_condition is not None and condition != selected_condition:
            continue
        for seed in seeds:
            config = resolved_config(
                base,
                specification,
                seed=seed,
                reference_count=reference_count,
                quick=quick,
            )
            run_directory = output / condition / f"seed-{seed:04d}"
            run_directory.mkdir(parents=True, exist_ok=True)
            config_path = run_directory / "resolved.toml"
            write_config(config, config_path)
            checksum = hashlib.sha256(config_path.read_bytes()).hexdigest()
            record_path = run_directory / "assembly-run.json"
            reusable = False
            if record_path.exists() and not force:
                previous = json.loads(record_path.read_text(encoding="utf-8"))
                reusable = (
                    previous.get("configuration_sha256") == checksum
                    and (run_directory / "trajectory.gsd").exists()
                    and (run_directory / "observables.csv").exists()
                    and (run_directory / "summary.json").exists()
                )
            print(f"[{condition}] seed={seed} {'reuse' if reusable else 'run'}")
            if not reusable:
                run(config_path, run_directory)
                summary = analyze(
                    config_path,
                    run_directory / "trajectory.gsd",
                    run_directory,
                )
                record = {
                    "condition": condition,
                    "configuration_sha256": checksum,
                    "parameters": asdict(config),
                    "summary": summary,
                }
                record_path.write_text(
                    json.dumps(record, indent=2) + "\n",
                    encoding="utf-8",
                )
            else:
                record = json.loads(record_path.read_text(encoding="utf-8"))
                if reanalyze:
                    record["summary"] = analyze(
                        config_path,
                        run_directory / "trajectory.gsd",
                        run_directory,
                    )
                    record_path.write_text(
                        json.dumps(record, indent=2) + "\n",
                        encoding="utf-8",
                    )
            manifest_runs.append(
                {
                    "condition": condition,
                    "seed": seed,
                    "configuration_sha256": checksum,
                    "directory": str(run_directory.resolve()),
                    "summary": record["summary"],
                }
            )

    manifest = {
        "question": (
            "How do interaction symmetry, system size, and a delayed aligning "
            "field change assembly geometry and time?"
        ),
        "study": str(study_path.resolve()),
        "base_config": str(base_path.resolve()),
        "quick": quick,
        "runs": manifest_runs,
    }
    (output / "assembly-study.json").write_text(
        json.dumps(manifest, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps({"runs": len(manifest_runs), "output": str(output)}, indent=2))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--study", type=Path, default=Path("assembly.toml"))
    parser.add_argument("--output", type=Path, default=Path("outputs/assembly"))
    parser.add_argument("--quick", action="store_true")
    parser.add_argument("--force", action="store_true")
    parser.add_argument("--reanalyze", action="store_true")
    parser.add_argument("--condition")
    return parser.parse_args()


if __name__ == "__main__":
    arguments = parse_args()
    run_assembly_study(
        arguments.study,
        arguments.output,
        quick=arguments.quick,
        force=arguments.force,
        reanalyze=arguments.reanalyze,
        selected_condition=arguments.condition,
    )
