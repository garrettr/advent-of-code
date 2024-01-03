use itertools::Itertools;
use std::collections::{HashMap, HashSet};

const EXAMPLE: &str = include_str!("example.txt");
const INPUT: &str = include_str!("input.txt");

fn main() {
    // dbg!(part1(INPUT));
    dbg!(part2(INPUT));
}

type Grid = Vec<Vec<char>>;

fn parse_grid(raw_grid: &str) -> Grid {
    raw_grid
        .lines()
        .map(|line| line.chars().collect())
        .collect()
}

#[derive(Debug, Eq, PartialEq, Hash, Clone)]
struct Point {
    row: usize,
    col: usize,
}

#[derive(Debug, Eq, PartialEq, Hash, Clone)]
struct Number {
    loc: Point,
    len: usize,
    value: i32,
}

#[derive(Debug, Eq, PartialEq, Hash, Clone)]
struct Part {
    loc: Point,
    value: char,
}

#[derive(Debug)]
struct Schematic {
    numbers: Vec<Number>,
    parts: Vec<Part>,
}

fn parse_schematic(grid: Grid) -> Schematic {
    let mut numbers = Vec::new();
    let mut digits = Vec::new();
    let mut parts = Vec::new();

    for (r, row) in grid.iter().enumerate() {
        for (c, &col) in row.iter().enumerate() {
            if col.is_ascii_digit() {
                digits.push(col);
                if c < row.len() - 1 {
                    continue;
                }
            } else if col != '.' {
                parts.push(Part {
                    loc: Point { row: r, col: c },
                    value: col,
                });
            }

            if !digits.is_empty() {
                let digits_str: String = digits.iter().collect();
                let value = digits_str.parse::<i32>().unwrap();
                numbers.push(Number {
                    loc: Point {
                        row: r,
                        col: c - digits.len(),
                    },
                    len: digits.len(),
                    value,
                });
                digits.clear();
            }
        }
    }

    Schematic { numbers, parts }
}

const OFFSETS: [i32; 3] = [-1, 0, 1];

impl Schematic {
    fn find_adjacent_numbers(&self, part: &Part) -> HashSet<Number> {
        let mut adjacent_numbers = HashSet::new();
        for row_offset in OFFSETS {
            for col_offset in OFFSETS {
                let row = part.loc.row as i32 + row_offset;
                let col = part.loc.col as i32 + col_offset;
                for number in self.numbers.iter() {
                    if row == number.loc.row as i32
                        && col >= number.loc.col as i32
                        && col < (number.loc.col + number.len) as i32
                    {
                        adjacent_numbers.insert(number.clone());
                    }
                }
            }
        }
        adjacent_numbers
    }
}

fn find_part_numbers(schematic: Schematic) -> HashMap<Part, HashSet<Number>> {
    let mut part_numbers = HashMap::new();
    for part in schematic.parts.iter() {
        let adjacent_numbers = schematic.find_adjacent_numbers(part);
        part_numbers.insert(part.clone(), adjacent_numbers);
    }
    part_numbers
}

fn part1(input: &str) -> i32 {
    let grid = parse_grid(input);
    let schematic = parse_schematic(grid);
    let part_numbers = find_part_numbers(schematic);
    part_numbers
        .values()
        .into_iter()
        .fold(HashSet::new(), |acc, hashset| {
            acc.union(&hashset).cloned().collect()
        })
        .iter()
        .map(|part_number| part_number.value)
        .sum()
}

fn part2(input: &str) -> i32 {
    let grid = parse_grid(input);
    let schematic = parse_schematic(grid);
    let part_numbers = find_part_numbers(schematic);
    part_numbers
        .iter()
        //.inspect(|&pn| println!("Debug: {:?}", pn))
        .filter_map(|(part, numbers)| {
            if part.value == '*' && numbers.len() == 2 {
                //println!("Debug: {:?} => {:?}", part, numbers);
                Some(numbers.iter().fold(1, |acc, number| acc * number.value))
            } else {
                None
            }
        })
        .sum()
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_part1() {
        assert_eq!(part1(EXAMPLE), 4361);
        assert_eq!(part1(INPUT), 530849);
    }

    #[test]
    fn test_part2() {
        assert_eq!(part2(EXAMPLE), 467835);
        assert_eq!(part2(INPUT), 84900879);
    }
}
