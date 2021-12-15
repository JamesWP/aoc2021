import io

def test_transcibe():
  with open("input11.txt") as f:
    data = f.read()

  s = 0 
  for line in data.strip().split("\n"):
    s += int(line)

  assert s == 51642421519

def neighbour(grid,x,y):
  for dx, dy in ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1),(1,1), (1, 0), (1, -1)):
    xx = x + dx
    yy = y + dy

    if xx >= 0 and yy >= 0 and xx < len(grid[0]) and yy < len(grid):
      yield (xx,yy)

def test_neighbour():
  grid = [[0,0,0],[0,0,0], [0,0,0]]
  assert len(list(neighbour(grid, 0,0))) == 3

def step(energy_levels):
  #First, the energy level of each octopus increases by 1.

  flashing = []
  #Then, any octopus with an energy level greater than 9 flashes. 
  for y, row in enumerate(energy_levels):
    for x, el in enumerate(row):
      energy_levels[y][x] += 1
      if energy_levels[y][x] == 10:
        flashing.append((x,y))
 
  #This increases the energy level of all adjacent octopuses by 1, including octopuses that are diagonally adjacent. 
  #  If this causes an octopus to have an energy level greater than 9, it also flashes. 
  #This process continues as long as new octopuses keep having their energy level increased beyond 9. 
  #(An octopus can only flash at most once per step.)
  while len(flashing) != 0:
    x, y = flashing.pop()

    for nx, ny in neighbour(energy_levels, x, y):
      energy_levels[ny][nx] += 1
      if energy_levels[ny][nx] == 10:
        flashing.append((nx, ny))
    
  #Finally, any octopus that flashed during this step has its energy level set to 0, as it used all of its energy to flash.
  flashed = 0
  for y, row in enumerate(energy_levels):
    for x, el in enumerate(row):
      if energy_levels[y][x] > 9:
        flashed +=1
        energy_levels[y][x] = 0

  return flashed

TESTS = {
   0: """6594254334
3856965822
6375667284
7252447257
7468496589
5278635756
3287952832
7993992245
5957959665
6394862637
""",
  1: """8807476555
5089087054
8597889608
8485769600
8700908800
6600088989
6800005943
0000007456
9000000876
8700006848
""",
  2: """0050900866
8500800575
9900000039
9700000041
9935080063
7712300000
7911250009
2211130000
0421125000
0021119000
""",
  8: """9060000644
7800000976
6900000080
5840000082
5858000093
6962400000
8021250009
2221130009
9111128097
7911119976
"""
}

TEST_FLASHES = {
  9: 204
}

def format(energy_levels):
  out = io.StringIO()

  for row in energy_levels:
    print(*row, sep="", file=out)

  return out.getvalue()
  

def test_part0():
  with open("input11-test.txt") as f:
    data = f.read()

  energy_levels = []

  for line in data.strip().split("\n"):
    row = []
    for c in line:
      row.append(int(c))
    energy_levels.append(row)

  flashes = 0
  for i in range(100):
    new_flash = step(energy_levels)
    flashes += new_flash
    if i in TEST_FLASHES:
      
      assert flashes == TEST_FLASHES[i]     
    if i in TESTS:
      assert format(energy_levels) == TESTS[i]     
  assert flashes == 1656

def test_part0():
  with open("input11.txt") as f:
    data = f.read()

  energy_levels = []

  for line in data.strip().split("\n"):
    row = []
    for c in line:
      row.append(int(c))
    energy_levels.append(row)

  flashes = 0
  for i in range(100):
    new_flash = step(energy_levels)
    flashes += new_flash
  assert flashes == 1608

def test_part00():
  with open("input11-test.txt") as f:
    data = f.read()

  energy_levels = []

  for line in data.strip().split("\n"):
    row = []
    for c in line:
      row.append(int(c))
    energy_levels.append(row)

  for i in range(1000):
    new_flash = step(energy_levels)
    if new_flash == len(energy_levels) * len(energy_levels[0]):
      break
  assert i+1 == 195 

def test_part2():
  with open("input11.txt") as f:
    data = f.read()

  energy_levels = []

  for line in data.strip().split("\n"):
    row = []
    for c in line:
      row.append(int(c))
    energy_levels.append(row)

  for i in range(1000):
    new_flash = step(energy_levels)
    if new_flash == len(energy_levels) * len(energy_levels[0]):
      break
  assert i+1 == 214

