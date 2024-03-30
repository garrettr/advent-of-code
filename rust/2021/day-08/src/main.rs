use std::collections::{HashMap, HashSet};

use frozenset::{Freeze, FrozenSet};

const EXAMPLE: &str = include_str!("example.txt");
const INPUT: &str = include_str!("input.txt");

#[derive(Debug)]
struct Entry<'a> {
    signal_patterns: [&'a str; 10],
    output_value: [&'a str; 4],
}

fn digits_to_int(digits: &[u8]) -> u64 {
    digits.iter().rev().enumerate().fold(0, |acc, (i, &d)| {
        acc + (d as u64) * 10u64.pow(i.try_into().unwrap())
    })
}

impl<'a> Entry<'a> {
    fn from_str(s: &'a str) -> Entry<'a> {
        let (signal_patterns, output_value) = s.split_once(" | ").unwrap();
        let output_value = output_value
            .split_ascii_whitespace()
            .collect::<Vec<&str>>()
            .try_into()
            .unwrap();
        let signal_patterns = signal_patterns
            .split_ascii_whitespace()
            .collect::<Vec<&str>>()
            .try_into()
            .unwrap();
        Self {
            signal_patterns,
            output_value,
        }
    }

    fn decode_digits(&self) -> HashMap<FrozenSet<char>, u8> {
        let mut patterns_by_len: HashMap<usize, Vec<HashSet<char>>> = HashMap::with_capacity(6);
        for pattern in self.signal_patterns {
            patterns_by_len
                .entry(pattern.len())
                .or_default()
                .push(pattern.chars().collect());
        }

        let mut digits: HashMap<u8, HashSet<char>> = HashMap::with_capacity(10);
        digits.insert(1, patterns_by_len.get_mut(&2).unwrap().remove(0));
        digits.insert(4, patterns_by_len.get_mut(&4).unwrap().remove(0));
        digits.insert(7, patterns_by_len.get_mut(&3).unwrap().remove(0));
        digits.insert(8, patterns_by_len.get_mut(&7).unwrap().remove(0));

        // There are two groups of remaining unidentified digits:
        // Length 5: 2, 3, 5
        // Length 6: 0, 6, 9

        // Of the 3 length 6 digits, 0 and 9 are a superset of the known digit 7,
        // while 6 is not.
        let v = patterns_by_len.get_mut(&6).unwrap();
        let i = v
            .iter()
            .position(|digit| !digit.is_superset(&digits[&7]))
            .unwrap();
        digits.insert(6, v.swap_remove(i));
        // Of the remaining length 6 digits, 0 and 9, 9 is a superset of 4 while
        // 0 is not.
        let i = v
            .iter()
            .position(|digit| digit.is_superset(&digits[&4]))
            .unwrap();
        digits.insert(9, v.swap_remove(i));
        assert!(v.len() == 1);
        digits.insert(0, v.swap_remove(0));

        // Similarly, of the 3 length 5 digits, only 3 is a superset of 7.
        let v = patterns_by_len.get_mut(&5).unwrap();
        let i = v
            .iter()
            .position(|digit| digit.is_superset(&digits[&7]))
            .unwrap();
        digits.insert(3, v.swap_remove(i));
        // Of the remaining length 5 digits, 2 and 5, only digit 5 contains
        // segments b and d. We can isolate segments b and d by taking the
        // difference of digit 4 - digit 1.
        let bd = &digits[&4] - &digits[&1];
        let i = v.iter().position(|digit| digit.is_superset(&bd)).unwrap();
        digits.insert(5, v.swap_remove(i));
        assert!(v.len() == 1);
        digits.insert(2, v.swap_remove(0));

        digits
            .drain()
            .map(|(digit, chars)| (chars.freeze(), digit))
            .collect()
    }

    fn decode(&self) -> u64 {
        let digits = self.decode_digits();
        let output_value: Vec<u8> = self
            .output_value
            .iter()
            .map(|digit| digit.chars().collect::<HashSet<_>>().freeze())
            .map(|digit| *digits.get(&digit).unwrap())
            .collect();
        digits_to_int(&output_value)
    }
}

fn parse(input: &str) -> Vec<Entry> {
    input
        .lines()
        .map(|line| Entry::from_str(line))
        .collect::<Vec<_>>()
}

fn part1(input: &str) -> u64 {
    let entries = parse(input);
    let unique_segment_lengths: HashSet<_> = [2, 3, 4, 7].into_iter().collect();
    entries
        .iter()
        .flat_map(|entry| entry.output_value.iter())
        .filter(|digit| unique_segment_lengths.contains(&digit.len()))
        .count() as u64
}

fn part2(input: &str) -> u64 {
    let entries = parse(input);
    entries.iter().map(|entry| entry.decode()).sum()
}

fn main() {
    dbg!(part1(INPUT));
    dbg!(part2(INPUT));
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_part1() {
        assert_eq!(part1(EXAMPLE), 26);
        assert_eq!(part1(INPUT), 381);
    }

    #[test]
    fn test_part2() {
        assert_eq!(part2(EXAMPLE), 61229);
        assert_eq!(part2(INPUT), 1023686);
    }
}
