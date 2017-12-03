
def find_floor(s):
    D = { '(': +1, ')': -1 }
    return sum(D[ch] for ch in s)

def find_basement(s):
    D = { '(': +1, ')': -1 }
    f = 0
    for (i, ch) in enumerate(s):
        f += D[ch]
        if f < 0:
            return i + 1
    raise Exception('Does not enter basement')

def test_1a_ex1a(): assert find_floor('(())') == 0
def test_1a_ex1b(): assert find_floor('()()') == 0
def test_1a_ex2a(): assert find_floor('(((') == 3
def test_1a_ex2b(): assert find_floor('(()(()(') == 3
def test_1a_ex3():  assert find_floor('))(((((') == 3
def test_1a_ex4a(): assert find_floor('())') == -1
def test_1a_ex4b(): assert find_floor('))(') == -1
def test_1a_ex5a(): assert find_floor(')))') == -3
def test_1a_ex5b(): assert find_floor(')())())') == -3

def test_1a_ex1(): assert find_basement(')') == 1
def test_1a_ex2(): assert find_basement('()())') == 5

def test_1a_answer(day01): assert find_floor(day01) == 232
def test_1b_answer(day01): assert find_basement(day01) == 1783
