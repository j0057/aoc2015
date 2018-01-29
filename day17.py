from itertools import combinations

def combine(L, t):
    return [n for n in range(1, len(L)+1) for c in combinations(L, n) if sum(c) == t]

def combine1(L, t):
    return sum(1 for _ in combine(L, t))

def combine2(L, t):
    results = combine(L, t)
    return sum(1 for n in results if n == min(results))

def test_17a_ex1(): assert combine1([20, 15, 10, 5, 5], 25) == 4
def test_17a_ex2(): assert combine2([20, 15, 10, 5, 5], 25) == 3

def test_17a_answer(day17_numbers): assert combine1(day17_numbers, 150) == 1304
def test_17b_answer(day17_numbers): assert combine2(day17_numbers, 150) == 18
