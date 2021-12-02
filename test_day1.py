def test_part0():
    data = [199, 200, 208, 210, 200, 207, 240, 269, 260, 263]

    changes = zip(data, data[1:])
    changes = (1 if b>a else 0 for a,b in changes)
    assert sum(changes) == 7

def test_part1():
    data = []

    with open("input1.txt", "r") as data_file:
      for line in data_file.readlines():
        data.append(int(line))

    changes = zip(data, data[1:])
    changes = (1 if b>a else 0 for a,b in changes)
    assert sum(changes) == 1532

def test_part00():
    data = [199, 200, 208, 210, 200, 207, 240, 269, 260, 263]

    data = list( a+b+c for a,b,c in zip(data, data[1:], data[2:]))

    changes = zip(data, data[1:])
    changes = (1 if b>a else 0 for a,b in changes)
    assert sum(changes) == 5

def test_part2():
    data = []

    with open("input1.txt", "r") as data_file:
      for line in data_file.readlines():
        data.append(int(line))

    data = list( a+b+c for a,b,c in zip(data, data[1:], data[2:]))

    changes = zip(data, data[1:])
    changes = (1 if b>a else 0 for a,b in changes)
    assert sum(changes) == 1571
