import re

def parse(line):
    match = re.match(r'^\w+ can fly (\d+) km/s for (\d+) seconds, but then must rest for (\d+) seconds.$', line)
    if not match:
        raise ValueError(line)
    return tuple(int(v) for v in match.groups())

def distance(t, v, f, r):
    return t // (f+r) * (v*f) + min(f, t % (f+r)) * v

def best_distance(reindeers, time):    
    return max(distance(time, v, f, r) for (v, f, r) in (parse(reindeer) for reindeer in reindeers))

def best_score(reindeers, time):
    scores = [0] * len(reindeers)
    speeds = [ parse(reindeer) for reindeer in reindeers ]
    for t in range(1, time):
        distances = [ distance(t, v, f, r) for (v, f, r) in speeds ]
        lead_dist = max(distances)
        scores = [ score + (dist == lead_dist) for (score, dist) in zip(scores, distances) ]
    return max(scores)

EX14 = [
    'Comet can fly 14 km/s for 10 seconds, but then must rest for 127 seconds.',
    'Dancer can fly 16 km/s for 11 seconds, but then must rest for 162 seconds.'
]

def test_14a_ex1(): assert best_distance(EX14, 1000) == 1120
def test_14b_ex1(): assert best_score(EX14, 1000) == 689

def test_14a_answer(day14_lines): assert best_distance(day14_lines, 2503) == 2640
def test_14b_answer(day14_lines): assert best_score(day14_lines, 2503) == 1102
