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


# part1(TEST)

input_path = os.path.join(os.path.dirname(__file__), "input.txt")
with open(input_path) as f:
    input = f.read().strip()
    part1(input)
