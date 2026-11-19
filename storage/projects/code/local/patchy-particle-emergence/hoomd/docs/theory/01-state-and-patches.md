# 1. State, geometry, and patches

## What kind of model is this?

This is a classical, two-dimensional, coarse-grained particle model. It is not
a literal model of atoms, electrons, quantum fields, or a measured chemical
substance. A particle represents one local unit whose movement and orientation
can interact with nearby units.

The quantities are written in **reduced units**. We set convenient reference
scales for length, mass, and energy instead of claiming that one simulated unit
equals one meter, kilogram, or joule. This lets us study structure without
pretending that the present calibration describes a particular material.

## The complete microscopic state

For $N$ particles, the system state at time $t$ is

$$
X(t)=\bigl(s_1(t),s_2(t),\ldots,s_N(t)\bigr).
$$

The dynamic state of particle $i$ is

$$
s_i(t)=
\bigl(
\mathbf{x}_i(t),
\mathbf{v}_i(t),
q_i(t),
\mathbf{L}_i(t)
\bigr),
$$

where:

- $\mathbf{x}_i=(x_i,y_i)$ is the center position;
- $\mathbf{v}_i$ is translational velocity;
- $q_i$ is orientation, stored by HOOMD as a quaternion; and
- $\mathbf{L}_i$ is angular momentum.

Motion is restricted to the $xy$ plane, so the orientation can be understood
pedagogically as one angle $\theta_i$ around the $z$ axis. The quaternion is a
numerically robust representation of that same orientation.

Every particle in the assembly experiment has

$$
R=0.5,
\qquad
\sigma=2R=1,
\qquad
m=1.
$$

If we treat it as a uniform disk, its moment of inertia around $z$ is

$$
I=\frac{1}{2}mR^2=0.125.
$$

Mass resists translational acceleration; moment of inertia resists angular
acceleration.

## A patch is a local direction

A patch is not a second particle and it is not a permanent bond. It is a
body-fixed direction along which attraction can be strong.

For a particle with $p$ evenly spaced patches, the local directors are

$$
\mathbf{d}_k^{(p)}=
\left(
\cos\frac{2\pi k}{p},
\sin\frac{2\pi k}{p},
0
\right),
\qquad
k=0,\ldots,p-1.
$$

The current experiment uses only type `P3`, so $p=3$:

$$
\mathbf d_0=(1,0,0),
$$

$$
\mathbf d_1=
\left(-\frac12,\frac{\sqrt3}{2},0\right),
$$

$$
\mathbf d_2=
\left(-\frac12,-\frac{\sqrt3}{2},0\right).
$$

Their angular separation is $2\pi/3=120^\circ$.

## Local frame and world frame

The three vectors above live in the particle's local frame. When particle $i$
rotates by $\theta_i$, the world-space director becomes

$$
\mathbf d_{i,k}(t)
=
R\bigl(\theta_i(t)\bigr)\mathbf d_k,
$$

with

$$
R(\theta)=
\begin{bmatrix}
\cos\theta & -\sin\theta\\
\sin\theta & \cos\theta
\end{bmatrix}.
$$

The particle therefore carries local geometry while moving through a shared
world. This distinction is what lets orientation matter.

## The geometry between two particles

For particles $i$ and $j$, define the displacement

$$
\mathbf r_{ij}=\mathbf x_j-\mathbf x_i,
$$

its distance

$$
r_{ij}=\lVert\mathbf r_{ij}\rVert,
$$

and the unit direction

$$
\widehat{\mathbf r}_{ij}
=
\frac{\mathbf r_{ij}}{r_{ij}}.
$$

$r_{ij}$ answers “how far apart?” while
$\widehat{\mathbf r}_{ij}$ answers “in which direction from $i$ to $j$?”. The
isotropic model uses mainly the distance. The patchy model also compares the
direction with the rotated patch directors.

## What the particle does not know

No particle stores a hexagon, a target neighbor list, the largest cluster, or
the final picture. Its future state is determined by its current state, nearby
interactions, the walls, and the thermal bath.

The possible hexagonal geometry enters only indirectly: three preferred
directions separated by $120^\circ$ are locally compatible with an open
three-valent network. Compatibility is not a command. Defects, chains, cycles,
separate domains, and incomplete structures remain possible.

## Check your understanding

Before continuing, you should be able to answer:

1. Why does rotating a particle change its attraction in the patchy model but
   not in the isotropic control?
2. Why is a patch a direction rather than a small independent particle?
3. Why can three patches permit hexagonal cells without encoding a hexagon?

