# example

# list1 = [3, 4, 2, 1, 3, 3]
# list2 = [4, 3, 5, 3, 9, 3]


def part1():
    with open('input.txt', 'r') as file:
        lines = file.readlines()
        list1 = []
        list2 = []
        for line in lines:
            left_str, right_str = line.split()
            list1.append(int(left_str))
            list2.append(int(right_str))

    list1.sort()
    list2.sort()

    sum = 0
    for left, right in zip(list1, list2):
        diff = abs(left - right)
        sum += diff

    print("Part 1:", sum)

def part2():
    with open('input.txt', 'r') as file:
        lines = file.readlines()
        list1 = []
        list2 = []
        for line in lines:
            left_str, right_str = line.split()
            list1.append(int(left_str))
            list2.append(int(right_str))

    list1.sort()
    list2.sort()

    sum = 0
    for left in list1:
        count = list2.count(left)
        sum += left * count

    print("Part 2:", sum)

part1()
part2()
