import pytest
import numpy

def run(data, use_any):
  numbers = [ int(v) for v in data.readline().split(",") ]
 
  boards =  [ int(v) for v in data.read().split() ]

  numbers = numpy.array(numbers)
  boards = numpy.array(boards)
  boards = numpy.reshape(boards, (-1, 5, 5))

  marked = numpy.full(boards.shape, False, dtype=bool)

  bingos = numpy.zeros(boards.shape[0])

  print(numbers)
  print(boards)
  #print(marked)

  for number in numbers:
    marked |= boards == number
    column_bingos = numpy.sum(numpy.swapaxes(marked, 1,2), 2) == 5
    row_bingos = numpy.sum(marked, 2) == 5
    
    new_bingos = numpy.logical_or(numpy.any(column_bingos, 1), numpy.any(row_bingos,1))

    delta_bingos = new_bingos != bingos

    bingos = new_bingos

    if use_any and numpy.any(bingos):
      break

    if not use_any and numpy.all(bingos):
      break
    

  board_sums = numpy.sum(boards, where=numpy.invert(marked), axis=(1, 2))
  board_sum = numpy.sum(board_sums * delta_bingos)
  print("sum", board_sum)
  print("number", number)
  
  return board_sum * number

def test_part0():
  with open("input4-test.txt", "r") as data:
    assert run(data, True) == 4512

def test_part1():
  with open("input4.txt", "r") as data:
    assert run(data, True) == 8442

def test_part00():
  with open("input4-test.txt", "r") as data:
    assert run(data, False) == 1924

def test_part2():
  with open("input4.txt", "r") as data:
    assert run(data, False) == 4590

