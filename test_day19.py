import itertools
import collections
import numpy
from numpy.core.fromnumeric import shape
import random

def parse(data):
    beacon_locations = {}
    scanner = None
    locations = []

    for line in data:
        if "scanner" in line:
            if locations:
                beacon_locations[scanner] = numpy.array(locations)
                locations = []
            _,_,num,_ = line.split(" ")
            scanner = int(num)
        elif "," in line:
            x,y,z = line.split(",")
            locations.append((int(x), int(y), int(z)))

    if locations:
        beacon_locations[scanner] = numpy.array(locations)
        locations = []

    return beacon_locations

transforms = numpy.array([
    [1,0,0,0,1,0,0,0,1],
    [1,0,0,0,0,-1,0,1,0],
    [1,0,0,0,-1,0,0,0,-1],
    [1,0,0,0,0,1,0,-1,0],
    [0,-1,0,1,0,0,0,0,1],
    [0,0,1,1,0,0,0,1,0],
    [0,1,0,1,0,0,0,0,-1],
    [0,0,-1,1,0,0,0,-1,0],
    [-1,0,0,0,-1,0,0,0,1],
    [-1,0,0,0,0,-1,0,-1,0],
    [-1,0,0,0,1,0,0,0,-1],
    [-1,0,0,0,0,1,0,1,0],
    [0,1,0,-1,0,0,0,0,1],
    [0,0,1,-1,0,0,0,-1,0],
    [0,-1,0,-1,0,0,0,0,-1],
    [0,0,-1,-1,0,0,0,1,0],
    [0,0,-1,0,1,0,1,0,0],
    [0,1,0,0,0,1,1,0,0],
    [0,0,1,0,-1,0,1,0,0],
    [0,-1,0,0,0,-1,1,0,0],
    [0,0,-1,0,-1,0,-1,0,0],
    [0,-1,0,0,0,1,-1,0,0],
    [0,0,1,0,1,0,-1,0,0],
    [0,1,0,0,0,-1,-1,0,0]]).reshape((24,3,3))

def viewpoint(locations, view_no):
    return locations.dot(transforms[view_no,:,:])

def test_input():
    with open("input19-test.txt") as data:
        return parse(data)

def real_input():
    with open("input19.txt") as data:
        return parse(data)

def points_to_set(array):
    return set(map(tuple,array))

def solve(test_points, unknown):
    for view_no in range(24):
        unknown_translated = viewpoint(unknown, view_no)

        test_point_list = list(range(test_points.shape[0]))
        unknown_point_list = list(range(unknown.shape[0]))

        random.shuffle(test_point_list)
        random.shuffle(unknown_point_list)

        test_point_list = test_point_list[0:20]
        unknown_point_list = unknown_point_list[0:20]

        for test_point_index in test_point_list:
            for unknown_point_index in unknown_point_list:
                
                offset = test_points[test_point_index, :] - unknown_translated[unknown_point_index, :]

                test_point_set =  points_to_set(test_points)
                unknown_translated_offset_set =  points_to_set(unknown_translated + offset)

                num_congruent = len(unknown_translated_offset_set.intersection(test_point_set))

                if num_congruent >= 12:
                    #print("Hit", view_no, offset)
                    return True, unknown_translated + offset, (view_no, offset)
    return False, None, None

def test_part0():
    test_beacons = test_input()
    while len(test_beacons) != 1:
        print(len(test_beacons), "groups remaining")
        for a, b in itertools.permutations(test_beacons, r=2):
            solved, result, solution = solve(test_beacons[a], test_beacons[b])
            if solved:
                test_beacons[a] = numpy.append(test_beacons[a], result, axis = 0)
                del test_beacons[b]
                break
    
    beacon_set = points_to_set(test_beacons[0])

    assert len(beacon_set) == 79

existing_solutions = [
    (0, 9, 9, (2, 1164, 41)),
(0, 10, 2, (1289, 1241, -37)),
(0, 11, 3, (27, 140, -1287)),
(0, 19, 23, (-45, 1174, -1191)),
(0, 26, 10, (-61, 2500, -1165)),
(0, 28, 16, (2319, 1204, -73)),
(0, 1, 8, (2320, 2356, -48)),
(0, 4, 14, (3706, 2481, -87)),
(0, 5, 21, (3601, 2517, 1178)),
(0, 3, 13, (4871, 2359, 1248)),
(0, 6, 4, (2493, 1292, -1245)),
(0, 7, 7, (4768, 2434, 25)),
(0, 18, 18, (2399, 88, -1282)),
(0, 16, 20, (3526, 17, -1303)),
(0, 8, 11, (3601, -16, -80)),
(0, 12, 6, (4772, 105, 56)),
(0, 25, 22, (2470, 3720, 52)),
(0, 21, 1, (3594, 2364, -1153)),
(0, 29, 17, (1137, -32, -57)),
(0, 34, 14, (1142, 1352, 1164)),
(0, 14, 22, (1133, 2441, 1205)),
(0, 15, 5, (1174, 16, 1239)),
(0, 23, 12, (2405, -1165, 43)),
(0, 24, 11, (3675, -1127, -1148)),
(0, 20, 19, (1216, 96, 2358)),
(0, 27, 13, (1118, -1129, 1231)),
(0, 32, 0, (4797, 2530, 2345)),
(0, 33, 14, (3554, 3580, 33)),
(0, 13, 10, (29, -1118, 1226)),
(0, 2, 17, (4772, 2460, 3667)),
(0, 35, 2, (3667, -1065, 63)),
(0, 31, 15, (3549, 2439, 2354)),
(0, 36, 10, (2483, 73, 11)),
(22, 37, 12, (-1148, -29, -45)),
(0, 17, 16, (4782, 3739, 3602)),
(0, 22, 15, (5928, -1, -1243)),
(0, 30, 2, (4877, 2438, 4735))
]

def test_part1():
    test_beacons = real_input()

    positions = {}

    for existing_solution in existing_solutions:
        dest, source, view, offset = existing_solution
        result = viewpoint(test_beacons[source], view) + numpy.array(offset)
        test_beacons[dest] = numpy.append(test_beacons[dest], result, axis = 0)
        del test_beacons[source]

        if dest == 0:
            positions[source]  = (viewpoint(numpy.array([[0,0,0]]), view) + numpy.array(offset)).reshape(3)

    print(max(abs(x1-x2)+abs(y1-y2)+abs(z1-z2) for (x1,y1,z1), (x2,y2,z2) in itertools.permutations(positions.values(), r=2)))
    #assert len(test_beacons) == 1

    while len(test_beacons) != 1:
        #print(len(test_beacons), "groups remaining")
        for a, b in itertools.permutations(test_beacons, r=2):
            if b == 0:
                continue
            solved, result, solution = solve(test_beacons[a], test_beacons[b])
            if solved:
                view, offset = solution
                print((a, b, view, tuple(offset)), sep=",")
                #print("above solution for translating", b, "into", a)
                test_beacons[a] = numpy.append(test_beacons[a], result, axis = 0)
                del test_beacons[b]
                #print(*test_beacons.keys(), sep=", ")
                break
                
    print(*test_beacons.keys(), sep="\n")

    for key, value in  test_beacons.items():
        beacon_set = points_to_set(value)

        assert len(beacon_set) == 457
        assert key == 0
