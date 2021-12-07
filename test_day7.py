import io
import numpy 
import math

def fuel(numbers, middle):
    return numpy.sum(numpy.absolute(numbers - middle))

def fuel_2(numbers, middle):
    diff = numpy.abs(numbers - middle)
    return numpy.sum(diff * (diff + 1) / 2)

def solve_dumb(data):
  numbers = numpy.array([int(n) for n in data.read().split(",")])

  totals = []
  for x in range(numpy.min(numbers), numpy.max(numbers)+1):
    total = fuel(numbers, x)
    totals.append(total) 

  return numpy.min(numpy.array(totals))

def solve_clever(data):
  numbers = numpy.array([int(n) for n in data.read().split(",")])
  return fuel(numbers, numpy.median(numbers))

def solve_lsq_dumb(data):
  numbers = numpy.array([int(n) for n in data.read().split(",")])

  totals = []
  for x in range(numpy.min(numbers), numpy.max(numbers)+1):
    total = fuel_2(numbers, x)
    totals.append(total) 

  return numpy.min(numpy.array(totals))

def chop_range(fn, rge):
    begin, end = rge

    if fn(begin)<fn(end):        
        mid = (end - begin)//2 + begin
        return begin, mid
    
    mid = (end - begin+1)//2 + begin
    return mid, end

def solve_lsq_not_as_dumb(data):
    numbers = numpy.array([int(n) for n in data.read().split(",")])
    space = numpy.min(numbers), numpy.max(numbers)

    def fn(meeting_point):
        return fuel_2(numbers, meeting_point)

    while space[1] != space[0]:
        space = chop_range(fn, space)

    return fn(space[0])

def test_fuel():
  assert fuel_2(numpy.array([11]), 0) == 66

def test_part0():
  data = io.StringIO("16,1,2,0,4,2,7,1,2,14")
  dumb = solve_dumb(data)
  data.seek(0, io.SEEK_SET)
  assert solve_clever(data) == dumb

def test_part1():
  with open("input7.txt","r") as data: 
    assert solve_clever(data) == 336721

def test_part00():
  data = io.StringIO("16,1,2,0,4,2,7,1,2,14")
  dumb = solve_lsq_dumb(data)
  data.seek(0, io.SEEK_SET)
  assert dumb == 168
  assert solve_lsq_not_as_dumb(data) == dumb

def test_part2():
  with open("input7.txt","r") as data: 
    assert solve_lsq_not_as_dumb(data) == 91638945
