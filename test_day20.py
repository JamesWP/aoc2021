import itertools

def parse(data):
    algo = next(data).strip()

    next(data)
    assert len(algo) == 512

    grid = {}

    for row, line in enumerate(data):
        for col, cell in enumerate(line.strip()):
            grid[(col, row)] = cell == '#'

    return grid, algo

def neighbours(pos):
    x,y = pos
    coords = itertools.product(range(-1,2), range(-1, 2))
    yield from ((x + dx, y + dy) for dy, dx in coords)


def test_neighbours():
    assert len(list(neighbours((0,0)))) == 9

def test_parse():
    with open("input20-test.txt") as data:
        parse(data)
    with open("input20.txt") as data:
        parse(data)

def coords(grid):
    xmin = min(x for x,_ in grid.keys())
    xmax = max(x for x,_ in grid.keys())
    ymin = min(y for _,y in grid.keys())
    ymax = max(y for _,y in grid.keys())

    xcoords = range(xmin -2, xmax + 3)
    ycoords = range(ymin -2, ymax + 3)

    yield from itertools.product(xcoords, ycoords)

def apply_algo(algo, nums):
    num = sum(1<<(8-place) for place, n in enumerate(nums) if n)
    return algo[num] == '#'

def test_apply_algo():
    nums = [i == 1 for i in [0,0,0,1,0,0,0,1,0]]
    algo = "..#.#..#####.#.#.#.###.##.....###.##.#..###.####..#####..#....#..#..##..##"

    assert apply_algo(algo, nums)

def print_grid(grid, background = False):
    lasty = 0
    for y, x in coords(grid):
        if y != lasty:
            print()
        if grid.get((x,y), background):
            print("#", end="")
        else:
            print(".", end="")
        lasty = y

def enhance(grid, algo, backgroud = False):
    new_grid = {}
    for y, x in coords(grid):
        pos = x,y
        nums = list(grid.get(n, backgroud) for n in neighbours(pos))

        new_grid[pos] = apply_algo(algo, nums)

    return new_grid

def test_part0():
    with open("input20-test.txt") as data:
        grid, algo = parse(data)

    print_grid(grid)
    grid = enhance(grid, algo)
    print_grid(grid)
    grid = enhance(grid, algo)
    print_grid(grid)

    assert sum(1 for pos in grid.values() if pos) == 35

def test_part1():
    background = False
    
    with open("input20.txt") as data:
        grid, algo = parse(data)

    #print_grid(grid, background)
    grid = enhance(grid, algo, background)
    background = apply_algo(algo, [background] * 9)
    #print_grid(grid, background)
    grid = enhance(grid, algo, background)
    background = apply_algo(algo, [background] * 9)
    #print_grid(grid, background)

    assert sum(1 for pos in grid.values() if pos) == 5259

def test_part00():
    with open("input20-test.txt") as data:
        grid, algo = parse(data)

    for _ in range(50):
        #print_grid(grid)
        grid = enhance(grid, algo)

    assert sum(1 for pos in grid.values() if pos) == 3351

def test_part2():
    with open("input20.txt") as data:
        grid, algo = parse(data)

    background = False

    for _ in range(50):
        grid = enhance(grid, algo, background)
        background = apply_algo(algo, [background] * 9)

    assert sum(1 for pos in grid.values() if pos) == 15287