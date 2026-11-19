"""Print one compact walk through the lecture's structures."""

from __future__ import annotations

from .model import Architecture, Box, Contract, Group, Leaf, Pipeline, compose, traced


def main() -> None:
    double = lambda x: x * 2
    increment = lambda x: x + 1

    composite = compose(increment, double)
    pipeline = Pipeline((double, increment))

    events: list[str] = []
    wrapped = traced("outer", traced("inner", composite, events), events)

    tree = Group((Leaf(2), Group((Leaf(3), Leaf(5)))))
    mapped = Box(4).map(double).map(increment)

    packet = Contract("packet/v1")
    architecture = Architecture()
    architecture.connect("reader", packet, "parser", packet)
    architecture.connect("parser", packet, "publisher", packet)

    print(f"composition: {composite(4)}")
    print(f"pipeline:    {pipeline(4)}")
    print(f"wrapper:     {wrapped(4)} -> {events}")
    print(f"composite:   {tree.fold()}")
    print(f"functor map: {mapped}")
    print(f"graph valid: {architecture.valid()}")


if __name__ == "__main__":
    main()

