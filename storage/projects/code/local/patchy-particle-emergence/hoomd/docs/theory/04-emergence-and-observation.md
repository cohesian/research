# 4. From microscopic motion to observable emergence

## Three descriptions of the same trajectory

The simulation contains exact particle states, but “network,” “cluster,” and
“order” are not primitive HOOMD objects in this experiment. They appear when an
observer projects the same state at a different scale.

The three levels are

$$
X(t)
\xrightarrow{\Pi_G}
G_t
\xrightarrow{\Pi_M}
M(t).
$$

- $X(t)$ is the microscopic state: positions, velocities, orientations, and
  momenta.
- $G_t=(V,E_t)$ is a mesoscopic contact graph.
- $M(t)$ is a vector of macroscopic measurements.

The projection discards information. Many microscopic arrangements can produce
the same graph, and many different graphs can produce the same summary value.

## Constructing the contact graph

Every particle becomes a vertex:

$$
V=\{1,2,\ldots,N\}.
$$

For the isotropic control, an analysis edge exists when the center distance is
below the declared contact cutoff $r_a=1.45$:

$$
(i,j)\in E_t
\iff
r_{ij}(t)\le r_a.
$$

For patchy particles, proximity is necessary but not sufficient. Let
$\mathcal D_i(t)$ be the rotated patch directors of $i$. Define the best
forward alignments

$$
a_i=
\max_{\mathbf d\in\mathcal D_i(t)}
\mathbf d\cdot\widehat{\mathbf r}_{ij},
$$

$$
a_j=
\max_{\mathbf d\in\mathcal D_j(t)}
\mathbf d\cdot(-\widehat{\mathbf r}_{ij}).
$$

Then

$$
(i,j)\in E_t
\iff
r_{ij}\le1.45
\quad\land\quad
a_i\ge0.95
\quad\land\quad
a_j\ge0.95.
$$

The dot product is a cosine because all directors are normalized. A threshold
of $0.95$ demands close angular alignment.

The edge definition is an analysis choice. It does not create or remove forces
in HOOMD.

## Connected-component growth

Let $C_{\max}(G_t)$ be the largest connected component. We normalize its size:

$$
S_{\max}(t)
=
\frac{|C_{\max}(G_t)|}{N}.
$$

$S_{\max}=0.8$ means that 80% of particles belong to one connected structure.
It says nothing by itself about whether that structure is compact, branched,
hexagonal, or globally aligned.

## Mean degree and coordination

The degree $k_i$ counts contacts incident to particle $i$. By the handshake
lemma,

$$
\bar{k}(t)
=
\frac{1}{N}\sum_i k_i
=
\frac{2|E_t|}{N}.
$$

We also measure the fractions

$$
P_q(t)=
\frac{1}{N}
\left|
\{i:k_i(t)=q\}
\right|
$$

for $q\in\{2,3,6\}$. Degree three is informative for an open three-patch
network; degree six is informative for dense triangular packing.

## Sixfold bond-orientational order

For each contact $(i,j)$, let $\theta_{ij}$ be the angle of
$\mathbf x_j-\mathbf x_i$. At node $i$ define

$$
\psi_6(i)
=
\frac{1}{k_i}
\sum_{j\in\mathcal N_i}
e^{6\mathrm{i}\theta_{ij}}.
$$

Multiplication by six makes directions separated by $60^\circ$ equivalent,
because

$$
e^{6\mathrm{i}(\theta+\pi/3)}
=e^{6\mathrm{i}\theta}e^{2\pi\mathrm{i}}
=e^{6\mathrm{i}\theta}.
$$

The local order parameter is

$$
\Psi_6^{\mathrm{local}}
=
\frac{1}{|V'|}
\sum_{i\in V'}|\psi_6(i)|,
$$

where $V'$ contains nodes with at least two contacts. It asks whether each
local neighborhood has sixfold-compatible angles.

The global order parameter is

$$
\Psi_6^{\mathrm{global}}
=
\left|
\frac{1}{|V'|}
\sum_{i\in V'}\psi_6(i)
\right|.
$$

This average occurs before taking the magnitude. Differently rotated domains
can cancel. A sample may therefore have high local order and low global order.

## First-passage time

To ask when a condition first becomes true, define

$$
\tau_a
=
\inf\{t:S_{\max}(t)\ge a\}.
$$

For example, $\tau_{0.5}$ is the first sampled time at which at least half of
the particles belong to one component. This is more informative than inspecting
only the final frame, because clusters can form and later break.

## Operational emergence

For this experiment, a structure is called emergent when:

1. no particle receives the final structure as a target;
2. it is produced by repeated finite-range interactions;
3. a declared projection makes it observable; and
4. changing a local rule changes the distribution of the observation.

This definition is intentionally modest. The macroscopic pattern follows from
the microscopic model; it does not violate it. “Emergent” means that a useful,
simpler description becomes visible at another scale.

## Observation is not control

The analyzer reads saved frames after HOOMD has evolved them. Computing
$S_{\max}$ or $\Psi_6$ does not feed those values back into the particles. The
observer would become a controller only if a future update depended on an
aggregate measurement.

## Why one beautiful trajectory is not a law

With random seed $r$, write an observable as $M^{(r)}(t)$. An ensemble mean is

$$
\overline{M}_R(t)
=
\frac{1}{R}
\sum_{r=1}^{R}M^{(r)}(t).
$$

We also need the spread across seeds. The present assembly comparison uses only
one seed, so it is a visual pilot and a hypothesis generator. Claims about
assembly time, system-size scaling, or field effectiveness require multiple
independent runs and uncertainty estimates.

## Current pilot interpretation

The single-seed result is consistent with three different macroscopic regimes:

- isotropic attraction produces a compact, higher-degree aggregate;
- three patches produce an open, mostly degree-three network; and
- delayed torque can increase global orientation while changing existing
  contacts.

The 192-particle run remains less globally coherent than the 48-particle run
within the same simulated duration. That is a question for an ensemble study,
not yet evidence that assembly time obeys a particular scaling law.

## Check your understanding

1. Why is the contact graph not part of the force law?
2. How can local $\Psi_6$ be high while global $\Psi_6$ is low?
3. Why must connectedness, degree, and angular order be interpreted together?
4. What additional evidence would turn the current visual hypothesis into a
   statistical claim?

