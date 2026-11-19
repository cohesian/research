# 3. Dynamics, temperature, and the delayed field

## Force is not displacement

Force changes momentum. For translation,

$$
m\frac{d\mathbf v_i}{dt}=\mathbf F_i,
\qquad
\frac{d\mathbf x_i}{dt}=\mathbf v_i.
$$

This is why multiplying force directly by the timestep is not a complete motion
rule. Over a small interval, force first changes velocity; the evolving
velocity changes position.

Rotation has the analogous structure:

$$
I\frac{d\boldsymbol\omega_i}{dt}=\boldsymbol\tau_i,
\qquad
\frac{d\theta_i}{dt}=\omega_i
$$

in the planar intuition.

## Langevin dynamics

Our particles are coupled to a thermal bath. Translational dynamics is
conceptually

$$
m\frac{d\mathbf v_i}{dt}
=
\mathbf F_i^{\mathrm C}
-\gamma\mathbf v_i
+\mathbf F_i^{\mathrm R}(t),
$$

where:

- $\mathbf F_i^{\mathrm C}$ is conservative force from pair interactions and
  walls;
- $-\gamma\mathbf v_i$ is drag; and
- $\mathbf F_i^{\mathrm R}$ is a random thermal force.

The random term has zero mean. Its variance is tied to temperature, drag, and
timestep so that noise and dissipation form one thermostat rather than two
unrelated effects. Rotation receives corresponding drag and random torque.

This means the system is open: it exchanges energy with a reservoir. The sum
of kinetic and potential energy need not remain constant.

## The numerical clock

The configured timestep is

$$
\Delta t=0.002.
$$

HOOMD advances the complete state synchronously:

$$
X^{n+1}=\Phi_{\Delta t}(X^n).
$$

The full assembly run uses $180000$ integration steps, so its simulated
duration is

$$
t_{\mathrm{final}}
=180000(0.002)=360.
$$

The shared clock does not give particles global knowledge. It prevents the
arbitrary order of a Python loop from allowing one particle to observe another
particle's future state during the same update.

## Why the simulation moves even without a target

At each step, four effects compose:

1. thermal noise perturbs velocity and orientation;
2. nearby potentials generate forces and torques;
3. drag dissipates motion; and
4. walls confine the population.

Noise lets the system explore configurations. Attractive wells make some
encounters persist. Repulsion prevents collapse. Directional envelopes select
which orientations bind strongly. A large-scale network can therefore form
without any direct network-building rule.

## External magnetic alignment

One comparison adds a body-fixed moment $\boldsymbol\mu_i$ and a uniform field
$\mathbf B$. The potential is

$$
U_i^{\mathrm{field}}
=
-\boldsymbol\mu_i\cdot\mathbf B.
$$

Its minimum occurs when the moment aligns with the field. The corresponding
torque is

$$
\boldsymbol\tau_i^{\mathrm{field}}
=
\boldsymbol\mu_i\times\mathbf B.
$$

For the experiment,

$$
\boldsymbol\mu_i=(1,0,0)
\quad\text{in the local particle frame},
$$

and, after activation,

$$
\mathbf B=(3,0,0)
\quad\text{in the world frame}.
$$

As the particle rotates, its local moment rotates in world space. The field
therefore tries to give every particle a common orientation.

## What the field does not do

The implemented field is spatially uniform. Its energy depends on orientation,
not position. Therefore it supplies torque but does not pull centers to the
right, attract particles to one another, or generate a field gradient.

This distinction prevents a common visual misunderstanding: alignment in the
rightmost panel is not caused by particles being dragged along the arrow.

## Why activation is delayed

The field is zero during the first half:

$$
0\le t<180.
$$

At step $90000$, corresponding to $t=180$, it changes to $\mathbf B=(3,0,0)$.
The experiment therefore has two phases:

$$
\text{local assembly}
\quad\longrightarrow\quad
\text{local assembly + global orienting torque}.
$$

This asks a more interesting question than applying the field from the start:
can a global bias reorganize a structure whose local bonds already have a
history?

The field can rotate a weakly constrained particle easily. Rotating a particle
inside a bonded network can raise patch energy or break contacts. The observed
response is a competition between field alignment, bond strength, thermal
noise, drag, and geometry.

## Dimensionless interpretation

The values $B=3$, $kT=0.18$, and $A=5$ are expressed in the model's reduced
units. We can compare them internally, but we cannot call the field “three
tesla” or the time “360 seconds” without a separate calibration to a physical
system.

## Check your understanding

1. Why does force change velocity rather than position directly?
2. Why is total mechanical energy not conserved under Langevin dynamics?
3. How can a uniform field change orientation without changing center
   position directly?
4. What question does delayed activation let us ask?

