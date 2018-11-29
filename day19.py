from functools import reduce
from itertools import groupby

def parse(lines):
    return ({ k: [v[2] for v in vs] for (k, vs) in groupby((line.split() for line in lines[:-2]), lambda t: t[0]) },
            lines[-1])

def indices(s, k):
    i = -len(k)
    while True:
        i = s.find(k, i+len(k))
        if i == -1:
            break
        yield i

def molecules(r, m):
    return {m[:i] + m[i:].replace(k, v, 1)
            for (k, vs) in r.items()
            for i in indices(m, k)
            for v in vs}

def reactions(f, r, m, c=0):
    if f == m:
        return c
    elif len(f) > len(m):
        return 0xffffffff
    else:
        return reduce(min, (reactions(f2, r, m, 1+c) for f2 in molecules(r, f)))

def test_19a_ex1(): assert len(molecules(*parse(['H => HO', 'H => OH', 'O => HH', '', 'HOH']))) == 4
def test_19a_ex2(): assert len(molecules(*parse(['H => HO', 'H => OH', 'O => HH', '', 'HOHOHO']))) == 7

def test_19b_ex1(): assert reactions('e', *parse(['e => H', 'e => O', 'H => HO', 'H => OH', 'O => HH', '', 'HOH'])) == 3
def test_19b_ex2(): assert reactions('e', *parse(['e => H', 'e => O', 'H => HO', 'H => OH', 'O => HH', '', 'HOHOHO'])) == 6

def test_19a_answer(day19_lines): assert len(molecules(*parse(day19_lines))) == 518

def _est_19b_answer(day19_lines): assert reactions('e', *parse(day19_lines)) == -13

def test_19b_answer(day19_lines):
    c = len(day19_lines)
    ar_cr = sum('Ar' in line and 'Cr' in line for line in day19_lines)
    y = sum('Y' in line for line in day19_lines)
    assert c - ar_cr - 2**y - 1 == -13
