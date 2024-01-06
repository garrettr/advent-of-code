use std::collections::HashSet;
use std::num::ParseIntError;
use std::str::FromStr;

const EXAMPLE: &str = include_str!("example.txt");
const INPUT: &str = include_str!("input.txt");

#[derive(Debug, PartialEq, Eq)]
struct Card {
    winning_numbers: HashSet<u32>,
    numbers: HashSet<u32>,
}

#[derive(Debug, PartialEq, Eq)]
struct ParseCardError;

fn parse_ints(s: &str) -> Result<Vec<u32>, ParseIntError> {
    s.trim().split_whitespace().map(|s| s.parse()).collect()
}

impl FromStr for Card {
    type Err = ParseCardError;

    fn from_str(s: &str) -> Result<Self, Self::Err> {
        let sections: Vec<&str> = s.split(&[':', '|']).collect();
        if sections.len() != 3 {
            return Err(ParseCardError);
        }
        let winning_numbers = parse_ints(sections[1])
            .map_err(|_| ParseCardError)?
            .into_iter()
            .collect();
        let numbers = parse_ints(sections[2])
            .map_err(|_| ParseCardError)?
            .into_iter()
            .collect();
        Ok(Card {
            winning_numbers,
            numbers,
        })
    }
}

fn parse_cards(s: &str) -> Vec<Card> {
    s.lines().map(|line| line.parse().unwrap()).collect()
}

impl Card {
    fn num_matching(&self) -> u32 {
        (&self.winning_numbers & &self.numbers).len() as u32
    }

    fn points(&self) -> u32 {
        let num_matching = self.num_matching();
        if num_matching == 0 {
            0
        } else {
            u32::pow(2, num_matching as u32 - 1)
        }
    }
}

fn part1(input: &str) -> u32 {
    parse_cards(input).iter().map(|card| card.points()).sum()
}

fn part2(input: &str) -> u32 {
    let cards = parse_cards(input);
    let mut copies_per_card = vec![1; cards.len()];
    for (i, card) in cards.iter().enumerate() {
        for j in 1..=(card.num_matching() as usize) {
            copies_per_card[i + j] += copies_per_card[i];
        }
    }
    copies_per_card.iter().sum()
}

fn main() {
    dbg!(part1(INPUT));
    dbg!(part2(INPUT));
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_parse_ints() {
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

        let invalid = "1 foo 2";
        assert!(parse_ints(invalid).is_err());
    }

    #[test]
    fn test_card_fromstr() {
        let expected = Ok(Card {
            winning_numbers: HashSet::from([41, 48, 83, 86, 17]),
            numbers: HashSet::from([83, 86, 6, 31, 17, 9, 48, 53]),
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

    #[test]
    fn test_part2() {
        assert_eq!(part2(EXAMPLE), 30);
        assert_eq!(part2(INPUT), 9881048);
    }
}
