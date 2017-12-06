
def look_and_say(s):
    def look_and_say_gen(s):
        i, j = 0, 0
        while i < len(s):
            if s[i] != s[j]:
                yield '{0}{1}'.format(i-j, s[j])
                j = i
            i += 1
        yield '{0}{1}'.format(i-j, s[j])
    return ''.join(look_and_say_gen(s))

def look_and_say_a_lot(s, n):
    for _ in range(n):
        s = look_and_say(s)
    return len(s)

def test_10_ex1(): assert look_and_say('1') == '11'
def test_10_ex2(): assert look_and_say('11') == '21'
def test_10_ex3(): assert look_and_say('21') == '1211'
def test_10_ex4(): assert look_and_say('1211') == '111221'
def test_10_ex5(): assert look_and_say('111221') == '312211'

def test_10_answer(day10): assert look_and_say_a_lot(day10, 40) == 329356
def test_10_answer(day10): assert look_and_say_a_lot(day10, 50) == 4666278
