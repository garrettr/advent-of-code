#!/usr/bin/env python3

from itertools import combinations


class InvalidNextNumber(Exception):
    def __init__(self, window, number):
        self.window = window
        self.number = number

    def __repr_(self):
        return f'{self.number} is not the sum of any two numbers in {self.window}'


class XmasCypher:
    def __init__(self, numbers, window_size=25):
        self.window_size = window_size
        self.preamble = numbers[:window_size]
        self.numbers = numbers[window_size:]

    @classmethod
    def from_file(cls, filename):
        with open(filename, 'r') as f:
            numbers = [int(line.strip()) for line in f.readlines()]
            return cls(numbers)

    @property
    def windows(self):
        window = self.preamble.copy()
        for number in self.numbers:
            yield window
            window = window[1:] + [number]

    @staticmethod
    def valid_next_number(window, number):
        for a, b in combinations(window, 2):
            if a + b == number:
                return True
        return False

    def validate(self):
        for window, number in zip(self.windows, self.numbers):
            if not self.valid_next_number(window, number):
                raise InvalidNextNumber(window, number)


def main():
    cypher = XmasCypher.from_file('input.txt')
    try:
        cypher.validate()
    except InvalidNextNumber as e:
        print(e)


if __name__ == '__main__':
    main()
