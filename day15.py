import re

def parse(line):
    return [int(v) for v in re.findall(r'\d+', line)]
    [ (-1, -2,  6,  3, 8]), ( 2,  3, -2, -1, 3) ]
    [ 44                  , 56                  ]

def best_cookie(ingredients):
    ingredients = [parse(ingredient) for ingredient in ingredients]
    for a in range(0, 100+1):
        for b in range(0, 100-a+1):
            for c in range(0, 100-a-b+1):
                for d in range(0, 100-a-b-c+1):
                    if a+b+c+d < 100:
                        continue
                    
                

def test_15a_ex1():
    assert best_cookie([
        'Butterscotch: capacity -1, durability -2, flavor 6, texture 3, calories 8',
        'Cinnamon: capacity 2, durability 3, flavor -2, texture -1, calories 3'
    ]) == 62842880
