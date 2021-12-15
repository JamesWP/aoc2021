from typing import DefaultDict
import numpy

def run(data):
    grid = {}
    flow = {}
    for y, line in enumerate(data):
        for x, col in enumerate(line.strip()):
            grid[(x,y)]=int(col)

    for (px,py), pv in grid.items():
        n = []
        for xd,yd in ((-1,0),(1,0),(0,-1),(0,1)):
            x = px + xd
            y = py + yd

            if (x,y) not in grid:
                continue

            n.append((x,y))

        flow_out = [(x,y) for x,y in n if pv > grid[(x,y)]]

        if not flow_out:
            flow[(px,py)] = (px, py)
        else:
            flow[(px,py)] = flow_out[0]
        
    #low_points = [grid[c] for c,cf in flow.items() if c == cf]

    while True:
        did_flowing = False
        for c,cf in flow.items():
            if flow[c] != c and flow[c] != flow[cf]:
                flow[c] = flow[cf]
                did_flowing = True
        if not did_flowing:
            break

    flow_by_destination = DefaultDict(list)

    for c, cf in flow.items():
        if grid[c] != 9:
            flow_by_destination[cf].append(c)

    basin_sizes = [len(sources) for _, sources in flow_by_destination.items()]
    return [ grid[d] for d in flow_by_destination.keys()], basin_sizes 


def test_part0():
    with open("input9-test.txt") as data:
        low_points, _ = run(data)
        sum(low_points) + len(low_points) == 15

def test_part1():
    with open("input9.txt") as data:
        low_points, _ = run(data)
        sum(low_points) + len(low_points) == 541

def test_part00():
    with open("input9-test.txt") as data:
        _, basins = run(data)
        prod = 1
        for x in sorted(basins)[-3:]:
            prod *= x
        assert prod == 1134

def test_part2():
    with open("input9.txt") as data:
        _, basins = run(data)
        prod = 1
        for x in sorted(basins)[-3:]:
            prod *= x
        assert prod == 847504