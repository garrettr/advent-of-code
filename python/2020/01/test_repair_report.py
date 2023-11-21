#!/usr/bin/env python3

import unittest

from repair_report import ExpenseReport, solve_part_1, solve_part_2

class TestRepairReport(unittest.TestCase):

    def setUp(self):
        self.expense_report = ExpenseReport.from_list([1721, 979, 366, 299, 675, 1456])

    def test_part_one(self):
        self.assertEqual(solve_part_1(self.expense_report), 514579)

    def test_part_two(self):
        self.assertEqual(solve_part_2(self.expense_report), 241861950)
