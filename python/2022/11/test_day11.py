import unittest

from advent import get_puzzle_input

from day11 import part1


class TestDay11(unittest.TestCase):
    def setUp(self):
        self.test  = get_puzzle_input(2022, 11, "test.txt")
        self.input = get_puzzle_input(2022, 11)

    def test_part1(self):
        self.assertEqual(part1(self.test), 10605)
        self.assertEqual(part1(self.input), 98280)
