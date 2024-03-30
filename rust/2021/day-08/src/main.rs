use std::collections::HashSet;

const EXAMPLE: &str = include_str!("example.txt");
const INPUT: &str = include_str!("input.txt");

#[derive(Debug)]
struct Entry<'a> {
    signal_patterns: [&'a str; 10],
    output_value: [&'a str; 4],
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
    0
}

fn main() {
    dbg!(part1(EXAMPLE));
    // dbg!(part2(EXAMPLE));
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
        // assert_eq!(part2(EXAMPLE), 0);
        // assert_eq!(part2(INPUT), 0);
    }
}
