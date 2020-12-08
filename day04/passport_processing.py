#!/usr/bin/env python3

class Passport:
    properties = set((
        'byr', 'iyr', 'eyr', 'hgt',
        'hcl', 'ecl', 'pid', 'cid',
    ))
    
    def __init__(self, **kwargs):
        for prop in Passport.properties:
            setattr(self, prop, kwargs.get(prop))

    @classmethod
    def from_string(cls, s):
        props = dict([f.split(':') for f in s.split()])
        return cls(**props)

    @property
    def valid(self):
        required_props = Passport.properties - set(('cid',))
        return all([getattr(self, prop) for prop in required_props])

    
class PassportsBatch:
    def __init__(self, passports):
        self.passports = passports

    @classmethod
    def from_file(cls, filename):
        with open(filename, 'r') as f:
            contents = f.read()
            # Passports are separated by '\n\n'
            passport_strings = contents.split('\n\n')
            passports = [Passport.from_string(s) for s in passport_strings]
            return cls(passports)
        

def main():
    batch = PassportsBatch.from_file('input.txt')
    num_valid = sum([passport.valid for passport in batch.passports])
    print(num_valid)


if __name__ == '__main__':
    main()

