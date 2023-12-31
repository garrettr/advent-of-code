#!/usr/bin/env python3
from dataclasses import dataclass
from pprint import pprint
import unittest

from advent import get_puzzle_input


@dataclass
class Range:
    dst_start: int
    src_start: int
    len: int

    def dst(self, src: int) -> int:
        if src in range(self.src_start, self.src_start + self.len):
            return self.dst_start + src - self.src_start
        return src


@dataclass
class Map:
    src: str
    dst: str
    ranges: list[Range]

    def find(self, src: int) -> int:
        for range in self.ranges:
            dst = range.dst(src)
            if dst != src:
                return dst
        return src


@dataclass
class Almanac:
    seeds_to_be_planted: list[int]
    maps: dict[str, Map]

    @classmethod
    def from_str(cls, s: str):
        seeds_section, *sections = s.split("\n\n")
        seeds_to_be_planted = [
            int(n) for n in seeds_section.split(":")[1].strip().split()
        ]

        maps = {}
        for section in sections:
            lines = section.split("\n")
            src, dst = lines[0].split()[0].split("-to-")
            ranges = [Range(*[int(n) for n in line.split()]) for line in lines[1:]]
            maps[src] = Map(src, dst, ranges)

        return cls(seeds_to_be_planted, maps)

    def find(self, src: str, src_num: int, dst: str) -> int:
        map = self.maps[src]
        if map.dst == dst:
            return map.find(src_num)
        return self.find(map.dst, map.find(src_num), dst)


def part1(input: str):
    almanac = Almanac.from_str(input)
    return min(
        almanac.find("seed", seed, "location") for seed in almanac.seeds_to_be_planted
    )


def part2(input: str):
    pass


class TestDay05(unittest.TestCase):
    def setUp(self):
        self.example = get_puzzle_input(2023, 5, "example.txt")
        self.input = get_puzzle_input(2023, 5)

    def test_part1(self):
        self.assertEqual(part1(self.example), 35)
        self.assertEqual(part1(self.input), 323142486)

    # def test_part2(self):
    #     self.assertEqual(part2(self.example), 30)
    #     self.assertEqual(part2(self.input), 9881058)


if __name__ == "__main__":
    unittest.main()
