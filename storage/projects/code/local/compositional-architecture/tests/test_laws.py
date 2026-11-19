from __future__ import annotations

import unittest

from compositional_architecture import (
    Architecture,
    Box,
    Contract,
    Group,
    Leaf,
    Pipeline,
    compose,
    identity,
    traced,
)


class CompositionTests(unittest.TestCase):
    def test_identity_law(self) -> None:
        increment = lambda x: x + 1
        self.assertEqual(compose(increment, identity)(4), increment(4))
        self.assertEqual(compose(identity, increment)(4), increment(4))

    def test_associativity(self) -> None:
        increment = lambda x: x + 1
        double = lambda x: x * 2
        square = lambda x: x**2
        left = compose(square, compose(double, increment))
        right = compose(compose(square, double), increment)
        self.assertEqual(left(3), right(3))

    def test_pipeline_preserves_order(self) -> None:
        pipeline = Pipeline((lambda x: x + 1, lambda x: x * 2))
        self.assertEqual(pipeline(3), 8)


class WrapperAndCompositeTests(unittest.TestCase):
    def test_wrapper_records_call_and_return_order(self) -> None:
        events: list[str] = []
        operation = traced(
            "outer",
            traced("inner", lambda x: x + 1, events),
            events,
        )
        self.assertEqual(operation(2), 3)
        self.assertEqual(
            events,
            ["enter:outer", "enter:inner", "exit:inner", "exit:outer"],
        )

    def test_composite_fold(self) -> None:
        component = Group((Leaf(2), Group((Leaf(3), Leaf(5)))))
        self.assertEqual(component.fold(), 10)


class FunctorLawTests(unittest.TestCase):
    def test_identity_law(self) -> None:
        value = Box(7)
        self.assertEqual(value.map(identity), value)

    def test_composition_law(self) -> None:
        value = Box(7)
        increment = lambda x: x + 1
        double = lambda x: x * 2
        self.assertEqual(
            value.map(compose(double, increment)),
            value.map(increment).map(double),
        )


class ArchitectureTests(unittest.TestCase):
    def test_compatible_edge(self) -> None:
        graph = Architecture()
        packet = Contract("packet/v1")
        graph.connect("reader", packet, "parser", packet)
        self.assertTrue(graph.valid())
        self.assertEqual(list(graph.neighbors("reader")), ["parser"])

    def test_incompatible_edge_is_rejected(self) -> None:
        graph = Architecture()
        with self.assertRaises(ValueError):
            graph.connect(
                "reader",
                Contract("bytes/v1"),
                "parser",
                Contract("json/v1"),
            )


if __name__ == "__main__":
    unittest.main()

