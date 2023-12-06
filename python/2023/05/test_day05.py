import unittest

from advent import get_puzzle_input

from day05 import part1, part2


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
