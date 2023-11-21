#!/usr/bin/env python3

class Individual(str):
    @property
    def answered_yes_to(self):
        return set(self)


class Group(list):
    @classmethod
    def from_string(cls, s):
        return cls([Individual(individual) for individual in s.strip().split('\n')])

    @property
    def questions_anyone_answered_yes_to(self):
        return set().union(*[individual.answered_yes_to for individual in self])

    @property
    def questions_everyone_answered_yes_to(self):
        individuals_questions_with_yes_answers = [individual.answered_yes_to for individual in self]
        return individuals_questions_with_yes_answers[0].intersection(*individuals_questions_with_yes_answers[1:])


class Groups(list):
    @classmethod
    def from_string(cls, groups):
        return cls([Group.from_string(group) for group in groups.split('\n\n')])


def main():
    with open('input.txt', 'r') as f:
        input = f.read()

    groups = Groups.from_string(input)
    sum_group_anyone_counts = sum([len(group.questions_anyone_answered_yes_to) for group in groups])
    sum_group_everyone_counts = sum([len(group.questions_everyone_answered_yes_to) for group in groups])
    print(sum_group_anyone_counts)
    print(sum_group_everyone_counts)


if __name__ == '__main__':
    main()
