# HOOMD emergence project

This portable Pixi/Python project is the executable companion to the
patchy-particle Emergence Lecture. It delegates classical time integration,
anisotropic patch forces, thermal noise, barriers, and thermodynamic quantities
to HOOMD-blue while keeping the full experiment declaration and analysis in the
repository.

## First experiment

The model places three particle types in a two-dimensional walled region:

| Type | Fixed patches | Count |
|---|---:|---:|
| `P1` | 1 | 32 |
| `P2` | 2 | 48 |
| `P3` | 3 | 16 |

All particles have the same mass and disk radius. Their initial positions use
isotropic best-candidate blue noise: each new position is selected from a
random candidate pool by maximizing its distance to the existing population.
This suppresses accidental dense pockets without imprinting a lattice.

A shifted Lennard-Jones core
provides excluded-volume repulsion, while `PatchyGaussian` supplies a smooth,
orientation-dependent attraction. Langevin dynamics adds declared thermal and
drag terms. The seed makes the randomized initial condition reproducible.

The default selective interaction matrix gives each type a simple chemical
role without prescribing a final geometry:

- `P2-P2` supports chain growth;
- `P2-P3` is strongest, allowing sparse `P3` particles to become branch points;
- `P1` prefers `P2` and `P3`, making it an end cap; and
- `P1-P1` and `P3-P3` are weak, reducing cap dimers and dense brancher clumps.

[`baseline.toml`](baseline.toml) preserves the earlier uniformly attractive,
ordinary-random control configuration.

The experiment writes:

~~~text
outputs/
├── trajectory.gsd
├── run.json
├── observables.csv
├── observables.png
├── snapshots.png
├── snapshots/
└── summary.json
~~~

The structural contact graph is an analysis projection, not a persistent bond
topology inside HOOMD. An edge is present when two centers are sufficiently
near and at least one patch on each particle faces the other.

## Controlled ensemble

[`study.toml`](study.toml) defines a controlled $2\times2$ study:

| Axis | Conditions |
|---|---|
| initialization | random rejection, best-candidate blue noise |
| type affinity | uniform, selective pair matrix |

The four conditions share particle counts, geometry, temperature, timestep,
barriers, run length, and contact-graph definition. Each condition runs three
seeds. Every run stores a fully resolved configuration plus its SHA-256
checksum, so the notebook analyzes declared simulation state rather than
hidden cell-local parameters.

~~~bash
pixi run study
pixi run notebook-build
pixi run notebook-execute
pixi run notebook-publish
pixi run video
~~~

The study writes ignored trajectories and tables under `outputs/study/` and a
tracked, executed Research resource under the Emergence TLE path. The
generated report compares individual seeds and condition mean $\pm$ standard
deviation, energy evolution, and median-seed peak structures.

`video` renders the representative blue-noise/selective trajectory into the
local `media` store as
[`emergence.mp4`](../../../../media/local/patchy-particle-emergence/emergence.mp4).
It uses all 400 saved simulation states, briefly holds the initial,
strongest-assembly, and final states, and displays the live contact graph and
macroscopic observables. It does not rerun HOOMD or call a voice service.

## Hexagonal assembly experiment

[`assembly.toml`](assembly.toml) asks a narrower visual question: how do
interaction symmetry, system size, and an aligning field change assembly
geometry and assembly time? It declares five controlled trajectories:

For a from-first-principles walkthrough, start with the
[`learning guide`](docs/README.md). It separates the mathematical model from
the HOOMD implementation and includes a small notebook for inspecting the
results.

| Condition | Intended comparison |
|---|---|
| isotropic | compact aggregation and six-neighbor local packing |
| three-patch | open, degree-three networks with possible hexagonal cells |
| three-patch + delayed field | competition between existing bonds and global alignment |
| small three-patch | finite-size reference |
| large three-patch | cost of building one coherent domain at larger scale |

The three-patch particles carry evenly spaced directors at $0$, $2\pi/3$, and
$4\pi/3$. No hexagon is encoded as a target. Hexagonal cells are possible
because local valence and angle constraints admit them, but defects, separate
domains, and incomplete assembly are valid outcomes.

The external magnetic field is activated halfway through its trajectory. It
applies torque to a local dipole; it does not pull particles in the field
direction. A weak field may fail to rotate an already bonded network, while a
strong field may align particles by breaking or frustrating some contacts.
That competition is part of the experiment rather than a rendering effect.

The analysis now separates:

- connected-component growth;
- mean degree and degree-two, degree-three, and degree-six fractions;
- local sixfold bond order, which can remain high in differently oriented
  domains; and
- global sixfold bond order, which requires those domains to agree.

Run the inexpensive calibration before the full trajectories:

~~~bash
pixi run assembly-smoke
pixi run assembly-study
pixi run assembly-video
~~~

`assembly-video` renders a synchronized 1920×1080 comparison directly from
the three 96-particle trajectories. It contains no narration and is intended
as the review master for a later Studio explanation.

The first release uses one seed to produce and inspect the visual hypothesis.
Any claim about scaling or field effectiveness requires a later seeded
ensemble and uncertainty estimates.

## Time and translation

HOOMD's molecular-dynamics integrator advances a synchronized timestep `dt`.
Conceptually, force changes velocity through acceleration and the evolving
velocity translates the particle:

$$
m\frac{d\mathbf v}{dt}=\mathbf F,
\qquad
\frac{d\mathbf x}{dt}=\mathbf v.
$$

Langevin dynamics additionally introduces drag and a random force consistent
with the configured thermal energy. Therefore `dt` is not a multiplier that
turns force directly into displacement. It controls the numerical resolution
of the coupled position, velocity, orientation, and angular-momentum update.

The local-interaction law and the temporal scheduler are distinct: finite-range
forces use local neighborhoods, while the MD integrator advances the system on
one shared clock.

## Run

HOOMD publishes supported macOS and Linux binaries through conda-forge. This
project therefore owns its complete Pixi environment.

~~~bash
pixi run test
pixi run smoke
pixi run experiment
pixi run render
pixi run baseline
pixi run study
pixi run notebook-build
pixi run notebook-execute
pixi run notebook-publish
pixi run video
~~~

`smoke` runs only 1,000 integration steps and writes to `outputs/smoke/`. Use
it to validate a new machine or configuration before starting the full run.
`render` can be repeated against the existing full trajectory without running
the dynamics again.

The snapshot montage includes temporal landmarks plus the frame with the
largest inferred patch-contact component. Each panel displays particle type,
patch directions, and instantaneous contact edges. Individual full-resolution
frames are also written under `outputs/snapshots/` for closer inspection or a
later animation.

To modify the population, timestep, temperature, barriers, or patch potential,
edit [`experiment.toml`](experiment.toml). Generated trajectories and figures
remain ignored local outputs.

## Validated baseline

The preserved seed-41 baseline configuration has been executed with HOOMD 7.1.2 on the
macOS ARM64 CPU build. Across the final 100 saved frames, the mean kinetic
temperature was `0.3503` for a configured target of `0.35`. The largest
patch-contact component reached `0.21875` of the population transiently and
averaged `0.08323` over those final frames.

This is a dispersed, fluctuating baseline—not yet evidence of a stable
macroscopic phase. That result is useful: it establishes a reproducible control
before varying temperature, attraction, density, and patch composition.

The default blue-noise/selective configuration has also been executed. Its
largest component reached `0.17708` of the population—17 of 96 particles—and
formed a visibly branched, partially cyclic structure. It remained transient,
ending at `0.04167`. Compared with the denser control, it sacrifices some peak
cluster size for a cleaner initial condition and more legible morphology.

## Controlled-study result

Across this exploratory three-seed ensemble, uniform attraction produced a
mean peak connected fraction near `0.106` for both initialization methods.
Selective affinity increased it to `0.160 ± 0.063` after random initialization
and `0.153 ± 0.006` after blue-noise initialization. The latter was therefore
more reproducible in this sample, while the former contained the highest
single-run peak and the greatest seed variance.

This supports a bounded observation: changing the local type-affinity matrix
changed the measured finite structures. It does not establish a stable bulk
phase or universal law.

## Scientific next step

Run seeded ensembles rather than interpreting a single trajectory. The first
parameter sweep should vary one axis at a time—temperature, density, patch
attraction, or particle composition—and report uncertainty and finite-size
effects for the structural observables.

Dynamic patch creation and field-mediated interactions are outside this fixed-
patch baseline. Adding either to HOOMD requires a declared custom action or
force and should follow validation of the current model.

Rigid bodies are intentionally absent. A HOOMD rigid body fixes a
predeclared collection of constituent particles into one geometry. That is
appropriate later if a *building block itself* has multiple physical beads,
but applying it to emergent clusters would assume the structure that this
experiment is meant to discover.
