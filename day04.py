
from itertools import count
from hashlib import md5

def mine_advent_coin(key, difficulty):
    for v in count():
        digest = md5('{0}{1}'.format(key, v).encode('ascii')).hexdigest()
        if digest.startswith('0' * difficulty):
            return v

def test_4a_ex1(): assert mine_advent_coin('abcdef', 5) == 609043
def test_4a_ex2(): assert mine_advent_coin('pqrstuv', 5) == 1048970

def test_4a_answer(day04_text): assert mine_advent_coin(day04_text, 5) == 254575
def test_4b_answer(day04_text): assert mine_advent_coin(day04_text, 6) == 1038736
