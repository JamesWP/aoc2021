import pytest
import pdb
import numpy
import itertools

def parse(data):
    unique_signal_patterns = []
    four_digit_output_value = []

    for line in data.readlines():
        a, b = line.strip().split("|")
        a = [frozenset({c for c in sorted(seg)}) for seg in a.strip().split(" ")]
        b = [frozenset({c for c in sorted(seg)}) for seg in b.strip().split(" ")]
        unique_signal_patterns.append(a)
        four_digit_output_value.append(b)

    return unique_signal_patterns, four_digit_output_value

def onefourseveneight(data):
    _, four_digit_output_value = parse(data)

    return sum(1 for r in four_digit_output_value for v in r if len(v) in [2,3,4,7])


NUMBERS = (
    frozenset({'a','b','c','e','f','g'}),
    frozenset({'c','f'}),
    frozenset({'a','c','d','e','g'}),
    frozenset({'a','c','d','f','g'}),
    frozenset({'b','c','d','f'}),
    frozenset({'a','b','d','f','g'}),
    frozenset({'a','b','d','e','f','g'}),
    frozenset({'a','c','f'}),
    frozenset({'a','b','c','d','e','f','g'}),
    frozenset({'a','b','c','d','f','g'})
)

INCLUSIONS = {
  n: tuple(i for i in range(10) if NUMBERS[i].issubset(segments)) for n,segments in enumerate(NUMBERS)
}
EXCLUSIONS = {
  n: tuple(i for i in range(10) if not NUMBERS[i].issubset(segments)) for n,segments in enumerate(NUMBERS)
}
SHARE_LENGTH = {
  n: tuple(i for i in range(10) if len(NUMBERS[n]) ==len(NUMBERS[i])) for n,segments in enumerate(NUMBERS)
}
LENGTHS = {
  n: tuple(i for i in range(10) if len(NUMBERS[i]) == n) for n in range(max((len(num) for num in NUMBERS))+1)
}


def solve_one(signal, display):
    known = {}
    unknown = {}
    for sig in signal + display:
      possibilities = list(LENGTHS[len(sig)])

      if len(possibilities) == 1:
        known[possibilities[0]] = sig
      else:
        unknown[sig] = possibilities

      #print(sig, LENGTHS[len(sig)])
    
    #print("BEFORE")
    #print(len(known), known.keys())
    #print(len(unknown), unknown.values())

    for _ in range(5):
      for sig, possibilities in list(unknown.items()):
        new_possibilities = {}
        for possibility in list(possibilities):
          for inclusion in INCLUSIONS[possibility]:
            if inclusion in known:
              if not known[inclusion].issubset(sig):
                possibilities.remove(possibility) if possibility in possibilities else None
                break
          for exclusion in EXCLUSIONS[possibility]:
            if exclusion in known:
              if known[exclusion].issubset(sig):
                possibilities.remove(possibility) if possibility in possibilities else None
                break
          if possibility == 5:
            if 4 in known and 1 in known:
              four_minus_one = known[4] - known[1]
              if not four_minus_one.issubset(sig):
                possibilities.remove(possibility) if possibility in possibilities else None
                break
          if possibility == 2:
            if 4 in known and 1 in known:
              four_minus_one = known[4] - known[1]
              if four_minus_one.issubset(sig):
                possibilities.remove(possibility) if possibility in possibilities else None
                break
                 
          
        if len(possibilities) == 1:
          known[possibilities[0]] = sig
          del unknown[sig]

        if len(unknown) == 0:
          break


    #print("AFTER")
    #print(len(known), known.keys())
    #print(len(unknown), unknown.values())
    #print()

    segs_to_number = {
      seg: num for num, seg in known.items()
    }
    
    num = 0
    for i, mul in zip(display, [1000, 100, 10 ,1]):
      num += mul * segs_to_number[i]
     
    return num

def solve(data):
    signals, display = parse(data) 

    return sum(solve_one(signal,display) for signal, display in zip(signals, display))

def test_part0():
    with open("input8-test.txt") as data:
        assert onefourseveneight(data) == 26

def test_part1():
    with open("input8.txt") as data:
        assert onefourseveneight(data) == 530

def test_part00():
    with open("input8-test.txt") as data:
        assert solve(data) == 61229

def test_part2():
    with open("input8.txt") as data:
        assert solve(data) == 1051087
