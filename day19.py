import re
from functools import reduce
from itertools import groupby

def parse(lines):
    return ({m[1][::-1]: m[0][::-1] for m in (re.match_groups(r'(\w+) => (\w+)', line) for line in lines[:-2])},
            lines[-1][::-1])

def replace_all(s, src, tgt):
    s = s.split(src)
    return [src.join(s[:i]) + tgt + src.join(s[i:]) for i in range(1, len(s))]

def day19a(rules, molecule):
    return {rep for (tgt, src) in rules.items()
                for rep in replace_all(molecule[::-1], src, tgt)}

def day19b(end, rules, molecule):
    #import pudb ; pudb.set_trace()
    #print(molecule)
    if end == molecule:
        return 0
    else:
        predecessor = re.sub('|'.join(sorted(rules, key=len, reverse=1)), lambda m: rules[m.group()], molecule, count=1)
        if molecule == predecessor:
            import pudb ; pudb.set_trace()
            raise Exception(f"Could not find predecessor for {molecule!r}")
        return 1 + day19b(end, rules, predecessor)

def test_19_replace1(): assert [*replace_all('fooXbarXspam', 'X', '_')] == ['foo_barXspam', 'fooXbar_spam']
def test_19_replace2(): assert [*replace_all('XfoobarXspam', 'X', '_')] == ['_foobarXspam', 'Xfoobar_spam']
def test_19_replace3(): assert [*replace_all('fooXbarspamX', 'X', '_')] == ['foo_barspamX', 'fooXbarspam_']

EX19A = ['H => HO', 'H => OH', 'O => HH', '']
EX19B = ['e => H', 'e => O', 'H => HO', 'H => OH', 'O => HH', '']

def test_19a_ex1(): assert len(day19a(*parse(EX19A+['HOH'])))    == 4
def test_19a_ex2(): assert len(day19a(*parse(EX19A+['HOHOHO']))) == 7

#def test_19b_ex1(): assert reactions('e', *parse(EX19B+['HOH']))    == 3
#def test_19b_ex2(): assert reactions('e', *parse(EX19B+['HOHOHO'])) == 6

#def test_19a(day19_lines): assert len(day19a(*parse(day19_lines))) == 518
def test_19b(day19_lines): assert day19b('e', *parse(day19_lines)) == 200
