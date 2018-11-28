from collections import namedtuple
from functools import reduce
from itertools import chain

class State(namedtuple('State', 'turn player_hp player_armor player_mana player_cast boss_hp boss_dmg '
                                'shield_effect poison_effect recharge_effect difficulty')):

    def player_won(self):
        return self.boss_hp <= 0

    def boss_won(self):
        return self.player_hp <= 0 or self.player_mana - self.player_cast < 53

    @property
    def player_charge(self):
        return self.player_mana - self.player_cast

    def get_actions(self):
        if self.turn & 1:
            yield 'attack'
        else:
            if self.player_charge >= 53: yield 'magic_missile'
            if self.player_charge >= 73: yield 'drain'
            if self.player_charge >= 113 and not self.shield_effect: yield 'shield'
            if self.player_charge >= 173 and not self.poison_effect: yield 'poison'
            if self.player_charge >= 229 and not self.recharge_effect: yield 'recharge'

    def attack(self):
        return self._replace(player_hp=self.player_hp - self.boss_dmg + self.player_armor)

    def magic_missile(self):
        return self._replace(player_cast=self.player_cast + 53, boss_hp=self.boss_hp - 4)

    def drain(self):
        return self._replace(player_cast=self.player_cast + 73, player_hp=self.player_hp + 2, boss_hp=self.boss_hp - 2)

    def shield(self):
        return self._replace(player_cast=self.player_cast + 113, shield_effect=6)

    def poison(self):
        return self._replace(player_cast=self.player_cast + 173, poison_effect=6)

    def recharge(self):
        return self._replace(player_cast=self.player_cast + 229, recharge_effect=5)

    def next_turn(self):
        return self._replace(turn=self.turn + 1,
                             player_hp=self.player_hp-(self.difficulty if self.turn & 1 else 0),
                             player_armor=7 if self.shield_effect else 0,
                             boss_hp=self.boss_hp-(3 if self.poison_effect else 0),
                             player_mana=self.player_mana+(101 if self.recharge_effect else 0),
                             shield_effect=max(0, self.shield_effect - 1),
                             poison_effect=max(0, self.poison_effect - 1),
                             recharge_effect=max(0, self.recharge_effect - 1))

    def do(self, action):
        return getattr(self, action)().next_turn()

def parse(grid):
    return tuple(int(row[-1]) for row in grid)

def day22(state, best):
    if state.player_won():
        return state.player_cast
    elif state.boss_won():
        return 2**64
    elif state.player_cast > best:
        return 2**64
    else:
        for action in state.get_actions():
            result = day22(state.do(action), best)
            best = min(best, result)
        return best

def day22a(player_hp, player_mana, boss_hp, boss_dmg):
    return day22(State(0, player_hp, 0, player_mana, 0, boss_hp, boss_dmg, 0, 0, 0, 0), 2**64)

def day22b(player_hp, player_mana, boss_hp, boss_dmg):
    return day22(State(0, player_hp, 0, player_mana, 0, boss_hp, boss_dmg, 0, 0, 0, 1), 2**64)

def test_22a_ex1():
    state = reduce(lambda s, a: s.do(a),
        'poison attack magic_missile'.split(),
        State(0, 10, 0, 250, 0, 13, 8, 0, 0, 0, 0))
    assert state.boss_hp == 0
    assert state.player_hp == 2
    assert state.player_cast == 173+53

def test_22a_ex2():
    state = reduce(lambda s, a: s.do(a),
        'recharge attack shield attack drain attack poison attack magic_missile'.split(),
        State(0, 10, 0, 250, 0, 14, 8, 0, 0, 0, 0))
    assert state.boss_hp == -1
    assert state.player_hp == 1
    assert state.player_cast == 229+113+73+173+53

def test_22a(day22_grid): assert day22a(50, 500, *parse(day22_grid)) == 900
def test_22b(day22_grid): assert day22b(49, 500, *parse(day22_grid)) == 1216
