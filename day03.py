def walk_route(route, c):
    D = { '^': (+1, 0), '>': (0, +1), 'v': (-1, 0), '<': (0, -1) }
    y, x = (0, 0)
    c[y, x] = c.get((y, x), 0) + 1
    for step in route:
        dy, dx = D[step]
        y += dy
        x += dx
        c[y, x] = c.get((y, x), 0) + 1
    return c

def count_houses(route):
    c = walk_route(route, {})
    return len(c)

def count_houses_with_robot(route):
    c = {}
    walk_route(route[0::2], c)
    walk_route(route[1::2], c)
    return len(c)

def test_3a_ex1(): assert count_houses('>') == 2
def test_3a_ex2(): assert count_houses('^>v<') == 4
def test_3a_ex3(): assert count_houses('^v^v^v^v^v') == 2

def test_3b_ex1(): assert count_houses_with_robot('^v') == 3
def test_3b_ex2(): assert count_houses_with_robot('^>v<') == 3
def test_3b_ex3(): assert count_houses_with_robot('^v^v^v^v^v') == 11

def test_3a_answer(day03_text): assert count_houses(day03_text) == 2565
def test_3b_answer(day03_text): assert count_houses_with_robot(day03_text) == 2639
