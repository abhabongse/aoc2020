from __future__ import annotations

import collections
import os
import re
from graphlib import TopologicalSorter  # noqa

Rules = dict[str, dict[str, int]]
AdjacencyList = dict[str, list[str]]

BAG_RE = re.compile(r'(?:(?P<count>\d+) )?(?P<color>\w+ \w+) bags?')


def main():
    this_dir = os.path.dirname(os.path.abspath(__file__))
    input_file = os.path.join(this_dir, 'input.txt')
    rules = read_input_files(input_file)

    # Part 1: count the number of bag colors that may enclose the shiny gold one
    p1_answer = count_enclosing_bags(rules, central_color='shiny gold')
    print(p1_answer)

    # Part 2: count the number of bags within a shiny gold bag
    p2_answer = count_containing_bags(rules, central_color='shiny gold')
    print(p2_answer)


def count_enclosing_bags(rules: Rules, central_color: str) -> int:
    """
    Counts the number of bag colors that may enclose
    a bag of the given central color.
    """
    reversed_adjlist = extract_reversed_adjlist(rules)
    enclosing_bags = reachable_nodes(reversed_adjlist, central_color)
    return len(enclosing_bags) - 1


def count_containing_bags(rules: Rules, central_color: str) -> int:
    """
    Counts the number of bags which are contained
    within a bag of the given central color.
    """
    adjlist = extract_adjlist(rules)
    contained_bags = reachable_nodes(adjlist, central_color)

    # TopologicalSorter requires the graph in the reversed direction
    reversed_adjlist = {
        k: v for k, v in extract_reversed_adjlist(rules).items()
        if k in contained_bags
    }

    total_counts = collections.Counter()
    total_counts[central_color] = 1
    for curr in TopologicalSorter(reversed_adjlist).static_order():
        for color, count in rules[curr].items():
            total_counts[color] += count * total_counts[curr]

    return sum(total_counts.values()) - 1


def extract_adjlist(rules: Rules) -> AdjacencyList:
    """
    Extracts the normal adjacency list which is a dictionary mapping
    from each from-node to a list of to-nodes.
    """
    return {
        subject: list(contents.keys())
        for subject, contents in rules.items()
    }


def extract_reversed_adjlist(rules: Rules) -> AdjacencyList:
    """
    Extracts the reversed adjacency list which is a dictionary mapping
    from each from-node to a list of to-nodes.
    """
    adjlist = collections.defaultdict(list)
    for subject, contents in rules.items():
        for color in contents.keys():
            adjlist[color].append(subject)
    return adjlist


def reachable_nodes(adjlist: AdjacencyList, source: str) -> set:
    """
    Computes a set of reachable nodes from the given source node
    using depth-first search (DFS) algorithm.
    """
    queue = collections.deque([source])
    visited = set()

    while queue:
        curr = queue.popleft()
        if curr in visited:
            continue
        visited.add(curr)
        queue.extend(adjlist[curr])

    return visited


def read_input_files(input_file: str) -> Rules:
    """
    Extracts a dictionary of rules from the input file.
    """
    with open(input_file) as input_fobj:
        rules = dict(parse_rule(line.strip()) for line in input_fobj)
    return rules


def parse_rule(rule_text: str) -> tuple[str, dict[str, int]]:
    """
    Parses a line of rule text into a tuple pair of
    - subject bag color
    - a dictionary mapping from each content bag color to its cardinality
    """
    subject_text, contents_text = rule_text.strip().split(' contain ')
    subject = BAG_RE.search(subject_text).group('color')

    contents = {}
    for matchobj in BAG_RE.finditer(contents_text):
        color = matchobj.group('color')
        if color == 'no other':
            continue
        count = int(matchobj.group('count'))
        contents[color] = count
    return subject, contents


if __name__ == '__main__':
    main()
