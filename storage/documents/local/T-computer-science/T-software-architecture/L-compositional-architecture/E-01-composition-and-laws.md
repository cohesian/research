# Composition and Its Laws

> Composition is the smallest architectural move: connect two local rules so
> that their shared boundary disappears from the outside.

## 1. A local transformation

Let a function be a map

$$
f:A\to B.
$$

It accepts values from a domain $A$ and produces values in a codomain $B$.
The notation says nothing yet about how $f$ is implemented. It exposes only a
contract at its boundary.

Now consider a second function

$$
g:B\to C.
$$

The codomain of $f$ matches the domain of $g$. Their shared type $B$ is the
local joint that makes direct composition possible.

## 2. Hiding the internal joint

The composition of $f$ followed by $g$ is

$$
g\circ f:A\to C,
$$

defined by

$$
(g\circ f)(x)=g(f(x)).
$$

From inside, two transformations still occur:

$$
x\xmapsto{f}f(x)\xmapsto{g}g(f(x)).
$$

From outside, the pair exposes one boundary:

$$
A\xrightarrow{g\circ f}C.
$$

This is the first compositional abstraction. Internal structure remains real,
but a larger unit can be treated through its outer contract.

## 3. Compatibility is a condition

If instead

$$
f:A\to B,
\qquad
g:D\to C,
$$

then $g\circ f$ is not automatically defined. We need either

$$
B=D
$$

or an explicit adapter

$$
\alpha:B\to D.
$$

The resulting composition is

$$
g\circ\alpha\circ f:A\to C.
$$

In software, parsers, serializers, protocol adapters, DTO mappings, and unit
conversions often occupy this exact structural position. An adapter is not
free: it becomes part of the composed behavior.

## 4. Identity

Every domain $A$ has an identity map

$$
\operatorname{id}_A:A\to A,
\qquad
\operatorname{id}_A(x)=x.
$$

It changes no value. For every $f:A\to B$,

$$
f\circ\operatorname{id}_A=f
$$

and

$$
\operatorname{id}_B\circ f=f.
$$

Identity matters because it gives a neutral element for composition. A stage
may be inserted or removed without changing the surrounding behavior when that
stage is truly the identity for the relevant domain.

## 5. Associativity

Given

$$
f:A\to B,
\qquad
g:B\to C,
\qquad
h:C\to D,
$$

composition is associative:

$$
h\circ(g\circ f)=(h\circ g)\circ f.
$$

Both sides send $x\in A$ to

$$
h(g(f(x))).
$$

Associativity lets us regroup a valid chain without changing its denotation.
This is a major reason compositional systems can be modular: a subsystem may be
replaced by its composite boundary and composed again at a larger scale.

Associativity does **not** imply commutativity. In general,

$$
g\circ f\neq f\circ g,
$$

and one side may not even be type-correct.

## 6. Pure equations and effects

The equations above describe mathematical functions. Real software operations
may also read clocks, write files, mutate state, fail, retry, or run
concurrently. Then the visible output value may not capture the whole effect.

We can still compose such computations, but only after making their execution
contract explicit. For example, a result type can expose failure:

$$
f:A\to \operatorname{Result}(B,E).
$$

The structural lesson is not that all software is pure. It is that composition
becomes trustworthy when the relevant boundary is visible.

## 7. The first scale transition

A composed map is simultaneously:

- many local steps when inspected internally;
- one usable component when inspected externally.

That change of scale will reappear in pipelines, wrappers, composites, and
whole architectures. The recurring question is:

$$
\text{Which internal details may be hidden without breaking the contract?}
$$

