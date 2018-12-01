import re
from functools import reduce

def p(s): return [int(x) for x in re.findall(r'\d+', s)]

def N(y, x): return x + (x+y-1) * (x+y-2) // 2

def f(y, x): return reduce(lambda a,_: a * 252533 % 33554393, range(N(y, x)-1), 20151125)

def test_25_ex1a(): assert N(1, 1) == 1
def test_25_ex1b(): assert N(6, 1) == 16
def test_25_ex1c(): assert N(3, 4) == 19
def test_25_ex1d(): assert N(1, 6) == 21

def test_25_ex2a(): assert f(1, 1) == 20151125
def test_25_ex2b(): assert f(6, 6) == 27995004

def test_25(day25_text): assert f(*p(day25_text)) == 9132360
