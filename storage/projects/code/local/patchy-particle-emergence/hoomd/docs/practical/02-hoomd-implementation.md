# 2. Translating the model into HOOMD

This chapter maps each mathematical object to the implementation in
[`simulate.py`](../../simulate.py). The snippets are intentionally short; use
the links to read the executable source.

## 1. Load and validate one complete state

[`load_config()`](../../config.py) converts TOML values to an immutable
`ExperimentConfig`. [`validate()`](../../config.py) rejects invalid states such
as negative timesteps, overlapping initial particles, a patch cutoff inside
the particle diameter, or a magnetic field attached to the isotropic control.

This is where configuration text becomes typed program state.

## 2. Build the initial snapshot

[`build_snapshot()`](../../simulate.py) creates a HOOMD `Snapshot` containing:

- the 2D simulation box;
- particle count and type IDs;
- positions from the blue-noise sampler;
- random planar orientations encoded as quaternions;
- mass, diameter, and moment of inertia.

For a planar angle $\theta$, the stored quaternion is

$$
q=
\left(
\cos\frac{\theta}{2},
0,
0,
\sin\frac{\theta}{2}
\right).
$$

## 3. Discover local neighbors

The force configuration begins with

```python
neighbor_list = hoomd.md.nlist.Cell(buffer=0.4)
```

A cell list partitions space so that the engine does not test every pair when
the potentials have finite cutoffs. It accelerates local interaction lookup; it
does not change the potential.

## 4. Add the repulsive core

The code creates a shifted Lennard-Jones pair potential and cuts it at
$2^{1/6}\sigma$:

```python
repulsive_cutoff = 2.0 ** (1.0 / 6.0) * config.particle_diameter
repulsion = hoomd.md.pair.LJ(
    nlist=neighbor_list,
    default_r_cut=repulsive_cutoff,
    mode="shift",
)
```

With this cutoff, only the repulsive part remains. Pair parameters assign the
energy scale and diameter.

## 5. Select isotropic or directional attraction

The controlled branch is explicit:

```python
if config.interaction_mode == "patchy":
    attraction = hoomd.md.pair.aniso.PatchyGaussian(...)
else:
    attraction = hoomd.md.pair.Gaussian(...)
```

Both use the same radial attraction magnitude, range, and cutoff. The patchy
version additionally receives the angular envelope and the body-frame
directors:

```python
attraction.directors[particle_type] = list(
    config.directors(particle_type)
)
```

The important experimental difference is therefore orientation dependence,
not a completely unrelated radial well.

## 6. Add confinement

Four `hoomd.wall.Plane` objects point inward from $\pm L$ on the $x$ and $y$
axes. A repulsive wall potential keeps particles inside that square.

HOOMD still requires a simulation box around the walls. The physical region of
interest is bounded by the walls, not by periodic wrapping.

## 7. Prepare the delayed field

If a field is configured, the simulation creates
`hoomd.md.external.field.Magnetic`. For delayed activation, its initial vector
is exactly zero:

```python
initial_field = (
    config.magnetic_field
    if config.magnetic_start_step == 0
    else (0.0, 0.0, 0.0)
)
```

The field object is already part of the force list, but it contributes no
torque during the first phase.

## 8. Compose the integrator

HOOMD receives a Langevin method and all force objects:

```python
langevin = hoomd.md.methods.Langevin(
    filter=hoomd.filter.All(),
    kT=config.temperature,
    default_gamma=config.linear_drag,
    default_gamma_r=(
        config.angular_drag,
        config.angular_drag,
        config.angular_drag,
    ),
)

simulation.operations.integrator = hoomd.md.Integrator(
    dt=config.dt,
    integrate_rotational_dof=True,
    methods=[langevin],
    forces=forces,
)
```

`integrate_rotational_dof=True` matters: without rotational integration, the
directional potential could not reorient particle bodies correctly.

## 9. Run in two phases

For the delayed-field condition, [`run()`](../../simulate.py) advances to the
activation step, mutates the field vector, then advances the remaining steps:

```python
simulation.run(config.magnetic_start_step)
for particle_type in config.particle_types:
    magnetic.params[particle_type] = {
        "B": config.magnetic_field,
        "mu": config.magnetic_moment,
    }
simulation.run(config.steps - config.magnetic_start_step)
```

The other trajectories execute one uninterrupted `simulation.run(...)`.

## 10. Store dynamics, not screenshots

A `hoomd.write.GSD` writer periodically stores particle properties, momentum,
and logged thermodynamic scalars in `trajectory.gsd`. The renderer and analyzer
read that trajectory later.

This separation lets us:

- change a plot without rerunning physics;
- change video pacing without rerunning physics;
- inspect the exact state behind a surprising frame; and
- compare multiple analysis projections of one trajectory.

## A productive way to read the source

Do not read `simulate.py` top to bottom on the first pass. Follow this path:

```text
run
 ├─ load_config
 ├─ build_snapshot
 │   ├─ random_positions
 │   └─ orientations
 ├─ configure_forces
 └─ simulation.run
```

For every function, ask which object from the theory chapters it implements.

