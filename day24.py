from functools import reduce
import operator as op
from itertools import combinations, islice

def day24(L, x):
    def find_groups(N, s, r, cmin=None, cmax=None):
        yield from (sg for sz in range(cmin or 0, (cmax or len(N))+1)
                       for g in combinations(sorted(N, reverse=1), sz) if sum(g) == s
                       for sg in find_groups(N-{*g}, s, r+[g])) \
                   if sum(N) > s else [r+[[*N]]]
    first = lambda G: next(x for x in G if x)
    best = first(islice(find_groups({*L}, sum(L)//x, [], M, M), 1) for M in range(len(L)+1))
    return reduce(op.mul, first(best)[0])

day24_ex = [*range(1, 6)] + [*range(7, 12)]

def test_24_ex1(): assert day24(day24_ex, 3) == 99

def test_24a(day24_numbers): assert day24(day24_numbers, 3) == 10723906903
def test_24b(day24_numbers): assert day24(day24_numbers, 4) == 74850409
