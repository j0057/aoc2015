ord_word = lambda s: [ ord(c) for c in s ]
chr_word = lambda v: ''.join(chr(c) for c in v)

def is_ok(v):
    if not any(ord(a)+1 == ord(b) and ord(b)+1 == ord(c)
               for (a,b,c) in zip(v, v[1:], v[2:])):
        return False
    if 'i' in v or 'o' in v or 'l' in v:
        return False
    if not any(a1==a2 and b1==b2 and a1!=b1
               for (a1, a2) in zip(v, v[1:])
               for (b1, b2) in zip(v, v[1:])):
        return False
    return True

def add_one(v):
    for i in range(-1, -len(v)-1, -1):
        v[i] = chr(ord(v[i]) + 1)
        if v[i] > 'z':
            v[i] = 'a'
        else:
            break
    
def get_next(s):
    v = list(s)
    while True:
        add_one(v)
        if is_ok(v):
            return ''.join(v)
    raise Exception(s)

def test_11a_ex1(): assert not is_ok('hijklmmn')
def test_11a_ex2(): assert not is_ok('abbceffg')
def test_11a_ex3(): assert not is_ok('abbcegjk')

def test_11a_ex4(): assert get_next('abcdefgh') == 'abcdffaa'
def test_11a_ex5(): assert get_next('ghijklmn') == 'ghjaabcc'

def test_11a_answer(day11_text): assert get_next(day11_text) == 'cqjxxyzz'
def test_11b_answer(day11_text): assert get_next('cqjxxyzz') == 'cqkaabcc'
