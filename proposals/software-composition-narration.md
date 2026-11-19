# From Functions to Architecture — Master Narration

## Part 0 — One request, many scales

A client sends one HTTP request. Before a response comes back, that request
crosses a gateway, authorization, business logic, storage, and observation.
The full graph looks large, but every step begins with one local contract. To
understand the architecture, follow the request.

The visual grammar will stay fixed. A small card is one local operation, a
wider card is a named composition, and a subsystem is the largest reusable
boundary. The symbols $f$, $P$, $W$, $Q$, and $v_S$ tell us which scale is
currently exposed.

## Part 1 — Composition

The gateway first decodes bytes into a request. Call that function $f$ from
$A$ to $B$. Validation receives that request and produces a trusted shape.
Call it $g$ from $B$ to $C$. Because both operations agree on $B$, the output
of decode can become the input of validate.

From inside, the request still crosses decoding and validation. From outside,
we can use the pair as one operation, $g$ after $f$, from bytes directly to a
validated request.
Composition has not erased the internal steps. It has hidden their compatible
joint behind a larger contract.

With a third compatible function, we may regroup the chain without changing
its result. That is associativity, and it is our first mechanism for changing
scale.

A stable boundary can now participate in more than one larger flow. The same
decode-and-validate module $V=g\circ f$ can serve an HTTP handler and a queue
worker. We reuse the connected pair without exposing or duplicating its
internal joint.

## Part 2 — Pipeline

Now make every joint visible. The request is decoded, validated, authorized,
handled, and encoded as JSON. The equation has become a real request pipeline.

Each stage asks only a local question. Does my output satisfy the next input?
Yet the complete path is composable only when every local joint is valid.
Change the order and the path may compute something different—or stop making
sense at all.

If the handler expects a domain command rather than the transport request, an
explicit DTO mapper can connect the ports. That conversion is a real operation
with real behavior. Once every joint is explicit, the whole pipeline can again
be contracted into one usable boundary.

## Part 3 — Wrapper

A wrapper is itself a function. From outside, it receives one input in $Q$ and
returns one output in $R$. The process between those ports is deliberately
hidden behind $W[f]$.

Open that boundary and the hidden process may be a graph. A policy can branch.
A cache hit can return without calling $f$ at all. A miss can call $f$ once,
retry it several times, and merge the result before returning.

The wrapper may short-circuit, branch, transform values, or invoke its wrapped
function zero, one, or many times. What it preserves is not a single internal
path. It preserves the outer contract from $Q$ to $R$, so the larger pipeline
can use $W[f]$ wherever it could use $f$.

## Part 4 — Recursive query plan

Inside the handler, data access is not one indivisible call. A join contains a
scan and a filtered subtree; that filter contains a predicate and another
scan. The request has reached a real recursive query plan.

Every operator exposes the same `execute` boundary. A scan returns rows. A
filter executes its child and removes rows. A join executes two children and
combines their results. Because every child is another query operator, the
same local rule applies recursively.

No node needs a description of the entire tree. And because a complete subtree
still exposes the shared boundary, it can be contracted and used beside an
ordinary leaf. A structure has become one component at the next scale.

## Part 5 — Logical plan to runtime plan

The query planner now changes representation. Scan, filter, and join are
logical operators. Sequential scan, predicate evaluation, and hash join are
executable runtime operators.

Mapping nodes is not enough. A structure-preserving translation must map
arrows as well, preserve identity, and preserve composition. Translating a
composed route must agree with translating each step and then composing the
results.

If this compiler preserves identities and composition, this is the functor
law. It is stronger than conversion and more precise than calling something a
mapper. The representation may change radically while the paths that give it
meaning survive.

## Part 6 — Architecture

Now zoom out. The request path, middleware stack, query plan, and plan
translation all coexist in one software architecture graph.

Its arrows do not all mean the same thing. Some carry data. Some represent
calls and returns. Some express containment or dependency. By selecting one
edge family, we obtain a projection of the same components for a particular
question.

The earlier patterns have not become one universal pattern. They remain local
geometries with different laws. What unifies them is disciplined composition:
explicit boundaries, compatible contracts, and relations whose meaning is not
lost when we move between scales.

When a connected subsystem exposes a stable outer contract, we can contract it
into a supernode. Internally it remains an architecture. Externally it becomes
one component that can compose again.

## Part 7 — Close

Complexity did not disappear. It became organized behind boundaries that can
be understood, tested, and reused. Architecture is not merely a large diagram.
It is the repeated transformation of local rules into larger, usable wholes.

Scale does not remove local rules. It composes them.
