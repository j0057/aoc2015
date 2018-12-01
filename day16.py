import re

def parse(aunt_sues):
    return { int(aunt): { k: int(v) for (k, v) in [ prop.split(': ') for prop in props.split(', ') ] }
             for (aunt, props) in [ re.match(r'^Sue (\d+): (.*)$', aunt_sue).groups() for aunt_sue in aunt_sues ] }

def find_sue(data, aunt_sue_props):
    for (aunt, props) in aunt_sue_props.items():
        for (k, v) in props.items():
            if data[k] != v:
                break
        else:
            return aunt
    raise Exception('Aunt not found')

def real_sue(data, aunt_sue_props):
    for (aunt, props) in aunt_sue_props.items():
        for (k, v) in props.items():
            if k in ['cats', 'trees']:
                if not v > data[k]:
                    break
            elif k in ['pomeranians', 'goldfish']:
                if not v < data[k]:
                    break
            else:
                if data[k] != v:
                    break
        else:
            return aunt
    raise Exception('Aunt not found')

DATA = dict(children=3, cats=7, samoyeds=2, pomeranians=3, akitas=0, vizslas=0, goldfish=5, trees=3, cars=2, perfumes=1)
EX16 = [
    'Sue 1: children: 2, cats: 7, samoyeds: 2, cars: 2, goldfish: 5',
    'Sue 2: children: 3, cats: 7, samoyeds: 2, cars: 2, goldfish: 5',
    'Sue 3: children: 3, cats: 8, samoyeds: 2, cars: 2, goldfish: 3'
]

def test_16a_ex(): assert find_sue(DATA, parse(EX16)) == 2
def test_16b_ex(): assert real_sue(DATA, parse(EX16)) == 3

def test_16a_answer(day16_lines): assert find_sue(DATA, parse(day16_lines)) == 40
def test_16b_answer(day16_lines): assert real_sue(DATA, parse(day16_lines)) == 241
