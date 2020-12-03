#!/usr/bin/env python3

def parse_expense_report(expense_report):
    return [int(line) for line in expense_report.split('\n') if line != ""]

def find_two_entries_that_sum_to_2020(expenses):
    for ai, a in enumerate(expenses):
        for b in expenses[ai+1:]:
            if a + b == 2020:
                return a, b

def solve_part_1(expense_report_filename):
    expense_report = open(expense_report_filename, 'r').read()
    expenses = parse_expense_report(expense_report)
    a, b = find_two_entries_that_sum_to_2020(expenses)
    return a * b

def find_three_entries_that_sum_to_2020(expenses):
    for ai, a in enumerate(expenses):
        for bi, b in enumerate(expenses[ai+1:]):
            for c in expenses[ai+bi+1:]:
                if a + b + c == 2020:
                    return a, b, c

def solve_part_2(expense_report_filename):
    expense_report = open(expense_report_filename, 'r').read()
    expenses = parse_expense_report(expense_report)
    a, b, c = find_three_entries_that_sum_to_2020(expenses)
    return a * b * c

def main():
    print(solve_part_1('input.txt'))
    print(solve_part_2('input.txt'))

if __name__ == "__main__":
    main()
