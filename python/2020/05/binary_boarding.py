#!/usr/bin/env python3

from functools import cached_property


def bsp(a, b, s):
    #print(a, b, s)

    if len(s) == 0:
        return a

    half = s[0]
    half_size = (b - a) // 2

    if half == 'F' or half == 'L':
        b = a + half_size
    elif half == 'B' or half == 'R':
        a = b - half_size

    return bsp(a, b, s[1:])


class BoardingPass(str):
    rows = 128
    cols = 8

    @cached_property
    def row(self):
        return bsp(0, BoardingPass.rows - 1, self[:7])

    @cached_property
    def col(self):
        return bsp(0, BoardingPass.cols - 1, self[-3:])

    @cached_property
    def seat_id(self):
        return self.row * 8 + self.col


def main():
    with open('input.txt', 'r') as f:
        boarding_passes = [BoardingPass(line.strip()) for line in f.readlines()]

    seat_ids = [boarding_pass.seat_id for boarding_pass in boarding_passes]
    highest_seat_id = max(seat_ids)

    sorted_seat_ids = sorted(seat_ids)
    for i, sid in enumerate(sorted_seat_ids[:-1]):
        if sorted_seat_ids[i+1] != sid + 1:
            missing_seat_id = sid + 1

    print(highest_seat_id)
    print(missing_seat_id)


if __name__ == '__main__':
    main()
