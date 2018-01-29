"""
Classes for representing a Life grid. Currently two algorithms are implemented,
a 'correct' one (L{SimpleLifeGrid}) and a faster one (L{UnrolledLifeGrid}).

@version: 1.0
@author: Joost Molenaar
@contact: j.j.molenaar at gmail dot com
@license: Copyright(c)2005 Joost Molenaar
"""

class LifeGrid:
    """Base class for representing a life grid.

    @version: 1.0
    @author: Joost Molenaar
    @contact: j.j.molenaar at gmail dot com
    @license: Copyright(c)2005 Joost Molenaar
    """
    def __init__(self, size):
        """Initialize LifeGrid instance.
        @param size: Number of cells in each side of the life grid.
        @type size: int
        """
        if size < 3:
            raise Exception("Size %d? Go away." % (size,))
        self.size = size
        
    def EmptyGrid(self):
        """Create an empty life grid.
        @return: List of list of 0's
        @rtype: list
        """
        return [ [ 0 for w in range(self.size) ] for h in range(self.size) ]
    
    def Put(self, x, y, value):
        """Put a value at a certain x,y coordinate.
        @param x: X coordinate
        @param y: Y coordinate
        @type x: int
        @type y: int
        """
        self.grid[y][x] = value
    
    def Get(self, x, y):
        """Return the value of a certain x,y coordinate.
        @param x: X coordinate
        @param y: Y coordinate
        @type x: int
        @type y: int
        @return Value of coordinate
        @rtype int
        """
        return self.grid[y][x]

class SimpleLifeGrid(LifeGrid):
    """Life grid that is readable and correct but not excessively fast.

    Speed of a 70x70 grid::
    non-localized: 8 fps
    localized: 10 fps

    @version: 1.0
    @author: Joost Molenaar
    @contact: j.j.molenaar at gmail dot com
    @license: Copyright(c)2005 Joost Molenaar
    """
    def __init__(self, size, survival=[2,3], birth=[3]):
        """Initialize SimpleLifeGrid instance.
        @param size: Size of grid
        @param survival: Number of neighbours required for survival.
        @param birth: Number of neighbours required for birth.
        @type size: int
        @type survival: list of int
        @type birth: list of int
        """
        LifeGrid.__init__(self, size)
        self.survival = survival
        self.birth = birth
        self.Reset()

    def Reset(self):
        """Reset SimpleLifeGrid instance to initial state.
        """
        self.grid = self.EmptyGrid()
        self.count = self.EmptyGrid()

    def CountNeighbours(self):
        """Fill C{self.count} grid with number of neighbours of each cell."""
        idx = lambda c: -int(c==0) + int(c==self.size-1)
        deltas = { -1:[0, 1], 0:[-1, 0, 1], 1:[-1, 0] }
        ## localize instance vars local for speed (gains +1 fps)
        size = self.size
        grid = self.grid
        count = self.count
        ## #
        for y in xrange(size):
            for x in xrange(size):
                count[y][x] = 0
                vertical = deltas[idx(y)]
                horizontal = deltas[idx(x)]
                for dy in vertical:
                    for dx in horizontal:
                        if (dy != 0) or (dx != 0):
                            count[y][x] += grid[y+dy][x+dx]

    def Iterate(self):
        """Advance the life grid by one iteration."""
        self.CountNeighbours()
        ## localize instance vars for speed (gains +1 fps)
        size = self.size
        survival = self.survival
        birth = self.birth
        grid = self.grid
        count = self.count
        ## #
        for y in xrange(size):
            for x in xrange(size):
                if grid[y][x] == 1:
                    if count[y][x] not in survival:
                        grid[y][x] = 0
                elif grid[y][x] == 0:
                    if count[y][x] in birth:
                        grid[y][x] = 1

# --- new code from here ---

xrange = range # the one Py3 hack needed to get the 2.4 code running :-)

def parse(lines):
    grid = SimpleLifeGrid(len(lines))
    grid.grid = [ [ 0 if ch == '.' else 1 for ch in line ] for line in lines ]
    return grid

def game_of_lights(grid, hack_on=0):
    while True:
        if hack_on: grid.grid[0][0] = grid.grid[0][-1] = grid.grid[-1][0] = grid.grid[-1][-1] = 1
        grid.Iterate()
        if hack_on: grid.grid[0][0] = grid.grid[0][-1] = grid.grid[-1][0] = grid.grid[-1][-1] = 1
        yield sum(sum(row) for row in grid.grid)

def iterate(g, n):
    for _ in range(n):
        r = next(g)
    return r

EX18 = [ '.#.#.#', '...##.', '#....#', '..#...', '#.#..#', '####..' ]

def test_18a_ex(): assert iterate(game_of_lights(parse(EX18), hack_on=0), 4) == 4
def test_18b_ex(): assert iterate(game_of_lights(parse(EX18), hack_on=1), 5) == 17

def test_18a_answer(day18_lines): assert iterate(game_of_lights(parse(day18_lines), hack_on=0), 100) == 814
def test_18b_answer(day18_lines): assert iterate(game_of_lights(parse(day18_lines), hack_on=1), 100) == 924
