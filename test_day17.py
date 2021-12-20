import itertools 
TEST_TARGET = ((20,30), (-10, -5))

TARGET = ((211,232), (-124,-69))

def x_steps(xvel):
  x = 0

  while True:
    yield x
    x += xvel
    if xvel < 0:
      xvel += 1
    elif xvel > 0:
      xvel -= 1
     

def y_steps(yvel):
  y = 0
  
  while True:
    yield y
    y += yvel
    yvel -= 1  

def test_part0():
  (xmin, xmax), (ymin, ymax) = TEST_TARGET


  #assert max(y for x,y in zip(x_steps(7), y_steps(9))) == 45

  my = 0
  hits = 0
  for xvel, yvel in itertools.product(range(100), range(-100,100)):
    this_maxy = 0
    hit = False
    for x,y in zip(x_steps(xvel), y_steps(yvel)):
      this_maxy = max(this_maxy, y) 
      if x >= xmin and x <= xmax and y >= ymin and y <= ymax:
        hit = True 
        break
      if x >= xmax:
        break
      if y <= ymin:
        break
    if hit:
      my = max(my, this_maxy)
      hits += 1
    

  assert 45 == my
  assert hits == 112

    


def test_part1():
  (xmin, xmax), (ymin, ymax) = TARGET

  my = 0
  hits = 0
  for xvel, yvel in itertools.product(range(300), range(-200,1000)):
    this_maxy = 0
    hit = False
    for x,y in zip(x_steps(xvel), y_steps(yvel)):
      this_maxy = max(this_maxy, y) 
      if x >= xmin and x <= xmax and y >= ymin and y <= ymax:
        hit = True 
        break
      if x > xmax:
        break
      if y < ymin:
        break
    if hit:
      my = max(my, this_maxy)
      hits += 1
    

  assert 7626 == my
  assert hits == 0

    
