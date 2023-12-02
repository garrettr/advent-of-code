import unittest

from advent import get_puzzle_input

from day02 import part1, part2


class TestDay02(unittest.TestCase):
    def setUp(self):
        self.example = get_puzzle_input(2023, 2, "example.txt")
        self.input = get_puzzle_input(2023, 2)

    def test_part1(self):
        self.assertEqual(part1(self.example), 8)
        self.assertEqual(part1(self.input), 2149)

    # def test_part2(self):
    #     self.assertEqual(part2(self.example), 281)
    #     self.assertEqual(part2(self.input), 54418)
