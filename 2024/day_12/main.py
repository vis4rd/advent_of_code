with open("input.txt", "r") as file:
    input: list[str] = file.readlines()
    for i, line in enumerate(input):
        input[i] = line.replace("\n", "")

type loc_t = tuple[int, int]
DIRS = [(-1, 0), (1, 0), (0, -1), (0, 1)]
H_DIRS = DIRS[:2]
V_DIRS = DIRS[2:]

class Region:
    def __init__(self, letter: str) -> None:
        self.letter = letter
        self.tiles: set[loc_t] = set()

    def area(self) -> int:
        return len(self.tiles)

    def perimeter(self) -> int:
        perimeter = 0
        for tile in self.tiles:
            for dir in DIRS:
                if (tile[0] + dir[0], tile[1] + dir[1]) not in self.tiles:
                    perimeter += 1
        return perimeter

    def price(self) -> int:
        return self.area() * self.perimeter()

    def sides(self) -> int:
        v_parts: set[loc_t] = set()
        h_parts: set[loc_t] = set()
        for tile in self.tiles:
            for dir in DIRS:
                if (tile[0] + dir[0], tile[1] + dir[1]) not in self.tiles:
                    if dir[1] == 0:
                        v_parts.add((tile[0] + dir[0]*0.2, tile[1] + dir[1]*0.2))
                    else:
                        h_parts.add((tile[0] + dir[0]*0.2, tile[1] + dir[1]*0.2))

        def merge_parts(parts: set[loc_t], search_dirs: list[loc_t]) -> list[set[loc_t]]:
            sides: list[set[loc_t]] = []
            for part in parts:
                for side in sides:
                    if any((part[0] + dir[0], part[1] + dir[1]) in side for dir in search_dirs):
                        side.add(part)
                        break
                else:
                    sides.append({part})
            return sides

        v_sides: list[set[loc_t]] = merge_parts(v_parts, V_DIRS)
        h_sides: list[set[loc_t]] = merge_parts(h_parts, H_DIRS)

        def merge_sides(sides: list[set[loc_t]], search_dirs: list[loc_t]) -> list[set[loc_t]]:
            any_merged: bool = False
            for i in range(len(sides)):
                for j in range(i + 1, len(sides)):
                    if any((tile[0] + dir[0], tile[1] + dir[1]) in sides[j] for tile in sides[i] for dir in search_dirs):
                        sides[i] |= sides[j]
                        sides.pop(j)
                        any_merged = True
                        break
            return any_merged

        while(merge_sides(v_sides, V_DIRS)):
            pass
        while(merge_sides(h_sides, H_DIRS)):
            pass

        return len(v_sides) + len(h_sides)

    def discounted_price(self) -> int:
        return self.area() * self.sides()



def is_in_region(region: Region, loc: loc_t) -> bool:
    return loc in region.tiles

def can_be_in_region(region: Region, loc: loc_t) -> bool:
    return any((loc[0] + dir[0], loc[1] + dir[1]) in region.tiles for dir in DIRS)

def merge_regions(regions: list[Region]) -> bool:
    any_merged: bool = False
    for i in range(len(regions)):
        for j in range(i + 1, len(regions)):
            if regions[i].letter == regions[j].letter and any(can_be_in_region(regions[i], tile) for tile in regions[j].tiles):
                regions[i].tiles |= regions[j].tiles
                regions.pop(j)
                any_merged = True
                break
    return any_merged

def construct_regions(input: list[str]) -> list[Region]:
    regions: list[Region] = []

    for y, row in enumerate(input):
        for x, tile in enumerate(row):
            for region in regions:
                if tile != region.letter:
                    continue
                if is_in_region(region, (y, x)):
                    break
                if can_be_in_region(region, (y, x)):
                    region.tiles.add((y, x))
                    break
            else:
                new_region = Region(tile)
                new_region.tiles.add((y, x))
                regions.append(new_region)

    while(merge_regions(regions)):
        pass

    return regions

regions = construct_regions(input)

print("Part 1:", sum(region.price() for region in regions))
print("Part 2:", sum(region.discounted_price() for region in regions))
