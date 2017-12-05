def unescape(s):
    def unescape_gen():
        i = 1
        while i < len(s)-1:
            if s[i:i+2] == '\\"':
                yield '"'
                i += 2
            elif s[i:i+2] == '\\\\':
                yield '\\'
                i += 2
            elif s[i:i+2] == '\\x':
                yield chr(int(s[i+2:i+4], 16))
                i += 4
            else:
                yield s[i]
                i += 1
    return ''.join(unescape_gen())

def escape(s):
    escaped = ('\\"' if ch == '"' else
               '\\\\' if ch == '\\' else
               ch if 32 <= ord(ch) < 128 else
               '\\x' + hex(ord(ch))[2:] for ch in s)
    return '"' + ''.join(escaped) + '"'

def count_difference1(lines):
    code = sum(len(s) for s in lines)
    data = sum(len(unescape(s)) for s in lines)
    return code - data

def count_difference2(lines):
    data = sum(len(s) for s in lines)
    code = sum(len(escape(s)) for s in lines)
    return code - data

def test_8a_ex1(): assert unescape('""') == ''
def test_8a_ex2(): assert unescape('"abc"') == 'abc'
def test_8a_ex3(): assert unescape('"aaa\\"aaa"') == 'aaa\"aaa'
def test_8a_ex4(): assert unescape('"\\x27"') == '\x27'

def test_8b_ex1(): assert escape('""') == '"\\"\\""'
def test_8b_ex2(): assert escape('"abc"') == '"\\"abc\\""'
def test_8b_ex3(): assert escape('"aaa\\"aaa"') == '"\\"aaa\\\\\\"aaa\\""'
def test_8b_ex4(): assert escape('"\\x27"') == '"\\"\\\\x27\\""'

def test_8a_answer(day08_lines): assert count_difference1(day08_lines) == 1333
def test_8a_answer(day08_lines): assert count_difference2(day08_lines) == 2046
