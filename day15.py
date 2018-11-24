import re
from functools import reduce

def parse(lines):
    return [[int(v) for v in re.findall(r'-?\d+', line)] for line in lines]

def day15(ing, n, scores, ok):
    if ing:
        return reduce(max, [day15(ing[1:], n-c, [a+b for (a,b) in zip(scores, [i*c for i in ing[0]])], ok)
                            for c in range(0 if ing[1:] else n, n+1)], 1)
    else:
        return reduce(lambda a,b: a*b, [max(0, score) for score in scores[:-1]], 1) * ok(scores)

def day15a(ing): return day15(ing, 100, [0]*5, lambda scores: True)
def day15b(ing): return day15(ing, 100, [0]*5, lambda scores: scores[-1] == 500)

EX15 = ['Butterscotch: capacity -1, durability -2, flavor 6, texture 3, calories 8',
        'Cinnamon: capacity 2, durability 3, flavor -2, texture -1, calories 3']

def test_15a_parse(): assert parse(EX15) == [[-1, -2, 6, 3, 8], [2, 3, -2, -1, 3]]

def test_15a_ex(): assert day15a(parse(EX15)) == 62842880
def test_15b_ex(): assert day15b(parse(EX15)) == 57600000

def test_15a_answer(day15_lines): assert day15a(parse(day15_lines)) == 18965440
def test_15b_answer(day15_lines): assert day15b(parse(day15_lines)) == 15862900
