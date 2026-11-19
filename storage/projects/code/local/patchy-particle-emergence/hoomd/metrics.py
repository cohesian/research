"""Structural observables derived from saved HOOMD trajectory frames."""

from __future__ import annotations

import math
from typing import Sequence

import numpy as np
from numpy.typing import NDArray

from config import ExperimentConfig

FloatArray = NDArray[np.float64]


def quaternion_angles(orientations: FloatArray) -> FloatArray:
    """Extract planar angles from HOOMD quaternions ``(w, x, y, z)``."""

    return 2.0 * np.arctan2(orientations[:, 3], orientations[:, 0])


def rotated_directors(
    config: ExperimentConfig,
    particle_type: str,
    angle: float,
) -> FloatArray:
    base = np.asarray(config.directors(particle_type), dtype=float)[:, :2]
    cosine = math.cos(angle)
    sine = math.sin(angle)
    rotation = np.asarray(((cosine, -sine), (sine, cosine)), dtype=float)
    return base @ rotation.T


def contact_edges(
    positions: FloatArray,
    orientations: FloatArray,
    type_ids: Sequence[int],
    type_names: Sequence[str],
    config: ExperimentConfig,
) -> tuple[tuple[int, int], ...]:
    """Infer the instantaneous patch-contact graph from one saved frame.

    HOOMD's patch potential is smooth and does not create persistent bonds. A
    contact edge is therefore an analysis projection: centers must be close and
    one patch on each particle must point sufficiently toward the other.
    """

    angles = quaternion_angles(np.asarray(orientations, dtype=float))
    directors = [
        rotated_directors(config, type_names[int(type_id)], float(angle))
        for type_id, angle in zip(type_ids, angles, strict=True)
    ]
    edges: list[tuple[int, int]] = []
    for left in range(len(positions) - 1):
        for right in range(left + 1, len(positions)):
            displacement = positions[right, :2] - positions[left, :2]
            distance = float(np.linalg.norm(displacement))
            if distance == 0.0 or distance > config.contact_cutoff:
                continue
            if config.interaction_mode == "isotropic":
                edges.append((left, right))
                continue
            direction = displacement / distance
            left_alignment = float(np.max(directors[left] @ direction))
            right_alignment = float(np.max(directors[right] @ -direction))
            if (
                left_alignment >= config.minimum_patch_alignment
                and right_alignment >= config.minimum_patch_alignment
            ):
                edges.append((left, right))
    return tuple(edges)


def bond_orientational_order(
    positions: FloatArray,
    edges: Sequence[tuple[int, int]],
    *,
    symmetry: int = 6,
) -> tuple[float, float]:
    """Return local and global bond order for an undirected contact graph.

    ``local`` measures whether each particle's neighborhood has the requested
    angular symmetry even when different domains point in different
    directions. ``global`` is high only when those local domains also share a
    common orientation.
    """

    neighbors: list[list[float]] = [[] for _ in range(len(positions))]
    for left, right in edges:
        displacement = positions[right, :2] - positions[left, :2]
        angle = math.atan2(float(displacement[1]), float(displacement[0]))
        neighbors[left].append(angle)
        neighbors[right].append(angle + math.pi)
    local_values = [
        np.mean(np.exp(1j * symmetry * np.asarray(angles)))
        for angles in neighbors
        if len(angles) >= 2
    ]
    if not local_values:
        return 0.0, 0.0
    return (
        float(np.mean(np.abs(local_values))),
        float(abs(np.mean(local_values))),
    )


def coordination_fractions(
    particle_count: int,
    edges: Sequence[tuple[int, int]],
) -> dict[int, float]:
    degrees = np.zeros(particle_count, dtype=int)
    for left, right in edges:
        degrees[left] += 1
        degrees[right] += 1
    return {
        degree: float(np.mean(degrees == degree))
        for degree in (2, 3, 6)
    }


def component_sizes(
    particle_count: int,
    edges: Sequence[tuple[int, int]],
) -> tuple[int, ...]:
    parent = list(range(particle_count))
    sizes = [1] * particle_count

    def find(node: int) -> int:
        while parent[node] != node:
            parent[node] = parent[parent[node]]
            node = parent[node]
        return node

    def union(left: int, right: int) -> None:
        left_root = find(left)
        right_root = find(right)
        if left_root == right_root:
            return
        if sizes[left_root] < sizes[right_root]:
            left_root, right_root = right_root, left_root
        parent[right_root] = left_root
        sizes[left_root] += sizes[right_root]

    for left, right in edges:
        union(left, right)
    counts: dict[int, int] = {}
    for node in range(particle_count):
        root = find(node)
        counts[root] = counts.get(root, 0) + 1
    return tuple(sorted(counts.values(), reverse=True))


def structural_observables(
    positions: FloatArray,
    orientations: FloatArray,
    type_ids: Sequence[int],
    type_names: Sequence[str],
    config: ExperimentConfig,
) -> dict[str, float]:
    edges = contact_edges(
        positions,
        orientations,
        type_ids,
        type_names,
        config,
    )
    sizes = component_sizes(len(positions), edges)
    angles = quaternion_angles(np.asarray(orientations, dtype=float))
    order = abs(np.mean(np.exp(1j * config.orientational_order * angles)))
    local_sixfold, global_sixfold = bond_orientational_order(
        positions,
        edges,
        symmetry=6,
    )
    coordination = coordination_fractions(len(positions), edges)
    return {
        "contact_count": float(len(edges)),
        "component_count": float(len(sizes)),
        "largest_component_fraction": float(max(sizes) / len(positions)),
        "mean_degree": float(2.0 * len(edges) / len(positions)),
        "orientational_order": float(order),
        "local_bond_order_6": local_sixfold,
        "global_bond_order_6": global_sixfold,
        "coordination_2_fraction": coordination[2],
        "coordination_3_fraction": coordination[3],
        "coordination_6_fraction": coordination[6],
    }
