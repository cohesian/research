"""Small, separate models of the structures discussed in the lecture."""

from __future__ import annotations

from collections.abc import Callable, Iterable
from dataclasses import dataclass, field
from functools import reduce
from typing import Generic, Protocol, TypeVar

A = TypeVar("A")
B = TypeVar("B")
C = TypeVar("C")


def identity(value: A) -> A:
    """The neutral function for composition."""

    return value


def compose(g: Callable[[B], C], f: Callable[[A], B]) -> Callable[[A], C]:
    """Return g after f: (g ∘ f)(x) = g(f(x))."""

    return lambda value: g(f(value))


@dataclass(frozen=True)
class Pipeline:
    """A left-to-right path of unary stages."""

    stages: tuple[Callable[[object], object], ...]

    def __call__(self, value: object) -> object:
        return reduce(lambda current, stage: stage(current), self.stages, value)


def traced(
    name: str,
    operation: Callable[[A], B],
    events: list[str],
) -> Callable[[A], B]:
    """Wrap an operation while preserving its unary interface."""

    def wrapper(value: A) -> B:
        events.append(f"enter:{name}")
        result = operation(value)
        events.append(f"exit:{name}")
        return result

    return wrapper


class Component(Protocol):
    """Common interface shared by leaves and composite groups."""

    def fold(self) -> int: ...


@dataclass(frozen=True)
class Leaf:
    value: int

    def fold(self) -> int:
        return self.value


@dataclass(frozen=True)
class Group:
    children: tuple[Component, ...]

    def fold(self) -> int:
        return sum(child.fold() for child in self.children)


@dataclass(frozen=True)
class Box(Generic[A]):
    """A minimal container whose map operation follows the functor laws."""

    value: A

    def map(self, function: Callable[[A], B]) -> Box[B]:
        return Box(function(self.value))


@dataclass(frozen=True)
class Contract:
    """A deliberately tiny boundary contract for the graph example."""

    name: str


@dataclass(frozen=True)
class Port:
    component: str
    contract: Contract


@dataclass(frozen=True)
class Edge:
    source: Port
    target: Port

    @property
    def compatible(self) -> bool:
        return self.source.contract == self.target.contract


@dataclass
class Architecture:
    """A graph that validates only local edge contracts."""

    components: set[str] = field(default_factory=set)
    edges: list[Edge] = field(default_factory=list)

    def connect(
        self,
        source: str,
        source_contract: Contract,
        target: str,
        target_contract: Contract,
    ) -> None:
        self.components.update((source, target))
        edge = Edge(Port(source, source_contract), Port(target, target_contract))
        if not edge.compatible:
            raise ValueError(
                f"incompatible edge: {source_contract.name} -> "
                f"{target_contract.name}"
            )
        self.edges.append(edge)

    def valid(self) -> bool:
        return all(edge.compatible for edge in self.edges)

    def neighbors(self, component: str) -> Iterable[str]:
        return (
            edge.target.component
            for edge in self.edges
            if edge.source.component == component
        )

