# 2. Local interactions: exclusion, attraction, force, and torque

## Potential energy is a landscape

A potential $U$ assigns an energy to every configuration. The particles do not
read that energy as an instruction. Force and torque arise from how rapidly the
energy changes when position or orientation changes:

$$
\mathbf F_i=-\nabla_{\mathbf x_i}U,
\qquad
\boldsymbol\tau_i=-\frac{\partial U}{\partial q_i}.
$$

Loosely: the dynamics tends to move downhill in potential energy, while
inertia, drag, thermal noise, and competing interactions prevent this from
being an instantaneous optimization.

The conservative energy in this experiment is

$$
U(X)=
\sum_{i<j}
\left[
U_{\mathrm{core}}(r_{ij})
+U_{\mathrm{attr}}(r_{ij},q_i,q_j)
\right]
+\sum_i U_{\mathrm{wall}}(\mathbf x_i)
+\sum_i U_{\mathrm{field}}(q_i).
$$

Not every term is active in every condition. The field, for example, is used
only in one delayed-field trajectory.

## Excluded volume: why centers do not collapse

Attraction alone would favor placing centers arbitrarily close. The model
therefore adds a steep repulsive core: a Lennard-Jones potential truncated at
its minimum and shifted to zero. This is commonly called the WCA form:

$$
U_{\mathrm{core}}(r)=
\begin{cases}
4\epsilon_r
\left[
\left(\dfrac{\sigma}{r}\right)^{12}
-\left(\dfrac{\sigma}{r}\right)^6
\right]+epsilon_r,
&r<2^{1/6}\sigma,\\[8pt]
0,
&r\ge 2^{1/6}\sigma.
\end{cases}
$$

Here $\epsilon_r=1$ and $\sigma=1$. Close to overlap, the $r^{-12}$ term rises
very quickly. At and beyond the cutoff, the core contributes nothing.

This is a soft numerical exclusion, not the quantum Pauli exclusion principle.

## The radial attractive well

Both comparison systems use a Gaussian attraction before the cutoff:

$$
U_{\mathrm G}(r)
=
-A\exp\left[
-\frac12\left(\frac{r}{\sigma_p}\right)^2
\right],
$$

with attraction magnitude $A=5$ and radial scale $\sigma_p=1$. It is truncated
at $r_c=1.75$ and shifted so that the stored potential reaches zero smoothly in
value at the cutoff:

$$
U_{\mathrm G}^{\mathrm{shift}}(r)=
\begin{cases}
U_{\mathrm G}(r)-U_{\mathrm G}(r_c),&r<r_c,\\
0,&r\ge r_c.
\end{cases}
$$

The attractive Gaussian and the repulsive core act together. Their sum creates
a preferred separation: moving closer lowers attractive energy until the
repulsive core becomes dominant.

This is the “elastic band” intuition you noticed. It is useful but imperfect:
there is no literal band and no Hookean rest length. The effective pull is the
slope $-dU/dr$ of the combined potential.

## Isotropic attraction

In the isotropic control,

$$
U_{ij}^{\mathrm{attr}}
=
U_{\mathrm G}^{\mathrm{shift}}(r_{ij}).
$$

Only center distance matters. Rotating either particle leaves the pair energy
unchanged, so this term generates translational force but no orientation-based
torque.

Because every direction is equally available, a particle can attract many
nearby neighbors. In two dimensions, dense triangular packing is therefore a
natural low-energy arrangement. Its coordination number can approach six.

## Directional attraction

For patchy particles, each pair of local directors is evaluated. Let
$\theta_{a,i}$ be the angle between patch $a$ on particle $i$ and
$\widehat{\mathbf r}_{ij}$. Let $\theta_{b,j}$ be the angle between patch $b$ on
particle $j$ and $-\widehat{\mathbf r}_{ij}$.

The angular gate used by HOOMD is based on

$$
h(\theta)=
\left[
1+\exp\bigl(-\omega(\cos\theta-\cos\alpha)\bigr)
\right]^{-1},
$$

normalized as

$$
f(\theta;\alpha,\omega)
=
\frac{h(\theta)-h(\pi)}{h(0)-h(\pi)}.
$$

The assembly experiment uses

$$
\alpha=0.22\ \mathrm{rad}\approx12.6^\circ,
\qquad
\omega=60.
$$

$\alpha$ controls angular width and $\omega$ controls how sharply the envelope
switches. The pair energy is a sum over patch pairs:

$$
U_{ij}^{\mathrm{patch}}
=
\sum_{a\in\mathcal D_i}
\sum_{b\in\mathcal D_j}
f(\theta_{a,i})
f(\theta_{b,j})
U_{\mathrm G}^{\mathrm{shift}}(r_{ij}).
$$

A term is strong only when the centers are close **and** both patches face one
another.

## Why patch alignment produces torque

Suppose the centers are within attractive range but the patch directions are
slightly misaligned. A small rotation can increase both angular envelope
values and lower the energy. The orientation derivative is therefore nonzero,
which produces torque.

Attraction can simultaneously:

- translate the centers because the energy depends on $r_{ij}$; and
- rotate the bodies because the energy depends on $q_i$ and $q_j$.

There is no two-stage rule saying “rotate first, translate second.” Both
contributions participate in the same time integration.

## Locality

Every pair potential vanishes beyond its declared cutoff. For particle $i$,
define

$$
\mathcal N_i(t)=
\left\{
j\ne i:r_{ij}(t)<r_c
\right\}.
$$

Then its pair force can be written

$$
\mathbf F_i^{\mathrm{pair}}(t)
=
\sum_{j\in\mathcal N_i(t)}\mathbf F_{ij}(t).
$$

HOOMD uses a cell neighbor list to discover these nearby pairs efficiently. The
global data structure is an implementation index; the physical rule remains
finite-range.

## Check your understanding

1. Why do we need both repulsion and attraction?
2. Which derivative produces translation and which produces rotation?
3. Why does the isotropic control favor dense packing while three patches
   favor lower coordination?

