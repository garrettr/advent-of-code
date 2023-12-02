import unittest

from advent import get_puzzle_input

from day01 import part1, part2


class TestDay01(unittest.TestCase):
    def setUp(self):
        self.example = get_puzzle_input(2023, 1, "example.txt")
        self.example2 = get_puzzle_input(2023, 1, "example2.txt")
        self.input = get_puzzle_input(2023, 1)

    def test_part1(self):
        self.assertEqual(part1(self.example), 142)
        self.assertEqual(part1(self.input), 54304)

    def test_part2(self):
        self.assertEqual(part2(self.example2), 281)
        self.assertEqual(part2(self.input), 54418)
