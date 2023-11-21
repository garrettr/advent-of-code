#!/usr/bin/env python3

class PasswordPolicy:
    def __init__(self, min, max, char):
        self.min = min
        self.max = max
        self.char = char

    @staticmethod
    def parse_line(line):
        dash_index = line.find('-')
        first_space_index = line.find(' ')
        colon_index = line.find(':')
        
        min = int(line[0:dash_index])
        max = int(line[dash_index+1:first_space_index])
        char = line[first_space_index+1:colon_index]
                       
        return min, max, char

    @classmethod
    def from_line(cls, line):
        min, max, char = cls.parse_line(line)
        return cls(min, max, char)

    def valid(self, password):
        return self.min <= password.count(self.char) <= self.max


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
