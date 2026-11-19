# Learning the assembly experiment

This directory explains the experiment in two layers. Start with `theory/`.
It develops the model in mathematical language without requiring Python or
HOOMD knowledge. Continue with `practical/` only after the objects in the
equations feel familiar.

## Part I — theory

1. [`01-state-and-patches.md`](theory/01-state-and-patches.md) — what a particle
   is in this model and how three body-fixed patches are represented.
2. [`02-local-interactions.md`](theory/02-local-interactions.md) — exclusion,
   isotropic attraction, directional attraction, force, and torque.
3. [`03-dynamics-and-field.md`](theory/03-dynamics-and-field.md) — how force
   becomes motion through Langevin dynamics and what the delayed field changes.
4. [`04-emergence-and-observation.md`](theory/04-emergence-and-observation.md) —
   how microscopic states are projected into a contact graph and macroscopic
   measurements.

## Part II — practical

1. [`01-experiment-design.md`](practical/01-experiment-design.md) — the five
   controlled trajectories and how their configurations are generated.
2. [`02-hoomd-implementation.md`](practical/02-hoomd-implementation.md) — the
   exact correspondence between each theoretical term and the HOOMD code.
3. [`03-analysis-and-video.md`](practical/03-analysis-and-video.md) — how a GSD
   trajectory becomes a graph, a table, a report, and the comparison video.
4. [`assembly-lab.ipynb`](practical/assembly-lab.ipynb) — a small notebook for
   inspecting the existing results without rerunning the full simulation.

The shortest useful path is:

```text
state → interactions → dynamics → graph projection → experiment → code → data
```

The canonical Research Lecture under `storage/documents/` remains the formal
publication. These files are the learning companion for the executable
project: they deliberately explain intermediate steps that production code
normally leaves implicit.

