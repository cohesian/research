# From Functions to Architecture — Master Video Design

## Editorial thesis

This is not a catalogue of software patterns. It follows one system as its
internal structure grows while its usable boundaries remain composable.

> Scale does not remove local rules; it composes them.

The continuous example is one HTTP request travelling through a real service:

```text
client -> gateway -> authorization -> handler -> repository -> database
```

The same information packet, labelled $\rho$, remains visible throughout the
film. Pipelines, wrappers, composites, functors, and the final architecture are
introduced only when the evolving system needs their particular geometry.

## Audience promise

By the end, a viewer should be able to answer four questions:

1. How do two compatible functions become one usable operation?
2. Why are pipelines, wrappers, and composites different shapes of
   composition?
3. What extra laws make a translation a functor rather than an arbitrary map?
4. How do the same local rules reappear in an architecture graph?

No prior category theory or design-pattern vocabulary is assumed. Equations
name structures after the motion has made them visible.

## Runtime

Target master: **6:40–7:00**, 16:9, 1080p60 after acceptance. The V3 silent
layout review renders at **5:33** and the V3 gTTS review at **6:54**.

| Part | Purpose | Time |
|---|---|---:|
| 0 | Cold open and fixed visual grammar | 0:00–0:44 |
| 1 | Compatible functions, contraction, and reuse | 0:44–1:55 |
| 2 | Typed request pipeline | 1:55–2:55 |
| 3 | Wrapper as a hidden control-flow graph | 2:55–3:50 |
| 4 | Recursive query plan | 3:50–4:52 |
| 5 | Logical plan to runtime plan | 4:52–5:40 |
| 6 | Architecture: the local shapes coexist | 5:40–6:32 |
| 7 | Close: one move repeated across scales | 6:32–6:54 |

Natural speech is expected to occupy roughly 4:45. The remaining time is
reserved for visual comprehension, equation holds, and transitions.

## Cohesian visual contract

Use `loci_plugins.cohesian` and the existing Studio V2 contract.

| Role | Representation |
|---|---|
| Canvas | Cohesian cream `#FFF8ED` |
| Primary operation | compact component card with input/output ports |
| Inactive structure | shell/muted stroke |
| Active boundary or invariant | gold |
| Primary text | ink |
| Secondary type or edge label | muted |
| Information packet $\rho$ | small gold request capsule with a short fading trail |
| Input/output contract | small port ring carrying a type label |
| Data-flow edge | directed deep-orange edge |
| Containment edge | thin shell edge, no arrow |
| Functor correspondence | dashed gold bridge between diagrams |
| Node anchor | one small spark in the upper-left interior; no decorative header rail |
| Information packet | symbolic signal spark with core, halo, and restrained trail |

Node size is vocabulary, not a response to label length: an atomic operation
is smallest, a module is one step larger, a named composite is larger again,
and a subsystem is the largest reusable boundary. Symbols such as $f$, $P$,
$W[f]$, $Q$, and $v_S$ preserve identity while prose labels explain the role.
Selected components gain a soft aura; repeated decorative bars are excluded.

The palette does semantic work. Do not introduce extra colors merely to make
the frame busier.

### Motion invariant

The outer input/output ports remain in place whenever internal detail expands
or contracts. This is the film's main visual statement: internal structure can
change scale while an external contract remains usable.

### Reusable motion vocabulary

- `Graph` and graph ticker: nodes, typed edges, path activation, architecture
  projections.
- `Stage`: ports, labels, packet $\rho$, wrapper rings, and free composition.
- `TransformMatchingTex`: equation regrouping and preservation laws.
- `TracedPath`: the packet's movement through a valid path.
- `ReplacementTransform`: contracting a subsystem into one component and
  expanding it again.
- Subtle camera push/pull: only to reveal a new scale. No ambient movement
  while equations are being read.
- Cohesian seed transition: opening punctuation and final closure, not between
  every conceptual beat.

## Master storyboard

### Part 0 — One architecture, one local move

**Time:** 0:00–0:22

**Frame:** Begin on a dense but legible architecture graph. Several edge
families are visible. A gold request capsule traces the concrete data path from
client to database. Before isolating its first compatible joint, introduce the
fixed size hierarchy and the symbols $f$, $P$, $W[f]$, $Q$, and $v_S$:

$$
f:A\to B,
\qquad
g:B\to C.
$$

**Motion:** A gold packet $\rho$ crosses $f$ and pauses at the shared $B$
port. The title appears only after the zoom has found this local joint:

```text
FROM FUNCTIONS TO ARCHITECTURE
The geometry of composition
```

**Narrative function:** Promise that the apparently large subject will be
derived from a small operation rather than explained as a list of terms.

---

### Part 1 — Composition hides one compatible joint

**Time:** 0:22–1:02

**Frame:** Keep $A$, $B$, and $C$ on one horizontal axis. Show $f$ and $g$ as
two circular operations with matching $B$ ports.

**Motion:**

1. $\rho$ travels $A\xrightarrow{f}B\xrightarrow{g}C$.
2. A thin gold boundary encloses the two nodes.
3. The internal $B$ joint dims; the boundary contracts into one node labelled
   $g\circ f$ while the outer $A$ and $C$ ports do not move.
4. Briefly add $h:C\to D$. Regroup three translucent boundaries to show
   associativity without moving the final $A$ and $D$ ports.
5. Name the connected pair $V=g\circ f$ and copy that same boundary into two
   distinct flows: HTTP bytes to a handler, and queue bytes to a worker.

**Equations:**

$$
(g\circ f)(x)=g(f(x)),
$$

then

$$
h\circ(g\circ f)=(h\circ g)\circ f.
$$

**Review criterion:** The viewer must see that contraction hides the internal
joint, not that the two functions have ceased to exist.

---

### Part 2 — The request becomes a typed pipeline

**Time:** 1:02–1:48

**Frame:** Re-expand the composed node and grow the same system into:

```text
decode -> validate -> authorize -> DTO map -> handle -> encode
```

Type names sit at ports rather than inside prose boxes. The packet $\rho$
changes its small symbolic glyph at each stage but keeps the same gold identity
marker.

**Motion:**

1. Activate one edge at a time as $\rho$ advances.
2. Pull `validate` out of place. The adjacent ports no longer match; movement
   stops at the broken edge.
3. Restore the order.
4. Insert a small explicit adapter at one deliberately mismatched joint.
5. Contract the complete valid path into one operation $P$ with the original
   input and final output ports.

**Equation:**

$$
P=f_n\circ\cdots\circ f_2\circ f_1.
$$

**Review criterion:** Order and compatibility must be visible as properties of
the path. The adapter must read as a real operation, not visual glue.

---

### Part 3 — A wrapper hides a control-flow graph

**Time:** 1:48–2:34

**Transition:** Contract the pipeline and retain only its request and response
ports, $Q$ and $R$.

**Frame:** Show one external subsystem $W[f]:Q\to R$. Open it into a policy
node with two branches: a cache hit that returns directly, and a miss that may
call and retry $f$ before both branches merge.

**Motion:**

1. A request pulse crosses the closed wrapper from $Q$ to $R$.
2. Open the boundary while the outer ports remain fixed.
3. Trace a cache hit through a path containing zero invocations of $f$.
4. Trace a miss through one invocation and one retry of $f$.
5. Contract the graph back into $W[f]$ without moving $Q$ or $R$.

**Equation:**

$$
W:(Q\to R)\to(Q\to R).
$$

Then:

$$
N_f(W,q)\in\{0,1,\ldots,n\}.
$$

**Review criterion:** The wrapper must read as a function with one public
contract and potentially branching hidden behavior. It must not imply that a
wrapper always invokes its wrapped function exactly once.

---

### Part 4 — A query plan repeats one boundary recursively

**Time:** 2:34–3:22

**Transition:** The handler expands its data access into a recursive query
plan.

**Frame:** Use one common operation language for `Scan`, `Filter`, and `Join`.
The join contains a scan and a filter subtree; the filter contains a predicate
and another scan.

**Motion:**

1. Reveal the tree from the root to its leaves with a slight lag.
2. Send `execute()` from the root to immediate children and recursively onward.
3. Row sets return upward and combine at the join.
4. Enclose the filter subtree and contract it into one query operator.
5. Place that operator beside an ordinary scan under the same parent.

**Equations:**

$$
Q::=\operatorname{Scan}(t)
\mid\operatorname{Filter}(p,Q)
\mid\operatorname{Join}(Q_1,Q_2),
$$

and, briefly,

$$
\operatorname{execute}:Q\to\operatorname{Rows}.
$$

**Review criterion:** A viewer should understand that a subtree is usable as a
component because the leaf and group share an interface, not merely because
the drawing is a tree.

---

### Part 5 — The planner preserves paths across representations

**Time:** 3:22–4:12

**Transition:** Keep the logical query plan on the left. On the right, reveal
the runtime operator graph that will execute it.

**Frame:** Source category $\mathcal C$ on the left; target category
$\mathcal D$ on the right. Objects and arrows are sparse and large enough to
read. Dashed gold correspondences map nodes to nodes and arrows to arrows.

**Motion:**

1. Map `Scan`, `Filter`, and `Join` to `SeqScan`, `Predicate`, and `HashJoin`.
2. Map $f$ and $g$ while preserving their adjacency.
3. Illuminate the direct composed edge $g\circ f$ on the source.
4. The corresponding target route illuminates in two steps, then contracts to
   $F(g\circ f)$.
5. Both sides meet visually on the equality sign.

**Equation:**

$$
F(g\circ f)=F(g)\circ F(f),
\qquad
F(\operatorname{id}_A)=\operatorname{id}_{F(A)}.
$$

**Review criterion:** The term “functor” is earned by the two preservation
laws. Avoid suggesting that any converter or mapper qualifies.

---

### Part 6 — The local geometries coexist as architecture

**Time:** 4:12–5:05

**Transition:** The two diagrams recede. Their nodes remain and become part of
the larger graph seen in the opening.

**Frame:** Build one labeled directed multigraph rather than a collection of
new icons:

$$
\mathcal A=(V,E,\lambda_V,\lambda_E).
$$

The earlier shapes are now recognizable inside it:

- the HTTP flow is a directed path;
- trace and retry wrap one handler;
- the query plan is a recursive containment tree;
- the logical-to-runtime planner preserves a diagram.

**Motion:**

1. Reveal the graph by reusing every existing node.
2. Toggle edge projections: data flow, call/return, containment, dependency.
   Non-selected edges remain faint so the common vertex set is obvious.
3. Select a stable subsystem $S$ and contract it into a supernode $v_S$.
4. The supernode composes with its neighbors exactly as the original
   $g\circ f$ node did.

**Equations:**

$$
\pi_q(\mathcal A)=(V,E_q),
$$

then

$$
\mathcal A/S.
$$

**Review criterion:** Architecture must read as multiple meaningful relation
types over shared components. Do not flatten every edge into “connects to.”

---

### Part 7 — Close the scale loop

**Time:** 5:05–5:20

**Motion:** The contracted architecture becomes the same single operation from
Part 1. It expands once—rapidly but legibly—through path, wrapper, tree, and
graph, then settles into the Cohesian seed-pod mark.

**Final line:**

> Scale does not remove local rules. It composes them.

No architecture inventory or repository list follows. The ending must remain
valid even as Cohesian evolves.

## Master narration structure

The complete production narration lives in
[`software-composition-narration.md`](software-composition-narration.md). Each
paragraph maps one-to-one to a storyboard part so it can be voiced and revised
without splitting a sentence across scene files.

## Short-form cut points

These are self-contained arguments, not arbitrary excerpts:

1. **Composition in 40 seconds** — Part 1, with a two-second title and close.
2. **Pipeline versus wrapper** — final 20 seconds of Part 2 plus all of Part 3.
3. **When a tree becomes one component** — Part 4.
4. **A map is not automatically a functor** — Part 5.
5. **Architecture repeats one local move** — contraction sequence from Part 6
   through the final line.

The vertical editions should be re-laid out around one concept. The landscape
master should not be blindly cropped.

## Implementation boundary for T3

- One exportable Loci project under Studio.
- One scene module per storyboard part plus a shared visual helper module.
- Free `gTTS` narration for the first review render.
- Low-quality 16:9 review before any HD render.
- No OpenAI voice call until the preview is accepted explicitly.
- Reusable generic behavior discovered during production belongs upstream in
  Loci; Cohesian visual language belongs in `loci-plugins`; one-off
  choreography remains in Studio.
