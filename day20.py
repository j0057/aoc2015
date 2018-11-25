from itertools import islice

def day20(N, s, m=None):
    a = [0] * N
    for e in range(1, N):
        for i in islice(range(0, N, e), 0, m):
            a[i] += e * s
    return [0] + a[1:]

def day20a(N, n): return next(i for i,v in enumerate(day20(N, 10))     if v >= n)
def day20b(N, n): return next(i for i,v in enumerate(day20(N, 11, 50)) if v >= n)

def test_20a_ex1(): assert day20(10, 10) == [0, 10, 30, 40, 70, 60, 120, 80, 150, 130]
def test_20a_ex2(): assert day20a(10, 70) == 4

def test_20a(day20_number): assert day20a(day20_number//10, day20_number) == 831600
def test_20b(day20_number): assert day20b(day20_number//10, day20_number) == 884520
