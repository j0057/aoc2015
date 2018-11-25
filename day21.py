from itertools import chain, combinations
from functools import reduce
import math

WEAPON = [ (8, 4, 0), (10, 5, 0),  (25, 6, 0), (40, 7, 0),  (74, 8, 0)]
ARMOR  = [(13, 0, 1), (31, 0, 2),  (53, 0, 3), (75, 0, 4), (102, 0, 5)]
RING   = [(25, 1, 0), (50, 2, 0), (100, 3, 0), (20, 0, 1),  (40, 0, 2), (80, 0, 3)]

def parse(grid):
    return tuple(int(row[-1]) for row in grid)

def rounds(hp, dm, ar):
    return math.ceil(hp / max(1, (dm-ar)))

def winner(a, b):
    return 0 if rounds(b[0], a[1], b[2]) <= rounds(a[0], b[1], a[2]) else 1

def day21():
    return (reduce(lambda a,b: (a[0]+b[0], a[1]+b[1], a[2]+b[2]), chain(w, a, r), (0, 0, 0))
            for wc in range(1, 1+1) for w in combinations(WEAPON, wc)
            for ac in range(0, 1+1) for a in combinations(ARMOR, ac)
            for rc in range(0, 2+1) for r in combinations(RING, rc))

def day21a(hp, boss): return reduce(min, (pr for (pr, dm, ar) in day21() if winner((hp, dm, ar), boss) == 0), 2**32)
def day21b(hp, boss): return reduce(max, (pr for (pr, dm, ar) in day21() if winner((hp, dm, ar), boss) == 1), 0)

def test_21_ex1(): assert rounds(12, 5, 2) == 4
def test_21_ex2(): assert rounds( 8, 7, 5) == 4

def test_21_ex3(): assert winner((8, 5, 5), (12, 7, 2)) == 0

def test_21a(day21_grid): assert day21a(100, parse(day21_grid)) == 78
def test_21b(day21_grid): assert day21b(100, parse(day21_grid)) == 148
