#!/usr/bin/env python3
"""
Python translation of the general-purpose backtracking algorithm from
"Programming Challenges: The Programming Contest Training Manual", p. 167-175.
"""

# Maximum solution length
AMAX = 10
# Found all solutions yet?
finished = False

# 8.1 Backtracking


def backtrack(a: list, k: int, input):
    if is_a_solution(a, k, input):
        process_solution(a, k)
    else:
        k += 1
        for candidate in construct_candidates(a, k, input):
            a[k] = candidate
            backtrack(a, k, input)
            if finished:
                return  # Terminate early


# 8.2 Constructing All Subsets
def is_a_solution(a: list, k: int, n: int):
    return k == n


def construct_candidates(a: list, k: int, n: int):
    return [True, False]


def process_solution(a: list, k: int):
    print(f"{{ {' '.join(str(i) for i in range(1, k + 1) if a[i])} }}")


def generate_subsets(n: int):
    a = [0] * AMAX
    backtrack(a, 0, n)


if __name__ == "__main__":
    generate_subsets(3)
