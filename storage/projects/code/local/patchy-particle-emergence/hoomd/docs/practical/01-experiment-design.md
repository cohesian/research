# 1. From a question to five controlled trajectories

This section translates the theoretical question into reproducible experiment
configuration. Read the four theory chapters first.

## The two configuration layers

The experiment separates common parameters from deliberate variations:

- [`assembly-base.toml`](../../assembly-base.toml) declares the state that all
  runs inherit;
- [`assembly.toml`](../../assembly.toml) declares only the variables being
  compared.

That separation makes the control logic visible. If five full configuration
files were copied by hand, an accidental difference in temperature or timestep
could be mistaken for an effect of interaction symmetry.

## Common state

The base file declares:

```toml
[simulation]
seed = 41
dt = 0.002
steps = 180000
temperature = 0.18
linear_drag = 1.0
angular_drag = 0.5

[population]
P3 = 96

[interaction]
mode = "patchy"
repulsion_energy = 1.0
patch_attraction = 5.0
patch_range = 1.0
patch_cutoff = 1.75
patch_half_angle = 0.22
patch_steepness = 60.0
```

The name `P3` is interpreted by [`ExperimentConfig.patch_count()`](../../config.py):
the integer after `P` is the number of evenly spaced directors. Thus no list of
three manually entered angles is hidden elsewhere.

## The five conditions

The study file declares:

| Name | $N$ | Attraction | Field | Purpose |
|---|---:|---|---:|---|
| `isotropic` | 96 | radial | 0 | dense-packing control |
| `three-patch` | 96 | directional | 0 | open-network comparison |
| `three-patch--delayed-field` | 96 | directional | 3 | intervention at half-time |
| `three-patch--small` | 48 | directional | 0 | finite-size comparison |
| `three-patch--large` | 192 | directional | 0 | finite-size comparison |

The first three isolate interaction symmetry and field response at fixed size.
The last three compare size at approximately fixed density.

## Resolving a run

[`resolved_config()`](../../assembly_study.py) starts from the immutable base
configuration and replaces only the declared experimental variables.

For count $N$, the wall half-extent is scaled as

$$
L_N=L_{96}\sqrt{N/96}.
$$

Because area grows approximately as $L_N^2$, this makes area proportional to
$N$ and keeps density approximately fixed.

For the field condition, the study declares a start fraction of $0.5$. The
resolver converts that relative choice to an exact step:

$$
n_{\mathrm{field}}
=
\operatorname{round}(0.5\times180000)
=90000.
$$

## Why every run writes `resolved.toml`

The study settings and base settings are convenient for humans, but neither
alone is the complete state of one run. Before simulation, the runner writes a
fully resolved configuration beside the trajectory:

```text
outputs/assembly/<condition>/seed-0041/resolved.toml
```

It also computes the SHA-256 of that file. A trajectory can be reused only when
the stored checksum matches the newly resolved configuration. This prevents a
silent mistake where old dynamics are analyzed as if they came from new
parameters.

The checksum verifies configuration identity. It does not prove that the
scientific model is correct.

## Initialization

Every condition uses the same seed and the same best-candidate blue-noise
sampler. For each new point:

1. draw a pool of random candidate positions;
2. measure each candidate's distance to the existing population;
3. select the candidate whose nearest neighbor is farthest away; and
4. accept it only if it respects the minimum initial distance.

This yields an isotropic but visibly spaced initial state. It avoids accidental
dense pockets without placing particles on a lattice.

Because the same seed is used, the three 96-particle conditions begin from the
same positions and orientations. The comparison then changes the interaction,
not the random initial geometry.

## Quick and full modes

The smoke mode limits each condition to 12000 steps and writes more frequently:

```bash
pixi run assembly-smoke
```

Its role is engineering validation: can the environment, configuration,
simulation, and analyzer complete? It is too short for scientific conclusions.

The full study is:

```bash
pixi run assembly-study
```

## Questions to ask before changing a parameter

Before editing the TOML, state the expected contrast:

- Does a wider patch angle reduce geometric selectivity?
- Does stronger thermal noise break incomplete networks out of traps or merely
  destroy bonds?
- Does an earlier field prevent independent domains from forming?
- Does the time to reach $S_{\max}\ge0.5$ grow with $N$ at fixed density?

Then modify one axis while holding the others fixed.

