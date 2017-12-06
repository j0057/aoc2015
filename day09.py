
import re
from itertools import groupby

def parse(lines):
    def parse_line(line):
        match = re.match(r'^(\w+) to (\w+) = (\d+)$', line)
        if not match:
            raise Exception(line)
        g = match.groups()
        return (g[0], g[1], int(g[2]))
    parsed = [ parse_line(line) for line in lines ]
    parsed += [ (d, s, w) for (s, d, w) in parsed ]
    return { s: { d: w for (_, d, w) in ds } for (s, ds) in groupby(sorted(parsed), lambda t: t[0]) }

def find_all_paths(G, p=[]):
    if len(p) == 0:
        for s in G:
            yield from find_all_paths(G, [s])
    elif len(p) < len(G):
        for d in G[p[-1]]:
            if d not in p:
                yield from find_all_paths(G, p+[d])
    else:
        yield p

def get_path_len(graph, path):
    return sum(graph[a][b] for (a, b) in zip(path, path[1:]))

def find_path(lines, func):
    graph = parse(lines)
    paths = list(find_all_paths(graph))
    shortest = func(paths, key=lambda p: get_path_len(graph, p))
    return get_path_len(graph, shortest)

def find_shortest_path(lines):
    return find_path(lines, min)

def find_longest_path(lines):
    return find_path(lines, max)

EX9 = [
    'London to Dublin = 464',
    'London to Belfast = 518',
    'Dublin to Belfast = 141'
]

def test_9a_ex1(): assert parse(EX9) == {
    'Belfast': { 'Dublin': 141, 'London': 518 },
    'Dublin' : { 'Belfast': 141, 'London': 464 },
    'London' : { 'Belfast': 518, 'Dublin': 464 }
}
def test_9a_ex2(): assert get_path_len(parse(EX9), ['London', 'Dublin', 'Belfast']) == 605
def test_9a_ex3(): assert find_shortest_path(EX9) == 605

def test_9b_ex1(): assert find_longest_path(EX9) == 982

def test_9a_answer(day09_lines): assert find_shortest_path(day09_lines) == 117
def test_9b_answer(day09_lines): assert find_longest_path(day09_lines) == 909
