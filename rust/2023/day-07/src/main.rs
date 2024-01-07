use std::collections::HashMap;
use std::num::ParseIntError;
use std::str::FromStr;

const EXAMPLE: &str = include_str!("example.txt");
const INPUT: &str = include_str!("input.txt");

#[derive(Debug, PartialEq, Eq, Hash, PartialOrd, Ord, Clone, Copy)]
enum Card {
    Joker,
    Number(u8),
    Jack,
    Queen,
    King,
    Ace,
}

#[derive(Debug, PartialEq)]
struct Hand {
    cards: [Card; 5],
    bid: i32,
}

#[derive(Debug, PartialEq, Eq, PartialOrd, Ord)]
enum HandType {
    HighCard,
    OnePair,
    TwoPair,
    ThreeOfAKind,
    FullHouse,
    FourOfAKind,
    FiveOfAKind,
}

#[derive(Debug, PartialEq)]
enum CamelCardsError {
    InvalidCard(char),
    InvalidHand(String),
    InvalidBid(ParseIntError),
}

impl TryFrom<char> for Card {
    type Error = CamelCardsError;

    fn try_from(c: char) -> Result<Self, Self::Error> {
        match c {
            'A' => Ok(Self::Ace),
            'K' => Ok(Self::King),
            'Q' => Ok(Self::Queen),
            'J' => Ok(Self::Jack),
            'T' => Ok(Self::Number(10)),
            digit @ '2'..='9' => Ok(Self::Number(digit as u8 - b'0')),
            _ => Err(Self::Error::InvalidCard(c)),
        }
    }
}

impl FromStr for Hand {
    type Err = CamelCardsError;

    fn from_str(s: &str) -> Result<Self, Self::Err> {
        let (cards, bid) = s.split_once(' ').ok_or(Self::Err::InvalidHand(format!(
            "Failed to split on space: {:?}",
            s
        )))?;

        let cards = cards
            .chars()
            .map(|c| Card::try_from(c))
            .collect::<Result<Vec<Card>, _>>()?
            .try_into()
            .map_err(|err| {
                Self::Err::InvalidHand(format!("Failed to parse cards {:?}: {:?}", cards, err))
            })?;

        let bid = bid.parse().map_err(|err| Self::Err::InvalidBid(err))?;

        Ok(Self { cards, bid })
    }
}

impl Hand {
    fn hand_type(&self) -> HandType {
        use HandType::*;

        let mut card_counts: Vec<i32> = self
            .cards
            .iter()
            .fold(HashMap::new(), |mut acc, card| {
                *acc.entry(card).or_insert(0) += 1;
                acc
            })
            .into_values()
            .collect();

        card_counts.sort_unstable_by(|a, b| b.cmp(a));

        match card_counts.as_slice() {
            &[5] => FiveOfAKind,
            &[4, 1] => FourOfAKind,
            &[3, 2] => FullHouse,
            &[3, 1, 1] => ThreeOfAKind,
            &[2, 2, 1] => TwoPair,
            &[2, 1, 1, 1] => OnePair,
            &[1, 1, 1, 1, 1] => HighCard,
            _ => panic!("Invalid type for hand: {:?} ({:?})", self, card_counts),
        }
    }
}

fn part1(input: &str) -> i32 {
    let mut hands: Vec<Hand> = input
        .lines()
        .map(|line| Hand::from_str(line).unwrap())
        .collect();

    hands.sort_unstable_by_key(|hand| (hand.hand_type(), hand.cards));

    hands
        .iter()
        .enumerate()
        .map(|(rank, hand)| (rank + 1) as i32 * hand.bid)
        .sum()
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
    fn test_parse_card() {
        assert_eq!(Card::try_from('A'), Ok(Card::Ace));
        assert_eq!(Card::try_from('K'), Ok(Card::King));
        assert_eq!(Card::try_from('Q'), Ok(Card::Queen));
        assert_eq!(Card::try_from('J'), Ok(Card::Jack));
        assert_eq!(Card::try_from('T'), Ok(Card::Number(10)));
        assert_eq!(Card::try_from('9'), Ok(Card::Number(9)));
        assert_eq!(Card::try_from('8'), Ok(Card::Number(8)));
        assert_eq!(Card::try_from('7'), Ok(Card::Number(7)));
        assert_eq!(Card::try_from('6'), Ok(Card::Number(6)));
        assert_eq!(Card::try_from('5'), Ok(Card::Number(5)));
        assert_eq!(Card::try_from('4'), Ok(Card::Number(4)));
        assert_eq!(Card::try_from('3'), Ok(Card::Number(3)));
        assert_eq!(Card::try_from('2'), Ok(Card::Number(2)));
        assert_eq!(Card::try_from('1'), Err(CamelCardsError::InvalidCard('1')));
    }

    #[test]
    fn test_parse_hand() {
        let expected = Hand {
            cards: [
                Card::Number(3),
                Card::Number(2),
                Card::Number(10),
                Card::Number(3),
                Card::King,
            ],
            bid: 765,
        };
        assert_eq!("32T3K 765".parse(), Ok(expected));

        assert!(matches!(
            "32T3K765".parse::<Hand>(),
            Err(CamelCardsError::InvalidHand(_))
        ));

        assert!(matches!(
            "32T3W 765".parse::<Hand>(),
            Err(CamelCardsError::InvalidCard('W'))
        ));

        assert!(matches!(
            "32T3K 76F".parse::<Hand>(),
            Err(CamelCardsError::InvalidBid(_))
        ));
    }

    #[test]
    fn test_hand_type() {
        use HandType::*;
        assert_eq!(Hand::from_str("AAAAA 0").unwrap().hand_type(), FiveOfAKind);
        assert_eq!(Hand::from_str("AA8AA 0").unwrap().hand_type(), FourOfAKind);
        assert_eq!(Hand::from_str("23332 0").unwrap().hand_type(), FullHouse);
        assert_eq!(Hand::from_str("TTT98 0").unwrap().hand_type(), ThreeOfAKind);
        assert_eq!(Hand::from_str("23432 0").unwrap().hand_type(), TwoPair);
        assert_eq!(Hand::from_str("A23A4 0").unwrap().hand_type(), OnePair);
        assert_eq!(Hand::from_str("23456 0").unwrap().hand_type(), HighCard);
    }

    #[test]
    fn test_part1() {
        assert_eq!(part1(EXAMPLE), 6440);
        assert_eq!(part1(INPUT), 247815719);
    }

    #[test]
    fn test_part2() {
        // assert_eq!(part2(EXAMPLE), ());
        // assert_eq!(part2(INPUT), ());
    }
}
