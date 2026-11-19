# Software Composition Topic Proposal

## Purpose

Build one continuous path from ordinary function composition to software
architecture. The topic separates structures that are often conflated:

- composition as a law-governed operation;
- pipelines as directed paths of compatible stages;
- wrappers and decorators as nested call/return structure;
- composites as recursive part/whole structure;
- functors as structure-preserving maps;
- architecture as a graph of local components and explicit contracts.

The existing `L-functions` and `L-composite` material remains valid and supplies
deeper background. This proposal is a synthesis: it explains how those local
ideas scale into an architectural view without claiming that every software
abstraction is automatically a category-theoretic functor.

Research proposes the content and topology below. K-graph remains responsible
for accepting the proposal and assigning canonical identifiers.

## Lecture abstract

Software architecture does not begin at the scale of services or repositories.
It begins when two local transformations can be joined without erasing the
contract that makes the joint valid. This lecture follows that single idea
across increasing structural scales: mathematical composition, directed
pipelines, nested wrappers, interface-preserving decorators, recursive
composites, structure-preserving functors, and finally labeled architecture
graphs. Each step introduces a distinct geometry and a distinct law. Together
they explain when a subsystem may be treated as one component—and when hiding
its internal structure would make the larger system less trustworthy.

## Learning outcomes

After the lecture, a reader should be able to:

1. state the identity and associativity laws for function composition;
2. identify the compatibility condition at a pipeline boundary;
3. distinguish data-flow paths from nested call/return structure;
4. distinguish decorators from generic wrappers and composites;
5. state both functor laws and recognize when “functor-like” is only a metaphor;
6. model an architecture as a labeled graph with multiple valid projections;
7. explain how a stable subsystem boundary permits graph contraction and
   composition at a larger scale.

## Proposed TLE

```text
T-computer-science
└── T-software-architecture
    └── L-compositional-architecture
        ├── E-01-composition-and-laws
        ├── E-02-pipelines-and-compatibility
        ├── E-03-wrappers-and-decorators
        ├── E-04-composites-and-recursion
        ├── E-05-functors-and-structure-preservation
        └── E-06-from-local-contracts-to-architecture
```

All proposed nodes are new. Their identifiers remain unassigned until K-graph
accepts the topology.

Suggested composite metadata:

| Node | Title | Description |
| --- | --- | --- |
| `T-software-architecture` | Software Architecture | Local contracts and compositional structures at architectural scale. |
| `L-compositional-architecture` | Compositional Architecture | From function composition to paths, wrappers, recursive components, functors, and system graphs. |

## Proposed grouping edges

- `T-computer-science` groups `T-software-architecture`.
- `T-software-architecture` groups `L-compositional-architecture`.
- `L-compositional-architecture` groups the six Entries above.

## Proposed linear edges

```text
E-01-composition-and-laws
  -> E-02-pipelines-and-compatibility
  -> E-03-wrappers-and-decorators
  -> E-04-composites-and-recursion
  -> E-05-functors-and-structure-preservation
  -> E-06-from-local-contracts-to-architecture
```

Each arrow proposes one `NEXT` edge. The inverse may be exposed as `PREV`
according to the K-graph convention.

## Proposed resources

| Node | Hierarchy | Key | Protocol |
| --- | --- | --- | --- |
| Every Entry | `documents` | `md` | `markdown-file@1` |
| `E-06-from-local-contracts-to-architecture` | `code` | `python-project` | `python-project@1` |

The Python project is executable documentation. It uses only the standard
library and tests the laws and structural distinctions developed in the prose.

## Semantic boundaries

- Function composition is defined only when adjacent domains are compatible.
- Composition is associative, but generally not commutative.
- A pipeline describes adjacency and data flow; a wrapper describes nesting
  and return flow. One implementation can exhibit both views, but the views
  are not identical.
- A decorator preserves an interface while adding behavior around another
  component. Merely calling another function is not sufficient to establish
  the Decorator pattern.
- A composite gives leaves and containers a common interface and recursive
  shape. A generic tree is not automatically an instance of the pattern.
- A functor maps objects and morphisms while preserving identities and
  composition. “Functor-like” programming analogies are labeled as analogies
  unless both laws are established.
- Architecture is not reduced to a single pattern. The final Entry treats it
  as a graph whose useful compositions depend on explicit local contracts.
