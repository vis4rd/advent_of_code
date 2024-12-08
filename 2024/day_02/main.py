with open('input.txt', 'r') as file:
    lines_str = file.readlines()
    lines: list[list[int]] = []
    for line in lines_str:
        line_levels = line.split()
        lines.append([int(x) for x in line_levels])

def part1():
    safe_count = 0
    for line in lines:
        if len(line) == len(set(line)):
            if (line == sorted(line)) or (line == sorted(line, reverse=True)):
                ok = True
                for i in range(len(line)-1):
                    if abs(line[i] - line[i+1]) > 3:
                        ok = False
                        break
                if ok:
                    safe_count += 1

    print("Part 1:", safe_count)

def part2():
    safe_count = 0
    for line in lines:
        variants = [line[:i] + line[i+1:] for i in range(len(line))]

        for variant in variants:
            if len(variant) == len(set(variant)):
                if (variant == sorted(variant)) or (variant == sorted(variant, reverse=True)):
                    ok = True
                    for i in range(len(variant)-1):
                        if abs(variant[i] - variant[i+1]) > 3:
                            ok = False
                            break
                    if ok:
                        safe_count += 1
                        break

    print("Part 2:", safe_count)

part1()
part2()
