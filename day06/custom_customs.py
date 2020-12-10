#!/usr/bin/env python3

class Individual(str):
    @property
    def answered_yes_to(self):
        return set(self)


class Group(list):
    @property
    def answered_yes_to(self):
        return set().union(*[individual.answered_yes_to for individual in self])

    @classmethod
    def from_string(cls, s):
        return cls([Individual(individual) for individual in s.split('\n')])


class Groups(list):
    @classmethod
    def from_string(cls, groups):
        return cls([Group.from_string(group) for group in groups.split('\n\n')])


def main():
    with open('input.txt', 'r') as f:
        input = f.read()

    groups = Groups.from_string(input)
    sum_group_counts = sum([len(group.answered_yes_to) for group in groups])
    print(sum_group_counts)


if __name__ == '__main__':
    main()
