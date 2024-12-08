import re


def compute_all_muls(matches: list[str]):
    sum: int = 0
    for match in matches:
        nums: list[int] = [int(x) for x in match[4:-1].split(',')]
        result: int = nums[0] * nums[1]
        sum += result

    print(sum)

def compute_all_muls_with_conditionals(matches: list[str]):
    remember: bool = True
    new_matches: list[str] = []
    for match in matches:
        if match.startswith('do()'):
            remember = True
            continue
        elif match.startswith('don\'t()'):
            remember = False
            continue
        if remember:
            new_matches.append(match)
    compute_all_muls(new_matches)

with open('input.txt', 'r') as file:
    input: str = ''.join(file.readlines())

    pattern: str = r'mul\([0-9]{1,3},[0-9]{1,3}\)'
    matches: list[str] = re.findall(pattern, input)
    print("Part 1:", end="")
    compute_all_muls(matches)

    pattern2: str = r'(?:mul\([0-9]{1,3},[0-9]{1,3}\)|(?:do\(\))|(?:don\'t\(\)))'
    matches2: list[str] = re.findall(pattern2, input)
    print("Part 2:", end="")
    compute_all_muls_with_conditionals(matches2)
