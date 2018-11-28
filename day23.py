from collections import defaultdict
import re

def parse(lines):
    return [(op, r, int(o or '0'))
            for (op, r, o)
            in [re.match_groups(r'^(\w+)(?: (\w),?)?(?: ([+-]\d+))?$', i) for i in lines]]

def day23(code, **init):
    reg = defaultdict(int, **init)
    while 0 <= reg['ip'] < len(code):
        op, r, o = code[reg['ip']]
        if   op == 'hlf': reg[r] //= 2
        elif op == 'tpl': reg[r] *= 3
        elif op == 'inc': reg[r] += 1
        elif op == 'jmp': reg['ip'] += (o-1)
        elif op == 'jie': reg['ip'] += (o-1) if reg[r]&1 == 0 else 0
        elif op == 'jio': reg['ip'] += (o-1) if reg[r]   == 1 else 0
        reg['ip'] += 1
    return reg

day23_ex1 = 'inc a|jio a, +2|tpl a|inc a'.split('|')

def test_23_ex0(): assert parse(day23_ex1) \
        == [('inc', 'a', 0), ('jio', 'a', 2), ('tpl', 'a', 0), ('inc', 'a', 0)]

def test_23_ex1(): assert day23(parse(day23_ex1)) == {'ip':4, 'a':2}

def test_23a(day23_lines): assert day23(parse(day23_lines), a=0) == {'ip':49, 'a':1, 'b':184}
def test_23b(day23_lines): assert day23(parse(day23_lines), a=1) == {'ip':49, 'a':1, 'b':231}
