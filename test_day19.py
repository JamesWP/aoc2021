import itertools
import collections
import numpy
from numpy.core.fromnumeric import shape

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
        for test_point_index in range(test_points.shape[0]):
            for unknown_point_index in range(unknown.shape[0]):
                
                offset = test_points[test_point_index, :] - unknown_translated[unknown_point_index, :]

                test_point_set =  points_to_set(test_points)
                unknown_translated_offset_set =  points_to_set(unknown_translated + offset)

                num_congruent = len(unknown_translated_offset_set.intersection(test_point_set))

                if num_congruent >= 12:
                    print("Hit")
                    return view_no, offset


def test_part0():
    scanner_offsets = {}
    test_beacons = test_input()
    for (a, scannera), (b,scannerb) in itertools.permutations(enumerate(test_beacons), r=2):
        result = solve(test_beacons[scannera], test_beacons[scannerb])
        if result:
            scanner_offsets[(a,b)] = result

    print(scanner_offsets)