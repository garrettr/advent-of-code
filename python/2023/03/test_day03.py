import unittest

from advent import get_puzzle_input

from day03 import part1, part2


class TestDay03(unittest.TestCase):
    def setUp(self):
        self.example = get_puzzle_input(2023, 3, "example.txt")
        self.input = get_puzzle_input(2023, 3)

    def test_part1(self):
        self.assertEqual(part1(self.example), 4361)
        self.assertEqual(part1(self.input), 530849)

    def test_part2(self):
        self.assertEqual(part2(self.example), 467835)
        self.assertEqual(part2(self.input), 84900879)
