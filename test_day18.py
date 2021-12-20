import math
import json
import itertools

class Explosion(Exception):
    def __init__(self, pair) -> None:
        super().__init__(pair)
        self.pair = pair

class Split(Exception):
    pass

def dump(number):
    return json.dumps(number).replace(" ", "")

def parse(number):
    return json.loads(number)

LEFT = 0
RIGHT = 1

def leftmost_add(parent, side, value):
    try:
        len(parent[side])
        # this is a pair, recurse
        leftmost_add(parent[side], LEFT, value)
    except TypeError:
        # this is a leaf, add
        parent[side] += value

def rightmost_add(parent, side, value):
    try:
        len(parent[side])
        # this is a pair, recurse
        rightmost_add(parent[side], RIGHT, value)
    except TypeError:
        # this is a leaf, add
        parent[side] += value

def explode(parent, side = None, level = 0):
    if side is None:
        # bootstrap
        sentinel = [parent, 0]
        try:
            did_explode = explode(sentinel, LEFT)
        except Explosion:
            did_explode = True
            pass 

        if sentinel[RIGHT] != 0:
            leftmost_add(parent, RIGHT, sentinel[RIGHT])
        return did_explode 

    # now we have our parent and ourselves
    number = parent[side]

    try:
        len(number) # assume number is a pair
    except TypeError: 
        # that was wrong, this must be a plain number
        return False

    # number is a pair

    if level == 4:
        print("exploding", number)
        # must explode!

        parent[side] = 0    

        if side == LEFT:
            leftmost_add(parent, RIGHT, number[RIGHT])
            number[RIGHT] = 0
        if side == RIGHT:
            rightmost_add(parent, LEFT, number[LEFT])
            number[LEFT] = 0

        raise Explosion(number)

    try:
        did_explode = explode(number, LEFT, level + 1)
        if did_explode:
            return did_explode
    except Explosion as e:
        left, right = e.pair
        if right != 0:
            leftmost_add(number, RIGHT, right)
            e.pair[RIGHT] = 0
        raise e

    try:
        did_explode = explode(number, RIGHT, level + 1)
        if did_explode:
            return did_explode
    except Explosion as e:
        left, right = e.pair
        if left != 0:
            rightmost_add(number, LEFT, left)
            e.pair[LEFT] = 0
        raise e

    return False

def split(parent, side = None):
    if side is None:
        sentinel = [parent, 0]
        try:
            return split(sentinel, LEFT)
        except Split:
            return True

    number = parent[side]

    try:
        len(number)

        split(number, LEFT)
        split(number, RIGHT)

    except TypeError:
        # this is a leaf
        if number >= 10:
            parent[side] = [math.floor(number / 2), math.ceil(number / 2)]
            raise Split()
    return False

def add(lhs, rhs):
    number = [lhs, rhs]

    reduce(number)

    return number

def reduce(number):
    print("reducing", number)
    while True:
        if explode(number):
            print("after explode", number)
            continue
        if split(number):
            print("after split", number)
            continue
        break 

def magnitude(number):
    try:
        left, right = number
        return magnitude(left)*3 + magnitude(right)*2
    except TypeError:
        return number

def pexplode(s):
    number = parse(s)

    assert explode(number)

    return dump(number)

def test_explode():

    assert pexplode('[[[[[9,8],1],2],3],4]') == '[[[[0,9],2],3],4]'
    # (the 9 has no regular number to its left, so it is not added to any regular number).

    assert pexplode('[7,[6,[5,[4,[3,2]]]]]') == '[7,[6,[5,[7,0]]]]'
    # (the 2 has no regular number to its right, and so it is not added to any regular number).

    assert pexplode('[[6,[5,[4,[3,2]]]],1]') == '[[6,[5,[7,0]]],3]'

    assert pexplode('[[3,[2,[1,[7,3]]]],[6,[5,[4,[3,2]]]]]') == '[[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]'
    # (the pair [3,2] is unaffected because the pair [7,3] is further to the left; [3,2] would explode on the next action).

    assert pexplode('[[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]') == '[[3,[2,[8,0]]],[9,[5,[7,0]]]]'

    assert pexplode('[[[[[4,3],4],4],[7,[[8,4],9]]],[1,1]]') == '[[[[0,7],4],[7,[[8,4],9]]],[1,1]]'

    assert pexplode('[[[[0,7],4],[7,[[8,4],9]]],[1,1]]') == '[[[[0,7],4],[15,[0,13]]],[1,1]]'

def test_explode2():

    assert pexplode('[[[[4,0],[5,0]],[[[4,5],[2,6]],[9,5]]],[7,[[[3,7],[4,3]],[[6,3],[8,8]]]]]') == '[[[[4,0],[5,4]],[[0,[7,6]],[9,5]]],[7,[[[3,7],[4,3]],[[6,3],[8,8]]]]]'

def test_split():
    def psplit(s):
        number = parse(s)

        assert split(number)

        return dump(number)
        
        
    assert psplit('[[[[0,7],4],[15,[0,13]]],[1,1]]') == '[[[[0,7],4],[[7,8],[0,13]]],[1,1]]'
    assert psplit('[[[[0,7],4],[[7,8],[0,13]]],[1,1]]') == '[[[[0,7],4],[[7,8],[0,[6,7]]]],[1,1]]'
    assert psplit('[1,10]') == '[1,[5,5]]'
    assert psplit('[1,11]') == '[1,[5,6]]'

def test_add():
    def padd(lhs, rhs):
        left = parse(lhs)
        right = parse(rhs)

        number = add(left, right)

        return dump(number)


    #assert padd('[[[[4,3],4],4],[7,[[8,4],9]]]','[1,1]') == '[[[[0,7],4],[[7,8],[6,0]]],[8,1]]'

    #assert padd(padd(padd('[1,1]', '[2,2]'), '[3,3]'), '[4,4]') == '[[[[1,1],[2,2]],[3,3]],[4,4]]'
    #assert padd(padd(padd(padd('[1,1]', '[2,2]'), '[3,3]'), '[4,4]'),'[5,5]') == '[[[[3,0],[5,3]],[4,4]],[5,5]]'

    assert padd('[[[0,[4,5]],[0,0]],[[[4,5],[2,6]],[9,5]]]' ,'[7,[[[3,7],[4,3]],[[6,3],[8,8]]]]') == '[[[[4,0],[5,4]],[[7,7],[6,0]]],[[8,[7,7]],[[7,9],[5,0]]]]'

    assert padd('[[[[4,0],[5,4]],[[7,7],[6,0]]],[[8,[7,7]],[[7,9],[5,0]]]]', '[[2,[[0,8],[3,4]]],[[[6,7],1],[7,[1,6]]]]') == '[[[[6,7],[6,7]],[[7,7],[0,7]]],[[[8,7],[7,7]],[[8,8],[8,0]]]]'

    assert padd('[[[[6,7],[6,7]],[[7,7],[0,7]]],[[[8,7],[7,7]],[[8,8],[8,0]]]]', '[[[[2,4],7],[6,[0,5]]],[[[6,8],[2,8]],[[2,1],[4,5]]]]') == '[[[[7,0],[7,7]],[[7,7],[7,8]]],[[[7,7],[8,8]],[[7,7],[8,7]]]]'

    assert padd('[[[[7,0],[7,7]],[[7,7],[7,8]]],[[[7,7],[8,8]],[[7,7],[8,7]]]]', '[7,[5,[[3,8],[1,4]]]]') == '[[[[7,7],[7,8]],[[9,5],[8,7]]],[[[6,8],[0,8]],[[9,9],[9,0]]]]'

    assert padd('[[[[7,7],[7,8]],[[9,5],[8,7]]],[[[6,8],[0,8]],[[9,9],[9,0]]]]', '[[2,[2,2]],[8,[8,1]]]') == '[[[[6,6],[6,6]],[[6,0],[6,7]]],[[[7,7],[8,9]],[8,[8,1]]]]'

    assert padd('[[[[6,6],[6,6]],[[6,0],[6,7]]],[[[7,7],[8,9]],[8,[8,1]]]]', '[2,9]') == '[[[[6,6],[7,7]],[[0,7],[7,7]]],[[[5,5],[5,6]],9]]'

    assert padd('[[[[6,6],[7,7]],[[0,7],[7,7]]],[[[5,5],[5,6]],9]]', '[1,[[[9,3],9],[[9,0],[0,7]]]]') == '[[[[7,8],[6,7]],[[6,8],[0,8]]],[[[7,7],[5,0]],[[5,5],[5,6]]]]'

    assert padd('[[[[7,8],[6,7]],[[6,8],[0,8]]],[[[7,7],[5,0]],[[5,5],[5,6]]]]', '[[[5,[7,4]],7],1]') == '[[[[7,7],[7,7]],[[8,7],[8,7]]],[[[7,0],[7,7]],9]]'

    assert padd('[[[[7,7],[7,7]],[[8,7],[8,7]]],[[[7,0],[7,7]],9]]', '[[[[4,2],2],6],[8,7]]') == '[[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]]'

def test_magnitude():
    def pmag(s):
        number = parse(s)
        return magnitude(number)

    assert pmag('[[1,2],[[3,4],5]]') == 143
    assert pmag('[[1,2],[[3,4],5]]') == 143
    assert pmag('[[[[0,7],4],[[7,8],[6,0]]],[8,1]]') == 1384.
    assert pmag('[[[[1,1],[2,2]],[3,3]],[4,4]]') == 445.
    assert pmag('[[[[3,0],[5,3]],[4,4]],[5,5]]') == 791.
    assert pmag('[[[[5,0],[7,4]],[5,5]],[6,6]]') ==  1137.
    assert pmag('[[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]]') == 3488

def test_part0():
    s = None
    with open("input18-test.txt") as data:
        for line in data:
            number = parse(line)

            if s is None:
                s = number
            else:
                s = add(s, number)

    assert dump(s) == '[[[[6,6],[7,6]],[[7,7],[7,0]]],[[[7,7],[7,7]],[[7,8],[9,9]]]]' 
    assert magnitude(s) == 4140

def test_part1():
    s = None
    with open("input18.txt") as data:
        for line in data:
            number = parse(line)

            if s is None:
                s = number
            else:
                s = add(s, number)

    assert magnitude(s) == 4207

def test_part00():
    numbers = []
    with open("input18-test.txt") as data:
        for line in data:
            numbers.append(line)

    max_mag = 0
    for a, b in itertools.combinations(numbers, 2):
        result = add(parse(a), parse(b))
        max_mag = max(max_mag, magnitude(result))

        result = add(parse(b), parse(a))
        max_mag = max(max_mag, magnitude(result))

    assert max_mag ==  3993

def test_part2():
    numbers = []
    with open("input18.txt") as data:
        for line in data:
            numbers.append(line)

    max_mag = 0
    for a, b in itertools.combinations(numbers, 2):
        result = add(parse(a), parse(b))
        max_mag = max(max_mag, magnitude(result))

        result = add(parse(b), parse(a))
        max_mag = max(max_mag, magnitude(result))

    assert max_mag ==  4635