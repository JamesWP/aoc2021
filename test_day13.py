

def parse(data):
  grid = set()
  for line in data:
    if len(line.strip()) == 0:
      break
    x,y = [int(v) for v in line.split(",")]
    grid.add((x,y))

  folds = []
  for line in data:
    f = line.split(" ")[2] 
    a, v = f.split("=")
    folds.append((a, int(v)))

  return grid, folds
  
def test_parse():
  with open("input13-test.txt") as f:
    grid, folds = parse(f)

  assert len(grid) == 18
  assert len(folds) == 2  

  assert folds == [('y', 7), ('x', 5)]

def test_part0():
  with open("input13-test.txt") as f:
    grid, folds = parse(f)
 
  grid = { fold_value(p, [folds[0]]) for p in grid }
  assert len(grid) == 17
   
def test_part1():
  with open("input13.txt") as f:
    grid, folds = parse(f)
 
  grid = { fold_value(p, [folds[0]]) for p in grid }
  assert len(grid) == 684

def test_part00():
  with open("input13-test.txt") as f:
    grid, folds = parse(f)
 
  grid = { fold_value(p, folds) for p in grid }
  assert len(grid) == 16
   
def test_part2():
  with open("input13.txt") as f:
    grid, folds = parse(f)
 
  grid = { fold_value(p, folds) for p in grid }

  print()
  for row in range(20):
    for col in range(120):
      if (col, row) in grid:
        print("#", sep="", end="")
      else:
        print(" ", sep="", end="")
    print()

  return grid 

def fold_value(c, folds):
  x, y = c
  for fd, fv in folds:
    if fd == 'x' and x > fv:
      x = (-(x - fv) + fv)
    if fd == 'y' and y > fv:
      y = (-(y - fv) + fv)
      
  return (x, y)
