#!/usr/bin/env python3
import os

TEST = """R 4
U 4
L 3
D 1
R 4
D 1
L 5
R 2"""

TEST2 = """R 5
U 8
L 8
D 3
R 17
D 10
L 25
U 20"""


def parse(input):
    directions = []
    for line in input.splitlines():
        direction, distance = line.split()
        directions.append((direction, int(distance)))
    return directions


Zero = (0, 0)


def add_vector_to_point(point, vector):
    return (point[0] + vector[0], point[1] + vector[1])


def subtract_points(point1, point2):
    return (point1[0] - point2[0], point1[1] - point2[1])


def simulate_rope(motions):
    H = T = Zero
    T_history = [T]
    vectors = {
        "L": (-1, 0),
        "R": (1, 0),
        "U": (0, 1),
        "D": (0, -1),
    }

    T_moves = {
        (0, 2): (0, 1),
        (0, -2): (0, -1),
        (2, 0): (1, 0),
        (-2, 0): (-1, 0),
        (1, 2): (1, 1),
        (2, 1): (1, 1),
        (-1, 2): (-1, 1),
        (-2, 1): (-1, 1),
        (1, -2): (1, -1),
        (2, -1): (1, -1),
        (-1, -2): (-1, -1),
        (-2, -1): (-1, -1),
    }

    for direction, distance in motions:
        # print(f"=== {direction} {distance} ===")
        for _ in range(distance):
            H = add_vector_to_point(H, vectors[direction])
            diff = subtract_points(H, T)
            T_move = T_moves.get(diff, Zero)
            if T_move != Zero:
                T = add_vector_to_point(T, T_move)
                T_history.append(T)
            # print(f"H: {H}, T: {T}, diff: {diff}")

    return T_history


def part1(input):
    motions = parse(input)
    T_history = simulate_rope(motions)
    T_uniques = set(T_history)
    print(len(T_uniques))


class Rope:
    def __init__(self, length):
        self.length = length
        self.knots = [Zero] * length
        self.knot_histories = [[Zero] for _ in range(length)]

    def __str__(self):
        dims = [[0, 0], [0, 0]]
        for i in range(2):
            for j, fn in enumerate((min, max)):
                dims[i][j] = fn(k[i] for k in self.knots)

        padding = 2

        def name(knot):
            i = self.knots.index(knot)
            return "H" if i == 0 else str(i)

        return "\n".join(
            [
                "".join(
                    [
                        name((x, y)) if (x, y) in self.knots else "."
                        for x in range(dims[0][0], dims[0][1] + 1 + padding)
                    ]
                )
                for y in reversed(range(dims[1][0], dims[1][1] + 1 + padding))
            ]
        )

    def simulate(self, motions):
        directions = {
            "L": (-1, 0),
            "R": (1, 0),
            "U": (0, 1),
            "D": (0, -1),
        }

        follow_moves = {
            (0, 2): (0, 1),
            (0, -2): (0, -1),
            (2, 0): (1, 0),
            (-2, 0): (-1, 0),
            (1, 2): (1, 1),
            (2, 1): (1, 1),
            (2, 2): (1, 1),
            (-1, 2): (-1, 1),
            (-2, 1): (-1, 1),
            (-2, 2): (-1, 1),
            (1, -2): (1, -1),
            (2, -1): (1, -1),
            (2, -2): (1, -1),
            (-1, -2): (-1, -1),
            (-2, -1): (-1, -1),
            (-2, -2): (-1, -1),
        }

        for direction, distance in motions:
            # print(f"== {direction} {distance} ==")
            for _ in range(distance):
                # Move head
                self.knots[0] = add_vector_to_point(
                    self.knots[0], directions[direction]
                )
                # Move the rest
                for i in range(1, self.length):
                    diff = subtract_points(self.knots[i - 1], self.knots[i])
                    move = follow_moves.get(diff, Zero)
                    if move != Zero:
                        self.knots[i] = add_vector_to_point(self.knots[i], move)
                        self.knot_histories[i].append(self.knots[i])
                # print(f"\n{self}\n")


def part2(input):
    motions = parse(input)
    r = Rope(10)
    r.simulate(motions)
    print(len(set(r.knot_histories[-1])))


# part1(TEST)
# part2(TEST)
# part2(TEST2)

input_path = os.path.join(os.path.dirname(__file__), "input.txt")
with open(input_path) as f:
    input = f.read().strip()
    part1(input)
    part2(input)
