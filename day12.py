import json

def obj_numbers(obj, ignore=None):
    if isinstance(obj, list):
        yield from (n for o in obj for n in obj_numbers(o, ignore=ignore))

    elif isinstance(obj, dict):
        if ignore is None or ignore not in obj.values():
            yield from (n 
                        for o in obj.values()
                        for n in obj_numbers(o, ignore=ignore))

    elif isinstance(obj, int):
        yield obj

def json_sum(s):
    return sum(obj_numbers(json.loads(s)))

def json_sum_no_red(s):
    return sum(obj_numbers(json.loads(s), ignore="red"))

def test_12a_ex1a(): assert json_sum('[1,2,3]') == 6
def test_12a_ex1b(): assert json_sum('{"a":2,"b":4}') == 6
def test_12a_ex2a(): assert json_sum('[[[3]]]') == 3
def test_12a_ex2b(): assert json_sum('{"a":{"b":4},"c":-1}') == 3
def test_12a_ex3a(): assert json_sum('{"a":[-1,1]}') == 0
def test_12a_ex3b(): assert json_sum('[-1,{"a":1}]') == 0
def test_12a_ex4a(): assert json_sum('[]') == 0
def test_12a_ex4a(): assert json_sum('{}') == 0

def test_12b_ex2(): assert json_sum_no_red('[1,{"c":"red","b":2},3]') == 4

def test_12a_answer(day12): assert json_sum(day12) == 156366
def test_12b_answer(day12): assert json_sum_no_red(day12) == 96852
