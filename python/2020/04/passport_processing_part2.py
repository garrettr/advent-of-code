#!/usr/bin/env python3

class PassportField(str):
    @property
    def valid(self):
        return False


class BirthYear(PassportField):
    @property
    def valid(self):
        has_4_digits = len(self) == 4 and self.isdecimal()
        in_range = 1920 <= int(self) <= 2002
        return has_4_digits and in_range


class IssueYear(PassportField):
    @property
    def valid(self):
        has_4_digits = len(self) == 4 and self.isdecimal()
        in_range = 2010 <= int(self) <= 2020
        return has_4_digits and in_range


class ExpirationYear(PassportField):
    @property
    def valid(self):
        has_4_digits = len(self) == 4 and self.isdecimal()
        in_range = 2020 <= int(self) <= 2030
        return has_4_digits and in_range


class Height(PassportField):
    @property
    def valid(self):
        unit = self[-2:]
        valid_unit = unit in ('cm', 'in')

        height = self[:-2]
        height_is_a_number = height.isdecimal()

        height_in_range = False
        try:
            if unit == 'cm':
                height_in_range = 150 <= int(height) <= 193
            elif unit == 'in':
                height_in_range = 59 <= int(height) <= 76
        except ValueError:
            # May occur if `height` is not a valid integer literal.
            pass

        return valid_unit and height_is_a_number and height_in_range


class HairColor(PassportField):
    @property
    def valid(self):
        hex_chars = '0123456789abcdef'
        return self.startswith('#') and all([char in hex_chars for char in self[1:]])


class EyeColor(PassportField):
    @property
    def valid(self):
        valid_eye_colors = ('amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth')
        return self in valid_eye_colors


class PassportID(PassportField):
    @property
    def valid(self):
        return len(self) == 9 and self.isdecimal()


class CountryID(PassportField):
    @property
    def valid(self):
        return True


class Passport:
    fields = {
        'byr': BirthYear,
        'iyr': IssueYear,
        'eyr': ExpirationYear,
        'hgt': Height,
        'hcl': HairColor,
        'ecl': EyeColor,
        'pid': PassportID,
        'cid': CountryID
    }

    def __init__(self, **kwargs):
        for name, cls in Passport.fields.items():
            setattr(self, name, cls(kwargs[name]) if name in kwargs else None)

    @classmethod
    def from_string(cls, s):
        fields = dict([f.split(':') for f in s.split()])
        return cls(**fields)

    @property
    def valid(self):
        required_fields = set(Passport.fields.keys()) - set(('cid',))
        has_required_fields = all([getattr(self, field) for field in required_fields])
        if not has_required_fields:
            return False

        required_fields_are_valid = all([getattr(self, field).valid for field in required_fields])
        return required_fields_are_valid


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

    def __iter__(self):
        # Make PassportsBatch iterable with a generator expression.
        # https://treyhunner.com/2018/06/how-to-make-an-iterator-in-python/
        return (passport for passport in self.passports)


def main():
    batch = PassportsBatch.from_file('input.txt')
    num_valid = sum([passport.valid for passport in batch])
    print(num_valid)


if __name__ == '__main__':
    main()

