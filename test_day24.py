def test_get_constants():
    constants = []
    with open("input24.txt") as data:
        for i, line in enumerate(data):
            if i % 18 == 0:
                constants.append([])
            if i % 18 in [4,5,15]:
                i = int(line.split(" ")[2])
                constants[-1].append(i)

    return constants

def func2(z0, w0, constants):
    c0, c1, c2 = constants
    w = w0
    z = z0
    x = z % 26
    z = z // c0
    x = x + c1
    x = 1 if x == w else 0
    x = 1 if x == 0 else 0
    y = 0
    y = y + 25
    y = y * x
    y = y + 1
    z = z * y
    y = 0
    y = y + w
    y = y + c2
    y = y * x
    z = z + y

    return z


def test_day1():
    constants = test_get_constants()
    print(*constants, sep="\n")

    [
     [1, 12, 9], 
        [1, 12, 4], 
            [1, 12, 2], 
            [26, -9, 5], 
        [26, -9, 1], 
        [1, 14, 6], 
            [1, 14, 11], 
            [26, -10, 15], 
            [1, 15, 7], 
            [26, -2, 12], 
            [1, 11, 15], 
            [26, -15, 9], 
        [26, -9, 12], 
     [26, -3, 12]
    ]
    print()
    answer = [9, 9, 2, 4] # 1-4
    answer = [9, 8, 9, 4, 9, 9, 9, 6] #5-12  
    answer = [3, 9, 9, 2, 4, 9, 8, 9, 4, 9, 9, 9, 6, 9] #1-12  
    # 39924989499969

    answer = [6, 8, 1, 1] # 1-4
    answer = [4, 1, 2, 1, 6, 1, 1, 1] #5-12  
    answer = [1, 6, 8, 1, 1, 4, 1, 2, 1, 6, 1, 1, 1, 7] #1-12  
    # 16811412161117
    z=0
    for constant in constants:
        if len(answer) != 0:
            a = answer[0]
            answer = answer[1:]
            znew = func2(z, a, constant)
            print(constant, "\t", znew%26, znew)
            z = znew
        else:
            print(constant, end="\t")
            for w in range(10):
                print(w, func2(z, w, constant)%26, sep=": ", end=" ")
            print()

    print()
    constant = [26,-2,12]
    #constant = [26,-9,12]
    #constant = [26,-15,9]
    constant=[26,-3,12]
    for z in range(26):
        print(z, end=":: \t")
        for w in range(10):
            print(w, func2(z, w, constant), sep=": ", end="\t")
        print()