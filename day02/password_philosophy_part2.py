#!/usr/bin/env python3

class PasswordPolicy:
    def __init__(self, p1, p2, char):
        self.p1 = p1
        self.p2 = p2
        self.char = char

    @staticmethod
    def parse_line(line):
        dash_index = line.find('-')
        first_space_index = line.find(' ')
        colon_index = line.find(':')
        
        p1 = int(line[0:dash_index])
        p2 = int(line[dash_index+1:first_space_index])
        char = line[first_space_index+1:colon_index]
                       
        return p1, p2, char

    @classmethod
    def from_line(cls, line):
        return cls(*cls.parse_line(line))

    def valid(self, password):
        # -1 because (Be careful; Toboggan Corporate Policies have no concept of "index zero"!)
        p1_match = password[self.p1-1] == self.char
        p2_match = password[self.p2-1] == self.char
        return p1_match ^ p2_match


class Password(str):
    @staticmethod
    def parse_line(line):
        colon_index = line.find(':')
        return line[colon_index+2:]

    @classmethod
    def from_line(cls, line):
        return cls.parse_line(line)

    
def main():
    lines = [line.strip() for line in open('input.txt', 'r').readlines()]
    passwords = [Password.from_line(line) for line in lines]
    policies = [PasswordPolicy.from_line(line) for line in lines]
    results = [policy.valid(password) for policy, password in zip(policies, passwords)]
    num_valid_passwords = len([result for result in results if result])
    print(num_valid_passwords)
    

if __name__ == "__main__":
    main()
