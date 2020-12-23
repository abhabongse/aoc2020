from __future__ import annotations

import itertools
from collections.abc import Iterator
from dataclasses import dataclass
from typing import Optional

import more_itertools
from tqdm import trange

Graph = tuple['Node', ...]


def main():
    # initial_arrangement = [3, 8, 9, 1, 2, 5, 4, 6, 7]
    initial_arrangement = [4, 5, 9, 6, 7, 2, 8, 1, 3]

    # Part 1
    graph = build_circular_graph(initial_arrangement)
    crab_modify_graph(graph, plucks=3, repeat=100)

    node_1 = more_itertools.first_true(graph, pred=lambda u: u.label == 1)
    final_arrangement = [u.label for u in nodes_in_circle(node_1)]
    p1_answer = ''.join(str(n) for n in final_arrangement[1:])
    print(p1_answer)

    # Part 2
    initial_arrangement = initial_arrangement + list(range(10, 1_000_001))
    graph = build_circular_graph(initial_arrangement)
    crab_modify_graph(graph, plucks=3, repeat=10_000_000)

    node_1 = more_itertools.first_true(graph, pred=lambda u: u.label == 1)
    p2_answer = node_1.next.label * node_1.next.next.label
    print(p2_answer)


@dataclass
class Node:
    label: int
    next: Optional[Node]


def build_circular_graph(arrangement: list[int]) -> Graph:
    """
    Builds a circular graph with linked list from the given arrangement
    and returns the list of nodes corresponding to the given arrangement.
    """
    nodes = tuple(Node(label, None) for label in arrangement)
    for u, v in more_itertools.windowed(itertools.chain(nodes, nodes[0:1]), n=2):
        u.next = v
    return nodes


def nodes_in_circle(start: Node) -> Iterator[Node]:
    """
    Obtains a sequence of nodes starting from the given node until it reaches back to start.
    """
    node = start
    while True:
        yield node
        node = node.next
        if node is start:
            break


def crab_modify_graph(graph: Graph, plucks: int, repeat: int = 1):
    """
    Modify the cups arrangement graph according to crab's challenge.
    It returns the next *current* cup.
    """
    reversed_map = {u.label: u for u in graph}
    current = graph[0]
    for _ in trange(repeat):
        plucked_rear, plucked_labels = compute_plucked(current, plucks)
        candidates = count_in_modulus(current.label - 1, -1, modulo=len(graph))
        dest_label = more_itertools.first_true(candidates, pred=lambda v: v not in plucked_labels)
        dest = reversed_map[dest_label]
        current.next, plucked_rear.next, dest.next = plucked_rear.next, dest.next, current.next
        current = current.next
    return current


def compute_plucked(current: Node, plucks: int) -> tuple[Node, list[int]]:
    """
    Obtains the labels of the next few plucked cups,
    starting from the next cup from the given current node.
    It returns the rear cup plucked as well as labels of all plucked cups.
    """
    labels = []
    for _ in range(plucks):
        current = current.next
        labels.append(current.label)
    return current, labels


def count_in_modulus(start: int, step: int = 1, *, modulo: int) -> Iterator[int]:
    """
    Produces an arithmetic sequence of numbers under the given modulus
    with 1-indexing (so remainder 0 would actually yield the modulus itself).
    """
    for value in itertools.count(start, step):
        yield value % modulo or modulo


if __name__ == '__main__':
    main()
