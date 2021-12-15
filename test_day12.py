import io
import collections

TEST_INPUT = """start-A
start-b
A-c
A-b
b-d
A-end
b-end"""

TEST_OUTPUT = [
    "start,A,b,A,c,A,end",
    "start,A,b,A,end",
    "start,A,b,end",
    "start,A,c,A,b,A,end",
    "start,A,c,A,b,end",
    "start,A,c,A,end",
    "start,A,end",
    "start,b,A,c,A,end",
    "start,b,A,end",
    "start,b,end",
]

TEST_INPUT2 = """dc-end
HN-start
start-kj
dc-start
dc-HN
LN-dc
HN-end
kj-sa
kj-HN
kj-dc"""

TEST_OUTPUT2 = [
    "start,HN,dc,HN,end",
    "start,HN,dc,HN,kj,HN,end",
    "start,HN,dc,end",
    "start,HN,dc,kj,HN,end",
    "start,HN,end",
    "start,HN,kj,HN,dc,HN,end",
    "start,HN,kj,HN,dc,end",
    "start,HN,kj,HN,end",
    "start,HN,kj,dc,HN,end",
    "start,HN,kj,dc,end",
    "start,dc,HN,end",
    "start,dc,HN,kj,HN,end",
    "start,dc,end",
    "start,dc,kj,HN,end",
    "start,kj,HN,dc,HN,end",
    "start,kj,HN,dc,end",
    "start,kj,HN,end",
    "start,kj,dc,HN,end",
    "start,kj,dc,end",
]

TEST_OUTPUT_pt2 = [
    'start,A,b,A,b,A,c,A,end',
    'start,A,b,A,b,A,end',
    'start,A,b,A,b,end',
    'start,A,b,A,c,A,b,A,end',
    'start,A,b,A,c,A,b,end',
    'start,A,b,A,c,A,c,A,end',
    'start,A,b,A,c,A,end',
    'start,A,b,A,end',
    'start,A,b,d,b,A,c,A,end',
    'start,A,b,d,b,A,end',
    'start,A,b,d,b,end',
    'start,A,b,end',
    'start,A,c,A,b,A,b,A,end',
    'start,A,c,A,b,A,b,end',
    'start,A,c,A,b,A,c,A,end',
    'start,A,c,A,b,A,end',
    'start,A,c,A,b,d,b,A,end',
    'start,A,c,A,b,d,b,end',
    'start,A,c,A,b,end',
    'start,A,c,A,c,A,b,A,end',
    'start,A,c,A,c,A,b,end',
    'start,A,c,A,c,A,end',
    'start,A,c,A,end',
    'start,A,end',
    'start,b,A,b,A,c,A,end',
    'start,b,A,b,A,end',
    'start,b,A,b,end',
    'start,b,A,c,A,b,A,end',
    'start,b,A,c,A,b,end',
    'start,b,A,c,A,c,A,end',
    'start,b,A,c,A,end',
    'start,b,A,end',
    'start,b,d,b,A,c,A,end',
    'start,b,d,b,A,end',
    'start,b,d,b,end',
    'start,b,end',
]

def get_routes(data, has_double_visited):
    graph = collections.defaultdict(list)
    for line in data:
        begin, end = line.strip().split("-")
        graph[begin].append(end)
        graph[end].append(begin)

    #print()
    #print(*graph.items(), sep="\n")

    def inner(route, begin, end, visited, hdv):
        if route and begin == 'start':
          return

        if begin in visited and hdv:
          return

        route.append(begin)

        double_visit = False

        if begin[0].islower():
            if begin in visited:
              hdv = True
              double_visit = True
            visited.add(begin)

        if begin == end:
            yield list(route)
        else:
            for edge in sorted(graph[begin]):
                yield from inner(route, edge, end, visited, hdv)

        if begin[0].islower():
            if not double_visit:
              visited.remove(begin)

        route.pop()

    return list(inner([], "start", "end", set(), has_double_visited))


def test_part0():
    data = io.StringIO(TEST_INPUT)
    routes = get_routes(data, has_double_visited=True)
    #print(*routes, sep="\n")
    assert len(routes) == 10

    for r, tr in zip(routes, TEST_OUTPUT):
        assert ",".join(r) == tr

    data = io.StringIO(TEST_INPUT2)
    routes = get_routes(data, has_double_visited=True)
    #print(*routes, sep="\n")

    for r, tr in zip(routes, TEST_OUTPUT2):
        assert ",".join(r) == tr

    with open("input12-test.txt") as data:
      routes = get_routes(data, has_double_visited=True)
    assert len(routes) == 226

def test_part1():
    with open("input12.txt") as data:
      routes = get_routes(data, has_double_visited=True)
    assert len(routes) == 3887
    
import pytest
def test_part00():
    data = io.StringIO(TEST_INPUT)
    routes = get_routes(data, has_double_visited=False)
    #print(*routes, sep="\n")

    assert len(routes) == 36

    for r, tr in zip(routes, TEST_OUTPUT_pt2):
        assert ",".join(r) == tr

    data = io.StringIO(TEST_INPUT2)
    routes = get_routes(data, has_double_visited=False)
    #print(*routes, sep="\n")

    assert len(routes) == 103

    with open("input12-test.txt") as data:
      routes = get_routes(data, has_double_visited=False)

    assert len(routes) == 3509

def test_part2():
    with open("input12.txt") as data:
      routes = get_routes(data, has_double_visited=False)
    assert len(routes) == 104834
