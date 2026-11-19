"""Configuration and shared geometry for the HOOMD emergence benchmark."""

from __future__ import annotations

from dataclasses import dataclass
import math
from pathlib import Path
import tomllib


@dataclass(frozen=True)
class ExperimentConfig:
    seed: int
    dt: float
    steps: int
    write_period: int
    temperature: float
    linear_drag: float
    angular_drag: float
    box_length: float
    wall_half_extent: float
    particle_radius: float
    particle_mass: float
    minimum_initial_distance: float
    initialization_method: str
    candidate_pool: int
    population: dict[str, int]
    repulsion_energy: float
    interaction_mode: str
    patch_attraction: float
    patch_range: float
    patch_cutoff: float
    patch_half_angle: float
    patch_steepness: float
    pair_attraction: dict[str, float]
    contact_cutoff: float
    minimum_patch_alignment: float
    orientational_order: int
    magnetic_field: tuple[float, float, float] | None
    magnetic_moment: tuple[float, float, float] | None
    magnetic_start_step: int

    @property
    def particle_count(self) -> int:
        return sum(self.population.values())

    @property
    def particle_types(self) -> tuple[str, ...]:
        return tuple(self.population)

    @property
    def particle_diameter(self) -> float:
        return 2.0 * self.particle_radius

    @property
    def moment_of_inertia(self) -> float:
        """Moment of inertia of a uniform disk around its local z-axis."""

        return 0.5 * self.particle_mass * self.particle_radius**2

    def patch_count(self, particle_type: str) -> int:
        if not particle_type.startswith("P"):
            raise ValueError(f"particle type must use P<count>: {particle_type!r}")
        try:
            count = int(particle_type[1:])
        except ValueError as error:
            raise ValueError(
                f"particle type must use P<count>: {particle_type!r}"
            ) from error
        if count < 1:
            raise ValueError("particle types need at least one patch")
        return count

    def directors(self, particle_type: str) -> tuple[tuple[float, float, float], ...]:
        """Return evenly spaced patch directors in the local xy-plane."""

        count = self.patch_count(particle_type)
        return tuple(
            (
                math.cos(2.0 * math.pi * index / count),
                math.sin(2.0 * math.pi * index / count),
                0.0,
            )
            for index in range(count)
        )

    def attraction_for(self, left: str, right: str) -> float:
        """Return the symmetric attraction magnitude for a type pair."""

        direct = f"{left}-{right}"
        reverse = f"{right}-{left}"
        if direct in self.pair_attraction:
            return self.pair_attraction[direct]
        if reverse in self.pair_attraction:
            return self.pair_attraction[reverse]
        return self.patch_attraction

    def validate(self) -> None:
        positive = {
            "dt": self.dt,
            "steps": self.steps,
            "write_period": self.write_period,
            "box_length": self.box_length,
            "wall_half_extent": self.wall_half_extent,
            "particle_radius": self.particle_radius,
            "particle_mass": self.particle_mass,
            "minimum_initial_distance": self.minimum_initial_distance,
            "repulsion_energy": self.repulsion_energy,
            "patch_attraction": self.patch_attraction,
            "patch_range": self.patch_range,
            "patch_cutoff": self.patch_cutoff,
            "patch_half_angle": self.patch_half_angle,
            "patch_steepness": self.patch_steepness,
            "contact_cutoff": self.contact_cutoff,
            "orientational_order": self.orientational_order,
            "candidate_pool": self.candidate_pool,
        }
        for name, value in positive.items():
            if value <= 0:
                raise ValueError(f"{name} must be positive")
        if self.seed < 1:
            raise ValueError("seed must be positive")
        if self.temperature < 0:
            raise ValueError("temperature cannot be negative")
        if self.linear_drag < 0 or self.angular_drag < 0:
            raise ValueError("drag cannot be negative")
        if not self.population or any(count < 1 for count in self.population.values()):
            raise ValueError("population counts must be positive")
        for particle_type in self.population:
            self.patch_count(particle_type)
        if self.initialization_method not in {"uniform_rejection", "blue_noise"}:
            raise ValueError(
                "initialization method must be uniform_rejection or blue_noise"
            )
        if self.interaction_mode not in {"isotropic", "patchy"}:
            raise ValueError("interaction mode must be isotropic or patchy")
        known_types = set(self.particle_types)
        for pair, attraction in self.pair_attraction.items():
            parts = pair.split("-")
            if len(parts) != 2 or any(part not in known_types for part in parts):
                raise ValueError(f"unknown particle pair in attraction matrix: {pair}")
            if attraction < 0:
                raise ValueError("pair attraction cannot be negative")
        if self.wall_half_extent >= self.box_length / 2.0:
            raise ValueError("walls must remain inside the periodic simulation box")
        if self.minimum_initial_distance < self.particle_diameter:
            raise ValueError("initial particles must not overlap")
        if self.patch_cutoff <= self.particle_diameter:
            raise ValueError("patch cutoff must extend beyond particle contact")
        if not 0.0 < self.patch_half_angle < math.pi:
            raise ValueError("patch_half_angle must lie in (0, pi)")
        if not 0.0 <= self.minimum_patch_alignment <= 1.0:
            raise ValueError("minimum_patch_alignment must lie in [0, 1]")
        has_field = self.magnetic_field is not None
        has_moment = self.magnetic_moment is not None
        if has_field != has_moment:
            raise ValueError("magnetic field and moment must be declared together")
        if self.magnetic_start_step < 0 or self.magnetic_start_step > self.steps:
            raise ValueError("magnetic_start_step must lie within the simulation")
        if has_field and self.interaction_mode != "patchy":
            raise ValueError("the magnetic alignment experiment requires patchy particles")


def load_config(path: str | Path) -> ExperimentConfig:
    source = Path(path)
    with source.open("rb") as stream:
        raw = tomllib.load(stream)

    simulation = raw["simulation"]
    geometry = raw["geometry"]
    interaction = raw["interaction"]
    analysis = raw["analysis"]
    initialization = raw.get("initialization", {})
    field = raw.get("field", {})
    field_enabled = bool(field.get("enabled", False))
    config = ExperimentConfig(
        seed=int(simulation["seed"]),
        dt=float(simulation["dt"]),
        steps=int(simulation["steps"]),
        write_period=int(simulation["write_period"]),
        temperature=float(simulation["temperature"]),
        linear_drag=float(simulation["linear_drag"]),
        angular_drag=float(simulation["angular_drag"]),
        box_length=float(geometry["box_length"]),
        wall_half_extent=float(geometry["wall_half_extent"]),
        particle_radius=float(geometry["particle_radius"]),
        particle_mass=float(geometry["particle_mass"]),
        minimum_initial_distance=float(geometry["minimum_initial_distance"]),
        initialization_method=str(
            initialization.get("method", "uniform_rejection")
        ),
        candidate_pool=int(initialization.get("candidate_pool", 64)),
        population={name: int(count) for name, count in raw["population"].items()},
        repulsion_energy=float(interaction["repulsion_energy"]),
        interaction_mode=str(interaction.get("mode", "patchy")),
        patch_attraction=float(interaction["patch_attraction"]),
        patch_range=float(interaction["patch_range"]),
        patch_cutoff=float(interaction["patch_cutoff"]),
        patch_half_angle=float(interaction["patch_half_angle"]),
        patch_steepness=float(interaction["patch_steepness"]),
        pair_attraction={
            str(pair): float(value)
            for pair, value in interaction.get("pair_attraction", {}).items()
        },
        contact_cutoff=float(analysis["contact_cutoff"]),
        minimum_patch_alignment=float(analysis["minimum_patch_alignment"]),
        orientational_order=int(analysis["orientational_order"]),
        magnetic_field=(
            tuple(float(value) for value in field["vector"])
            if field_enabled
            else None
        ),
        magnetic_moment=(
            tuple(float(value) for value in field["moment"])
            if field_enabled
            else None
        ),
        magnetic_start_step=int(field.get("start_step", 0)),
    )
    config.validate()
    return config


def write_config(config: ExperimentConfig, path: str | Path) -> None:
    """Write one fully resolved experiment configuration as TOML."""

    config.validate()
    lines = [
        "[simulation]",
        f"seed = {config.seed}",
        f"dt = {config.dt!r}",
        f"steps = {config.steps}",
        f"write_period = {config.write_period}",
        f"temperature = {config.temperature!r}",
        f"linear_drag = {config.linear_drag!r}",
        f"angular_drag = {config.angular_drag!r}",
        "",
        "[geometry]",
        f"box_length = {config.box_length!r}",
        f"wall_half_extent = {config.wall_half_extent!r}",
        f"particle_radius = {config.particle_radius!r}",
        f"particle_mass = {config.particle_mass!r}",
        f"minimum_initial_distance = {config.minimum_initial_distance!r}",
        "",
        "[initialization]",
        f'method = "{config.initialization_method}"',
        f"candidate_pool = {config.candidate_pool}",
        "",
        "[population]",
    ]
    lines.extend(f"{name} = {count}" for name, count in config.population.items())
    lines.extend(
        [
            "",
            "[interaction]",
            f"repulsion_energy = {config.repulsion_energy!r}",
            f'mode = "{config.interaction_mode}"',
            f"patch_attraction = {config.patch_attraction!r}",
            f"patch_range = {config.patch_range!r}",
            f"patch_cutoff = {config.patch_cutoff!r}",
            f"patch_half_angle = {config.patch_half_angle!r}",
            f"patch_steepness = {config.patch_steepness!r}",
        ]
    )
    if config.pair_attraction:
        lines.extend(["", "[interaction.pair_attraction]"])
        lines.extend(
            f"{pair} = {value!r}"
            for pair, value in config.pair_attraction.items()
        )
    lines.extend(["", "[field]"])
    lines.append(
        f"enabled = {'true' if config.magnetic_field is not None else 'false'}"
    )
    if config.magnetic_field is not None and config.magnetic_moment is not None:
        field = ", ".join(repr(value) for value in config.magnetic_field)
        moment = ", ".join(repr(value) for value in config.magnetic_moment)
        lines.extend(
            [
                f"vector = [{field}]",
                f"moment = [{moment}]",
                f"start_step = {config.magnetic_start_step}",
            ]
        )
    lines.extend(
        [
            "",
            "[analysis]",
            f"contact_cutoff = {config.contact_cutoff!r}",
            f"minimum_patch_alignment = {config.minimum_patch_alignment!r}",
            f"orientational_order = {config.orientational_order}",
            "",
        ]
    )
    Path(path).write_text("\n".join(lines), encoding="utf-8")
