import io
import numpy
import bitstring

def test_part0():
  data= """00100
11110
10110
10111
10101
01111
00111
11100
10000
11001
00010
01010"""
  
  with io.StringIO(data) as data:
    values = list(list(line.strip()) for line in data.readlines())
   
  values = numpy.array(values)
  gamma_rate = numpy.sum(numpy.transpose(values) == '1', 1) >= numpy.size(values, 0)/2
    
  gamma_rate = bitstring.BitArray(gamma_rate).uint


  epsilon_rate = numpy.sum(numpy.transpose(values) == '1', 1) < numpy.size(values, 0)/2
    
  epsilon_rate = bitstring.BitArray(epsilon_rate).uint

  assert gamma_rate == 22
  assert epsilon_rate == 9

def test_part1():
  with open("input3.txt") as data:
    values = list(list(line.strip()) for line in data.readlines())
   
  values = numpy.array(values)
  gamma_rate = numpy.sum(numpy.transpose(values) == '1', 1) >= numpy.size(values, 0)/2
    
  gamma_rate = bitstring.BitArray(gamma_rate).uint
  epsilon_rate = numpy.sum(numpy.transpose(values) == '1', 1) < numpy.size(values, 0)/2
    
  epsilon_rate = bitstring.BitArray(epsilon_rate).uint

  assert gamma_rate == 419
  assert epsilon_rate == 3676
  assert gamma_rate * epsilon_rate == 1
