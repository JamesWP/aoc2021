TEST_INPUT = """[({(<(())[]>[[{[]{<()<>>
[(()[<>])]({[<{<<[]>>(
{([(<{}[<>[]}>{[]{[(<()>
(((({<>}<{<{<>}{[]{[]{}
[[<[([]))<([[{}[[()]]]
[{[{({}]{}}([{[{{{}}([]
{<[[]]>}<{[{[{[]{()[[[]
[<(<(<(<{}))><([]([]()
<{([([[(<>()){}]>(<<{{
<{([{{}}[<[[[<>{}]]]>[]]"""

OPEN_CLOSE = {
  '(':')',
  '[':']',
  '{':'}',
  '<':'>'
}

SCORE = {
  ')': 3,
  ']': 57,
  '}': 1197,
  '>': 25137
}

def parse(data):
  scores = []
  incomplete_parts = []
  for line in data.split("\n"):
    stack = []
    incomplete = False
    for char in line:
      corrupt = False
      if char in OPEN_CLOSE:
        stack.append(OPEN_CLOSE[char])
      else:
        if not stack:
          incomplete=True
          break 
        st = stack.pop()
        if st != char:
          #print("expected", st, "but found", char, "instead")
          scores.append(SCORE[char])
          corrupt = True
          break

    if corrupt or not stack:
      continue

    stack.reverse()
    incomplete_parts.append(stack)
      
  return scores, incomplete_parts

def test_part0():
  result,_ = parse(TEST_INPUT)
  syntax_error = result
  assert sum(syntax_error) == 26397

def test_part1():
  with open("input10.txt") as f:
      data = f.read()

  result,_ = parse(data)
  syntax_error = result
  assert sum(syntax_error) == 345441

COMP_SCORE = {
  ')':1,
  ']':2,
  '}':3,
  '>':4
}

def test_part00():
  _,incomplete = parse(TEST_INPUT)
  assert incomplete[0] == list('}}]])})]')

  def score(completion):  
    s = 0
    for c in completion:
      s *=5
      s += COMP_SCORE[c]
    return s

  incomplete = [ score(i) for i in incomplete] 
  #print(len(incomplete)) 
  assert len(incomplete) % 2 == 1
  assert incomplete[0] == 288957
  assert incomplete[1] == 5566

  incomplete.sort()

  assert incomplete[(len(incomplete)-1)//2] == 288957

def test_part2():
  with open("input10.txt") as f:  
    data = f.read()

  _,incomplete = parse(data)

  def score(completion):  
    s = 0
    for c in completion:
      s *=5
      s += COMP_SCORE[c]
    return s

  incomplete = [ score(i) for i in incomplete] 

  incomplete.sort()

  assert incomplete[(len(incomplete)-1)//2] == 3235371166
