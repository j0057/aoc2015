
def parse(s):
    return [ int(d) for d in s.split('x') ]

def calc_paper_area(dimensions):
    l, w, h = parse(dimensions)
    surfaces =  [ l * w, w * h, h * l ]
    return 2 * sum(surfaces) + min(surfaces)

def calc_paper_areas(dimension_lines):
    return sum(calc_paper_area(d) for d in dimension_lines)

def calc_ribbon_length(dimensions):
    d1, d2, d3 = sorted(parse(dimensions))
    return 2 * d1 + 2 * d2 + d1 * d2 * d3

def calc_ribbon_lengths(dimension_lines):
    return sum(calc_ribbon_length(d) for d in dimension_lines)

def test_2a_ex1(): assert calc_paper_area('2x3x4') == 58
def test_2a_ex2(): assert calc_paper_area('1x1x10') == 43

def test_2b_ex1(): assert calc_ribbon_length('2x3x4') == 34
def test_2b_ex2(): assert calc_ribbon_length('1x1x10') == 14

def test_2a_answer(day02_lines): assert calc_paper_areas(day02_lines) == 1598415
def test_2b_answer(day02_lines): assert calc_ribbon_lengths(day02_lines) == 3812909
