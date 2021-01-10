#!/usr/bin/env python3

class ExpenseReport(list):

    @classmethod
    def from_list(cls, l):
        return cls(l)

    @classmethod
    def from_file(cls, filename):
        with open(filename, "r") as f:
            expenses = [int(line) for line in f.readlines() if line]
            return cls(expenses)


def find_two_entries_that_sum_to_2020(expenses):
    for ai, a in enumerate(expenses):
        for b in expenses[ai+1:]:
            if a + b == 2020:
                return a, b


def solve_part_1(expense_report):
    a, b = find_two_entries_that_sum_to_2020(expense_report)
    return a * b


def find_three_entries_that_sum_to_2020(expenses):
    for ai, a in enumerate(expenses):
        for bi, b in enumerate(expenses[ai+1:]):
            for c in expenses[ai+bi+1:]:
                if a + b + c == 2020:
                    return a, b, c


def solve_part_2(expense_report):
    a, b, c = find_three_entries_that_sum_to_2020(expense_report)
    return a * b * c


def main():
    expense_report = ExpenseReport.from_file('input.txt')
    print(solve_part_1(expense_report))
    print(solve_part_2(expense_report))


if __name__ == "__main__":
    main()
