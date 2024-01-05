use std::collections::HashSet;
use std::num::ParseIntError;
use std::str::FromStr;

const EXAMPLE: &str = include_str!("example.txt");
const INPUT: &str = include_str!("input.txt");

#[derive(Debug, PartialEq, Eq)]
struct Card {
    winning_numbers: Vec<i32>,
    numbers: Vec<i32>,
}

#[derive(Debug, PartialEq, Eq)]
struct ParseCardError;

fn parse_ints(s: &str) -> Result<Vec<i32>, ParseIntError> {
    s.trim()
        .split_whitespace()
        .map(|s| s.parse::<i32>())
        .collect()
}

impl FromStr for Card {
    type Err = ParseCardError;

    fn from_str(s: &str) -> Result<Self, Self::Err> {
        let sections: Vec<&str> = s.split(&[':', '|']).collect();
        if sections.len() != 3 {
            return Err(ParseCardError);
        }
        let winning_numbers = parse_ints(sections[1]).map_err(|_| ParseCardError)?;
        let numbers = parse_ints(sections[2]).map_err(|_| ParseCardError)?;
        Ok(Card {
            winning_numbers,
            numbers,
        })
    }
}

fn parse_cards(s: &str) -> Vec<Card> {
    s.lines()
        .map(|line| line.parse::<Card>().unwrap())
        .collect()
}

impl Card {
    fn points(&self) -> i32 {
        let winning_numbers: HashSet<i32> = self.winning_numbers.iter().cloned().collect();
        let num_winners: i32 = self
            .numbers
            .iter()
            .map(|n| if winning_numbers.contains(n) { 1 } else { 0 })
            .sum();
        if num_winners == 0 {
            0
        } else {
            i32::pow(2, num_winners as u32 - 1)
        }
    }
}

fn part1(input: &str) -> i32 {
    parse_cards(input).iter().map(|card| card.points()).sum()
}

fn part2(input: &str) -> () {}

fn main() {
    dbg!(part1(INPUT));
    // dbg!(part2(INPUT));
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_parse_ints_on_valid_inputs() {
        let valid = "1 2 3";
        assert_eq!(parse_ints(valid), Ok(Vec::from([1, 2, 3])));

        let valid_multiple_digits = "11 222 3333";
        assert_eq!(
            parse_ints(valid_multiple_digits),
            Ok(Vec::from([11, 222, 3333]))
        );

        let valid_leading_whitespace = " 1 2 3";
        assert_eq!(
            parse_ints(valid_leading_whitespace),
            Ok(Vec::from([1, 2, 3]))
        );

        let valid_trailing_whitespace = "1 2 3 ";
        assert_eq!(
            parse_ints(valid_trailing_whitespace),
            Ok(Vec::from([1, 2, 3]))
        );

        let valid_interior_whitespace = "10  1 22";
        assert_eq!(
            parse_ints(valid_interior_whitespace),
            Ok(Vec::from([10, 1, 22]))
        );
    }

    #[test]
    fn test_parse_ints_on_invalid_inputs() {
        let invalid = "1 foo 2";
        assert!(parse_ints(invalid).is_err());
    }

    #[test]
    fn test_card_fromstr() {
        let expected = Ok(Card {
            winning_numbers: Vec::from([41, 48, 83, 86, 17]),
            numbers: Vec::from([83, 86, 6, 31, 17, 9, 48, 53]),
        });

        let valid = "Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53";
        // Explicit call
        assert_eq!(Card::from_str(valid), expected);
        // Implicit calls, through parse
        assert_eq!(valid.parse(), expected);
        assert_eq!(valid.parse::<Card>(), expected);

        let missing_numbers = "Card 1: 41 48 83 86 17";
        assert!(Card::from_str(missing_numbers).is_err());
    }

    #[test]
    fn test_part1() {
        assert_eq!(part1(EXAMPLE), 13);
        assert_eq!(part1(INPUT), 21919);
    }

    // #[test]
    // fn test_part2() {
    //     // assert_eq!(part2(EXAMPLE), ());
    //     // assert_eq!(part2(INPUT), ());
    // }
}
