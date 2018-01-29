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
    return (m[:i] + m[i:].replace(k, v, 1)
            for (k, vs) in r.items()
            for i in indices(m, k)
            for v in vs)
        
def count_molecules(r, m):
    return len(set(molecules(r, m)))

def count_reactions(f, r, m):
    pass

EX19_1 = ['H => HO', 'H => OH', 'O => HH', '', 'HOH']
EX19_2 = ['H => HO', 'H => OH', 'O => HH', '', 'HOHOHO']

def test_19a_ex1(): assert count_molecules(*parse(['H => HO', 'H => OH', 'O => HH', '', 'HOH'])) == 4
def test_19a_ex2(): assert count_molecules(*parse(['H => HO', 'H => OH', 'O => HH', '', 'HOHOHO'])) == 7

def test_19b_ex1(): assert count_reactions('e', *parse(['e => H', 'e => O', 'H => HO', 'H => OH', 'O => HH', '', 'HOH'])) == 3
def test_19b_ex2(): assert count_reactions('e', *parse(['e => H', 'e => O', 'H => HO', 'H => OH', 'O => HH', '', 'HOHOHO'])) == 6

def test_19a_answer(day19_lines): assert count_molecules(*parse(day19_lines)) == 518

def test_19b_answer(day19_lines): assert count_reactions('e', *parse(day19_lines)) == None
