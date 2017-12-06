import re
from itertools import groupby, permutations

def parse(line):
    match = re.match(r'^(\w+) would (gain|lose) (\d+) happiness units by sitting next to (\w+).$', line)
    if not match:
        raise Exception(line)
    p1, s, v, p2 = match.groups()
    return (p1, p2, +int(v) if s == 'gain' else -int(v))

def get_score(graph, arr):
    return sum(graph[p1][p2] for (p1, p2) in zip(arr, arr[1:]+[arr[0]])) \
         + sum(graph[p2][p1] for (p1, p2) in zip(arr, arr[1:]+[arr[0]]))

def happiness_maximum(lines, also_include=None):
    parsed = [ parse(line) for line in lines ]
    graph = { p1: { p2: v for (_, p2, v) in group }
              for (p1, group) in groupby(parsed, lambda t: t[0]) }
    if also_include is not None:
        for p in graph:
            graph[p][also_include] = 0
        graph[also_include] = { p2: 0 for p2 in graph.keys() }
    best = max(permutations(graph), key=lambda arr: get_score(graph, list(arr)))
    return get_score(graph, list(best))

def test_13a_ex1():
    assert happiness_maximum([
        'Alice would gain 54 happiness units by sitting next to Bob.',
        'Alice would lose 79 happiness units by sitting next to Carol.',
        'Alice would lose 2 happiness units by sitting next to David.',
        'Bob would gain 83 happiness units by sitting next to Alice.',
        'Bob would lose 7 happiness units by sitting next to Carol.',
        'Bob would lose 63 happiness units by sitting next to David.',
        'Carol would lose 62 happiness units by sitting next to Alice.',
        'Carol would gain 60 happiness units by sitting next to Bob.',
        'Carol would gain 55 happiness units by sitting next to David.',
        'David would gain 46 happiness units by sitting next to Alice.',
        'David would lose 7 happiness units by sitting next to Bob.',
        'David would gain 41 happiness units by sitting next to Carol.'
    ]) == 330

def test_13a_answer(day13_lines): assert happiness_maximum(day13_lines) == 733
def test_13b_answer(day13_lines): assert happiness_maximum(day13_lines, also_include='Joost') == 725 # ungrateful bastards!
