# Compositional Architecture Lab

This standard-library Python project makes the structures in
`L-compositional-architecture` executable without pretending they are the same
abstraction.

It demonstrates:

- associative function composition and identity;
- a left-to-right pipeline;
- wrappers with visible inward/outward execution;
- a recursive composite and fold;
- a `Box.map` operation satisfying the two functor laws;
- local contract checks on architecture edges.

Run the demonstration from this directory:

```bash
python -m compositional_architecture.demo
```

Run the checks:

```bash
python -m unittest discover -s tests -v
```

The code is intentionally small. It is executable documentation, not a
general-purpose framework.

