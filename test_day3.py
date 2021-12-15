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
  assert gamma_rate * epsilon_rate == 1540244

def test_part00():
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
    values_start = list(list(line.strip()) for line in data.readlines())
   
  values = numpy.array(values_start)

 
  for OXY in [True, False]: 
    values = numpy.array(values_start)
    for bit in range(5):
      zero_counts = numpy.sum(numpy.transpose(values) == '0',1)
      one_counts = numpy.sum(numpy.transpose(values) == '1',1)
      #print("\t", '0', zero_counts, '1', one_counts)
      
      if OXY:
        keep_zero = zero_counts > one_counts
      else:
        keep_zero = zero_counts <= one_counts

      #print("\t", "keep zero", keep_zero[bit])
      keep = values[:,bit] == ('0' if keep_zero[bit] else '1')
      #print("\t", values[keep])
      #print("\t", keep)

      values = values[keep]
      if numpy.size(values,0)<2:
        break
    #print("done", values)
    value = bitstring.BitArray(values[0] == '1').uint
    #print("OXY" if OXY else "CO2", value)


def test_part2():
  with open("input3.txt", "r") as data:
    values_start = list(list(line.strip()) for line in data.readlines())
   
  values = numpy.array(values_start)

 
  for OXY in [True, False]: 
    values = numpy.array(values_start)
    for bit in range(12):
      zero_counts = numpy.sum(numpy.transpose(values) == '0',1)
      one_counts = numpy.sum(numpy.transpose(values) == '1',1)
      #print("\t", '0', zero_counts, '1', one_counts)
      
      if OXY:
        keep_zero = zero_counts > one_counts
      else:
        keep_zero = zero_counts <= one_counts

      #print("\t", "keep zero", keep_zero[bit])
      keep = values[:,bit] == ('0' if keep_zero[bit] else '1')
      #print("\t", values[keep])
      #print("\t", keep)

      values = values[keep]
      if numpy.size(values,0)<2:
        break
    #print("done", values)
    value = bitstring.BitArray(values[0] == '1').uint
    #print("OXY" if OXY else "CO2", value)


