import re

import pytest

class BaseLightGrid(object):
    def __init__(self):
        self.grid = [ [0] * 1000 for _ in range(1000) ]

    def __len__(self):
        return sum(sum(row) for row in self.grid)

    def turn_on_rect(self, y1, x1, y2, x2):
        for y in range(y1, y2+1):
            for x in range(x1, x2+1):
                self.turn_on(y, x)
        return self

    def turn_off_rect(self, y1, x1, y2, x2):
        for y in range(y1, y2+1):
            for x in range(x1, x2+1):
                self.turn_off(y, x)
        return self

    def toggle_rect(self, y1, x1, y2, x2):
        for y in range(y1, y2+1):
            for x in range(x1, x2+1):
                self.toggle(y, x)
        return self

    def execute(self, lines):
        parsers = [
            (self.turn_on_rect,  r'^turn on (\d+),(\d+) through (\d+),(\d+)$'),
            (self.turn_off_rect, r'^turn off (\d+),(\d+) through (\d+),(\d+)$'),
            (self.toggle_rect,   r'^toggle (\d+),(\d+) through (\d+),(\d+)$')
        ]
        for line in lines:
            for (func, regex) in parsers:
                match = re.match(regex, line)
                if not match:
                    continue
                func(*[ int(v) for v in match.groups() ])
        return self

class LightGrid1(BaseLightGrid):
    def turn_on(self, y, x):
        self.grid[y][x] = 1

    def turn_off(self, y, x):
        self.grid[y][x] = 0

    def toggle(self, y, x):
        self.grid[y][x] = 1 - self.grid[y][x]

class LightGrid2(BaseLightGrid):
    def turn_on(self, y, x):
        self.grid[y][x] += 1

    def turn_off(self, y, x):
        self.grid[y][x] = max(0, self.grid[y][x] - 1)

    def toggle(self, y, x):
        self.grid[y][x] += 2

grid1 = pytest.fixture(lambda: LightGrid1())
grid2 = pytest.fixture(lambda: LightGrid2())

def test_6a_ex1(grid1):
    assert len(grid1.turn_on_rect(0, 0, 999, 999)) == 1000000

def test_6a_ex2(grid1):
    assert len(grid1.toggle_rect(0, 0, 999, 0)) == 1000

def test_6a_ex3(grid1):
    assert len(grid1
        .turn_on_rect(0, 0, 999, 999)
        .turn_off_rect(499, 499, 500, 500)) == 999996

def test_6b_ex1(grid2):
    assert len(grid2.turn_on_rect(0, 0, 0, 0)) == 1

def test_6b_ex1b(grid2):
    assert len(grid2.toggle_rect(0, 0, 0, 0)) == 2

def test_6b_ex2(grid2):
    assert len(grid2.toggle_rect(0, 0, 999, 999)) == 2000000

def test_6a_answer(grid1, day06_lines):
    assert len(grid1.execute(day06_lines)) == 569999

def test_6b_answer(grid2, day06_lines):
    assert len(grid2.execute(day06_lines)) == 17836115
