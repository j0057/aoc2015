import re

def is_nice(s):
    if len(re.findall(r'([aeiou])', s)) < 3:
        return False
    if not re.search(r'(.)\1', s):
        return False
    if re.search(r'(ab|cd|pq|xy)', s):
        return False
    return True

def count_nice(lines):
    return sum(1 for line in lines if is_nice(line))

def is_new_nice(s):
    if not re.search(r'(..).*\1', s):
        return False
    if not re.search(r'(.).\1', s):
        return False
    return True

def count_new_nice(lines):
    return sum(1 for line in lines if is_new_nice(line))

def test_5a_ex1(): assert is_nice('ugknbfddgicrmopn')
def test_5a_ex2(): assert is_nice('aaa')
def test_5a_ex3(): assert not is_nice('jchzalrnumimnmhp')
def test_5a_ex4(): assert not is_nice('haegwjzuvuyypxyu')
def test_5a_ex5(): assert not is_nice('dvszwmarrgswjxmb')

def test_5b_ex1(): assert is_new_nice('qjhvhtzxzqqjkmpb')
def test_5b_ex2(): assert is_new_nice('xxyxx')
def test_5b_ex3(): assert not is_new_nice('uurcxstgmygtbstg')
def test_5b_ex4(): assert not is_new_nice('ieodomkazucvgmuy')

def test_5a_answer(day05_lines): assert count_nice(day05_lines) == 238
def test_5b_answer(day05_lines): assert count_new_nice(day05_lines) == 69
