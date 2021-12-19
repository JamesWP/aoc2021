import collections
import io

TEST_INPUT= """NNCB

CH -> B
HH -> N
CB -> H
NH -> C
HB -> C
HC -> B
HN -> C
NN -> C
BH -> H
NC -> B
NB -> B
BN -> B
BB -> N
BC -> B
CC -> N
CN -> C"""

def pairs(polymer):
  pairs = collections.Counter()
  for pair in zip(polymer, polymer[1:]):
    pairs[pair] += 1

  return pairs

TESTS = {
  0: pairs('NCNBCHB'),
  1: pairs('NBCCNBBBCBHCB'),
  2: pairs('NBBBCNCCNBBNBNBBCHBHHBCHB'),
  3: pairs('NBBNBNBBCCNBCNCCNBBNBBNBBBNBBNBBCBHCBHHNHCBBCBHCB')
}

def parse(data):
  template = next(data).strip()

  next(data) 

  #print("template", template)

  rules = { tuple(fs): i for fs, i in ( line.strip().split(" -> ") for line in data) }

  return template, rules 

def solve(data, steps = 10, tests = None):
  template, rules = parse(data) 
 
  pair_counts = pairs(template)

  for i in range(steps):
    new_pair_counts = collections.Counter()
    for pair, count in pair_counts.items():
      if pair in rules:
        new_pair_counts[(pair[0], rules[pair])] += count
        new_pair_counts[(rules[pair], pair[1])] += count
      else:
        new_pair_counts[pair] += count
     
    if tests and i in tests:
      assert new_pair_counts == tests[i] 

    pair_counts = new_pair_counts
   

  result = collections.Counter()  

  for (a,b), count in pair_counts.items():
    result[a] += count
    result[b] += count

  result[template[0]] +=1
  result[template[-1]] +=1

  return result


def test_part0():
  result = solve(io.StringIO(TEST_INPUT), tests = TESTS)

  most_common = result.most_common()

  _, a = most_common[0]
  _, b = most_common[-1]

  assert a//2 - b//2 == 1588



def test_part1():
  with open("input14.txt") as data:
    result = solve(data)

  most_common = result.most_common()

  _, a = most_common[0]
  _, b = most_common[-1]

  assert a//2 - b//2 == 2621

def test_part00():
  result = solve(io.StringIO(TEST_INPUT), steps = 40)

  most_common = result.most_common()

  _, a = most_common[0]
  _, b = most_common[-1]

  assert a//2 - b//2 == 2188189693529
         
def test_part2():
  with open("input14.txt") as data:
    result = solve(data, steps = 40)

  most_common = result.most_common()

  _, a = most_common[0]
  _, b = most_common[-1]

  assert a//2 - b//2 == 2621
         
    
 
