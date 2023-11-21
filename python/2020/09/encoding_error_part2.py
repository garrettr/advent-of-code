#!/usr/bin/env python3

from itertools import combinations


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
                return False, number
        return True, None

    def _find_contiguous_set_of_summands_for(self, invalid_number):
        all_numbers = self.preamble + self.numbers

        for i in range(len(all_numbers) - 2):
            for j in range(i + 2, len(all_numbers)):
                summands = all_numbers[i:j]
                if sum(summands) == invalid_number:
                    return summands

    def find_encryption_weakness(self, invalid_number):
        summands = self._find_contiguous_set_of_summands_for(invalid_number)
        return sum((f(summands) for f in (min, max)))


def main():
    cypher = XmasCypher.from_file('input.txt')
    validated, invalid_number = cypher.validate()
    print(invalid_number)
    weakness = cypher.find_encryption_weakness(invalid_number)
    print(weakness)

if __name__ == '__main__':
    main()
