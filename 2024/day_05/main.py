import functools

with open("input.txt", "r") as file:
    input: list[str] = file.readlines()
    for i, line in enumerate(input):
        input[i] = line.replace("\n", "")

sep_index: int = input.index("")
rules: list[str] = input[:sep_index]


def is_valid(first: int, second: int, rule: str) -> bool:
    rule_str: list[str] = rule.split("|")
    rule_int: list[int] = [int(rule) for rule in rule_str]
    if first not in rule_int or second not in rule_int:
        return True
    return [first, second] == rule_int


def is_valid_all(first: int, second: int, rules: list[str]) -> bool:
    for rule in rules:
        if not is_valid(first, second, rule):
            return False
    return True


updates_str: list[str] = input[sep_index + 1 :]
updates: list[list[int]] = [
    [int(update_el) for update_el in update.split(",")] for update in updates_str
]

# part 1


def is_update_valid(update: list[int], rules: list[str]) -> bool:
    for i in range(len(update)):
        for j in range(i + 1, len(update)):
            if not is_valid_all(update[i], update[j], rules):
                return False
    return True


valid_updates: list[list[int]] = []
invalid_updates: list[list[int]] = []
for update in updates:
    (valid_updates if is_update_valid(update, rules) else invalid_updates).append(
        update
    )


def sum_of_middle(updates: list[list[int]]) -> int:
    sum: int = 0
    for update in updates:
        sum += update[len(update) // 2]
    return sum


print("Part 1:", sum_of_middle(valid_updates))

# Part 2


def cmp_update_el(first: int, second: int, rules: list[str]) -> int:
    for rule in rules:
        rule_str: list[str] = rule.split("|")
        rule_int: list[int] = [int(rule) for rule in rule_str]
        if first not in rule_int or second not in rule_int:
            continue
        if [first, second] != rule_int:
            return 1
    return -1


def fix_update(update: list[int], rules: list[str]) -> list[int]:
    return sorted(
        update, key=functools.cmp_to_key(lambda x, y: cmp_update_el(x, y, rules))
    )


fixed_updates: list[list[int]] = [
    fix_update(update, rules) for update in invalid_updates
]
print("Part 2:", sum_of_middle(fixed_updates))
