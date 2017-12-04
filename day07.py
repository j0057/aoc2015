import re

import pytest

class WireCircuit(object):
    def __init__(self):
        self.wires = {}

    def __getitem__(self, item):
        if not isinstance(self.wires[item], int):
            self.wires[item] = self.wires[item]()
        return self.wires[item]

    def execute(self, program):
        parsers = [
            (r'^([0-9]+) -> ([a-z]+)$',                     lambda v: v),
            (r'^([a-z]+) -> ([a-z]+)$',                     lambda a: self[a]),
            (r'^([0-9]+) AND ([a-z]+) -> ([a-z]+)$',        lambda v, a: v & self[a]),
            (r'^([a-z]+) AND ([a-z]+) -> ([a-z]+)$',        lambda a1, a2: self[a1] & self[a2]),
            (r'^([a-z]+) OR ([a-z]+) -> ([a-z]+)$',         lambda a1, a2: self[a1] | self[a2]),
            (r'^([a-z]+) LSHIFT ([0-9]+) -> ([a-z]+)$',     lambda a, v: (self[a] << v) & 0xffff),
            (r'^([a-z]+) RSHIFT ([0-9]+) -> ([a-z]+)$',     lambda a, v: (self[a] >> v) & 0xffff),
            (r'^NOT ([a-z]+) -> ([a-z]+)$',                 lambda a: ~self[a] & 0xffff)
        ]
        for line in program:
            for (regex, operation) in parsers:
                match = re.match(regex, line)
                if not match:
                    continue
                args = [ int(v) if v.isnumeric() else v for v in match.groups() ]
                self.wires[args[-1]] = (lambda op, a: lambda: op(*a))(operation, args[:-1])
                break
            else:
                raise Exception(line)

circuit = pytest.fixture(lambda: WireCircuit())

def test_7a_ex0(circuit):
    circuit.execute(['123 -> x'])
    assert circuit['x'] == 123

def test_7a_ex1(circuit):
    circuit.execute([
        '123 -> x',
        '456 -> y',
        'x AND y -> d',
        'x OR y -> e',
        'x LSHIFT 2 -> f',
        'y RSHIFT 2 -> g',
        'NOT x -> h',
        'NOT y -> i'
    ])
    assert circuit['d'] == 72
    assert circuit['e'] == 507
    assert circuit['f'] == 492
    assert circuit['g'] == 114
    assert circuit['h'] == 65412
    assert circuit['i'] == 65079
    assert circuit['x'] == 123
    assert circuit['y'] == 456

def test_7a_answer(circuit, day07_lines):
    circuit.execute(day07_lines)
    assert circuit['a'] == 46065

def test_7b_answer(circuit, day07_lines):
    circuit.execute(day07_lines + ['46065 -> b'])
    assert circuit['a'] == 14134
