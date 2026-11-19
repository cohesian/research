# From Local Contracts to Architecture

> Architecture appears when many local boundaries, relations, and rules are
> considered as one evolving system.

## 1. Components and relations

Model a software architecture as a labeled directed multigraph

$$
\mathcal A=(V,E,\lambda_V,\lambda_E).
$$

Here:

- $V$ is the set of components;
- $E$ is the set of directed relations;
- $\lambda_V$ assigns a component contract or role to each node;
- $\lambda_E$ assigns a relation type or protocol to each edge.

Different edges may represent different facts:

- calls;
- data flow;
- dependency;
- containment;
- publication;
- observation.

Flattening all of them into one unlabeled arrow destroys useful semantics.

## 2. Local validity

For an edge $e:u\to v$, let

$$
\operatorname{out}(u,e)
$$

be the contract exposed by $u$, and

$$
\operatorname{in}(v,e)
$$

the contract required by $v$. The edge is locally valid when

$$
\operatorname{out}(u,e)
\cong
\operatorname{in}(v,e),
$$

possibly through an explicit adapter.

This is the pipeline compatibility rule generalized from a path to a graph.
Each node can remain locally understandable while the graph grows globally.

## 3. Multiple projections

One system graph supports many projections. Given an edge predicate $q$, define

$$
E_q=\{e\in E\mid q(\lambda_E(e))\}.
$$

Then

$$
\pi_q(\mathcal A)=(V,E_q)
$$

shows only the selected relation family.

Examples include:

- a dependency projection;
- a runtime-call projection;
- a data-flow projection;
- an ownership projection;
- a deployment projection.

These are not competing architectures. They are different questions asked of
the same system.

## 4. Patterns as local graph shapes

The earlier structures reappear as subgraphs or interpretations:

- a **composition** contracts a compatible path into one boundary;
- a **pipeline** is a directed path;
- a **wrapper** is nested call/return structure;
- a **decorator** is a one-around-one wrapper preserving an interface;
- a **composite** is recursive one-to-many containment under one interface;
- a **functor** translates one compositional graph into another while
  preserving identity and composition.

No single pattern describes the entire architecture. Their value is local:
they make repeated shapes recognizable and give those shapes laws.

## 5. Scale through contraction

Let $S\subseteq V$ be a connected subsystem with a stable outer contract. We
may contract it into a supernode $v_S$:

$$
\mathcal A/S.
$$

Internally, $S$ may contain many nodes and edges. Externally, other components
interact with $v_S$ through the exposed boundary.

This is the graph analogue of replacing

$$
A\xrightarrow{f}B\xrightarrow{g}C
$$

with

$$
A\xrightarrow{g\circ f}C.
$$

Architecture therefore repeats the original compositional move at a larger
scale.

## 6. Cohesion and coupling

Composition is useful when a boundary encloses behavior that changes for a
shared reason. This is cohesion. A boundary becomes costly when it must know
too many unrelated neighbors or when many external nodes depend on its hidden
details. This is coupling.

Graph degree alone does not measure either property. A highly connected router
may have one cohesive role, while a low-degree component may still mix
unrelated concerns. The labels and contracts matter.

## 7. Failure of composition

A system can be assembled without being meaningfully compositional. Warning
signs include:

- hidden shared state;
- incompatible assumptions behind identical types;
- order-sensitive wrappers whose order is undocumented;
- adapters that silently discard information;
- cycles with no explicit convergence rule;
- a “common interface” so broad that it communicates no constraint.

Composition succeeds when local substitution preserves the relevant behavior
of the larger system, not merely when the code compiles.

## 8. One continuous idea

The lecture can now be read as one scale transition:

$$
\text{function}
\to
\text{composition}
\to
\text{path}
\to
\text{nesting}
\to
\text{recursive tree}
\to
\text{architecture graph}.
$$

At every scale, the same discipline returns:

1. expose a boundary;
2. state the local contract;
3. make relations explicit;
4. preserve the laws relied upon by consumers;
5. hide only what can safely be hidden.

Scale does not remove local rules. It composes them.

## 9. Connections to the existing corpus

This lecture is a synthesis rather than a replacement for the earlier detailed
studies:

- [Functions](../../L-functions/E-01-function.md) develops the bounded
  executable node.
- [Function Network](../../L-functions/E-03-function-network.md) studies paths
  and wrapper trees directly as graphs.
- [Function Natural Wrappers](../../L-functions/E-04-function-natural-wrappers.md)
  examines coordination burden inside ordinary functions.
- [Carbon Binder](../../L-composite/E-01-carbon-binder.md) introduces the shared
  interface as reusable structural glue.
- [TLE Composite](../../L-composite/E-04-TLE-composite.md) applies recursive
  composition and multiple edge projections to a knowledge corpus.
