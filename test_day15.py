import heapq
import collections
TEST_PATH = [1,1,2,1,3,6,5,1,1,1,5,1,1,3,2,3,2,1,1]

def parse(data):
  grid = {}
  for y, line in enumerate(data):
    for x, cell in enumerate(line.strip()):
      grid[(x,y)] = int(cell)

  gsize = max(y for _,y in grid.keys()) + 1

  def g(point):
    if point in grid:
      return grid[point]

    x,y = point

    v = x // gsize + y // gsize

    x %= gsize
    y %= gsize

    return (((v + grid[(x,y)]) -1) %9) + 1
    

  return g

def neighbours(point, goal):
  x,y = point
  for dx, dy in [(-1,0), (1,0), (0,1),(0,-1)]:
    if x + dx >= 0 and y + dy >= 0 and x + dx <= goal[0] and y + dy <= goal[1]:
      yield (x+dx, y+dy)


def shortest_path(dims, grid, goal=(9,9)):
  min_dist = collections.defaultdict(lambda: 999999)
  unvisited = { (x,y) for y in range(dims) for x in range(dims) }

  min_dist[(0,0)] = 0

  heap = []
  for key, value in min_dist.items():
    heapq.heappush(heap, (value, key))

  while len(unvisited) != 0:
    _, nxt = heapq.heappop(heap)

    if nxt not in unvisited:
      continue

    score = min_dist[nxt]

    unvisited.remove(nxt)
    
    for n in neighbours(nxt, goal):
      if n in unvisited:
        min_dist[n] = min(min_dist[n], min_dist[nxt] + grid(n))
        heapq.heappush(heap, (min_dist[n], n))
 
  return min_dist[goal]

def test_part0():
  with open("input15-test.txt") as data:
      grid = parse(data)

  assert sum(TEST_PATH[1:]) == 40

  assert shortest_path(10, grid) == sum(TEST_PATH[1:])


def test_part1():
  with open("input15.txt") as data:
      grid = parse(data)

  assert shortest_path(100, grid, goal=(99,99)) == 583


def test_part00():
  with open("input15-test.txt") as data:
      grid = parse(data)

  assert [1,1,6,3,7,5,1,7,4,2,2,2,7,4,8,6] == [ grid((x, 0)) for x in range(16) ]
  assert [1,1,2,3,7,1,1,3,1,2,2,2,3,4,8,2] == [ grid((0, y)) for y in range(16) ]

  assert shortest_path(50, grid, goal=(49,49)) == 315

def test_part2():
  with open("input15.txt") as data:
      grid = parse(data)

  assert shortest_path(500, grid, goal=(499,499)) == 2927
