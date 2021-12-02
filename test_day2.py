import io

def test_part0():
  data = """forward 5
down 5
forward 8
up 3
down 8
forward 2"""

  data = io.StringIO(data)

  horizontal_position = 0
  depth = 0

  for line in data.readlines():
    direction, size = line.split(" ")

    if direction == "forward":
      horizontal_position += int(size)
    elif direction == "down":
      depth += int(size)
    elif direction == "up":
      depth -= int(size)
    else:
      assert False
  
  assert horizontal_position * depth == 150
    
def test_part1():

  with open("input2.txt", "r") as data:

    horizontal_position = 0
    depth = 0

    for line in data.readlines():
      direction, size = line.split(" ")

      if direction == "forward":
        horizontal_position += int(size)
      elif direction == "down":
        depth += int(size)
      elif direction == "up":
        depth -= int(size)
      else:
        assert False
    
    assert horizontal_position * depth == 1604850
    
def test_part00():
  data = """forward 5
down 5
forward 8
up 3
down 8
forward 2"""

  data = io.StringIO(data)

  horizontal_position = 0
  aim = 0
  depth = 0

  for line in data.readlines():
    direction, size = line.split(" ")

    if direction == "forward":
      horizontal_position += int(size)
      depth += aim * int(size)
    elif direction == "down":
      aim += int(size)
    elif direction == "up":
      aim -= int(size)
    else:
      assert False
  
  assert horizontal_position * depth == 900

def test_part2():

  with open("input2.txt", "r") as data:
    horizontal_position = 0
    aim = 0
    depth = 0

    for line in data.readlines():
      direction, size = line.split(" ")

      if direction == "forward":
        horizontal_position += int(size)
        depth += aim * int(size)
      elif direction == "down":
        aim += int(size)
      elif direction == "up":
        aim -= int(size)
      else:
        assert False
    
    assert horizontal_position * depth == 1685186100
