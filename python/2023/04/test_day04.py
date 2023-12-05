import unittest

from advent import get_puzzle_input

from day04 import part1, part2


class TestDay04(unittest.TestCase):
    def setUp(self):
        self.example = get_puzzle_input(2023, 4, "example.txt")
        self.input = get_puzzle_input(2023, 4)

    def test_part1(self):
        self.assertEqual(part1(self.example), 13)
        self.assertEqual(part1(self.input), 21919)

    def test_part2(self):
        self.assertEqual(part2(self.example), 30)
        self.assertEqual(part2(self.input), 9881048)
