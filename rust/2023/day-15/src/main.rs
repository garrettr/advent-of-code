use std::{collections::HashMap, fmt::Display, str::FromStr};

const EXAMPLE: &str = include_str!("example.txt");
const INPUT: &str = include_str!("input.txt");

fn hash(s: &str) -> u32 {
    s.bytes()
        .fold(0, |acc, byte| ((acc + byte as u32) * 17) % 256)
}

fn part1(input: &str) -> u32 {
    input.trim().split(',').map(|step| hash(step)).sum()
}

#[derive(Debug)]
enum Day15Error {
    ParseIntError(std::num::ParseIntError),
    ParseStepError(String),
}

impl Display for Day15Error {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        match self {
            Self::ParseIntError(e) => write!(f, "{}", e),
            Self::ParseStepError(s) => write!(f, "invalid step: {}", s),
        }
    }
}

impl From<std::num::ParseIntError> for Day15Error {
    fn from(e: std::num::ParseIntError) -> Self {
        Self::ParseIntError(e)
    }
}

#[derive(Debug)]
enum StepKind {
    Insert { focal_length: u8 },
    Remove,
}

#[derive(Debug)]
struct Step {
    label: String,
    kind: StepKind,
}

impl FromStr for Step {
    type Err = Day15Error;

    fn from_str(s: &str) -> Result<Self, Self::Err> {
        if s.contains('=') {
            let (label, focal_length) = s
                .split_once('=')
                .ok_or_else(|| Self::Err::ParseStepError(s.to_owned()))?;
            let focal_length = focal_length.parse()?;
            return Ok(Self {
                label: label.to_owned(),
                kind: StepKind::Insert { focal_length },
            });
        } else if s.contains('-') {
            let (label, _) = s
                .split_once('-')
                .ok_or_else(|| Self::Err::ParseStepError(s.to_owned()))?;
            return Ok(Self {
                label: label.to_owned(),
                kind: StepKind::Remove,
            });
        }
        Err(Self::Err::ParseStepError(s.to_owned()))
    }
}

#[derive(Debug)]
struct Lens {
    label: String,
    focal_length: u8,
}

fn parse(input: &str) -> Vec<Step> {
    input
        .trim()
        .split(',')
        .map(|step| step.parse().expect("step should be parsed successfully"))
        .collect()
}

fn focusing_power(box_num: u8, slot_num: u8, focal_length: u8) -> u32 {
    (box_num as u32 + 1) * (slot_num as u32 + 1) * focal_length as u32
}

fn part2(input: &str) -> u32 {
    let steps = parse(input);
    let mut boxes: HashMap<u8, Vec<Lens>> = HashMap::with_capacity(256);

    for step in steps {
        let box_num = hash(&step.label) as u8;
        let r#box = boxes.entry(box_num).or_insert(Vec::new());
        let lens_with_same_label = r#box.iter().position(|lens| lens.label == step.label);
        match step.kind {
            StepKind::Insert { focal_length } => {
                (*r#box).push(Lens {
                    label: step.label,
                    focal_length,
                });
                if let Some(i) = lens_with_same_label {
                    (*r#box).swap_remove(i);
                }
            }
            StepKind::Remove => {
                if let Some(i) = lens_with_same_label {
                    (*r#box).remove(i);
                }
            }
        }
    }

    boxes
        .iter()
        .map(|(&box_num, r#box)| {
            r#box
                .iter()
                .enumerate()
                .map(|(i, lens)| focusing_power(box_num, i as u8, lens.focal_length))
                .sum::<u32>()
        })
        .sum()
}

fn main() {
    dbg!(part1(INPUT));
    dbg!(part2(INPUT));
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_hash() {
        assert_eq!(hash("HASH"), 52);
        assert_eq!(hash("rn=1"), 30);
        assert_eq!(hash("cm-"), 253);
        assert_eq!(hash("qp=3"), 97);
        assert_eq!(hash("cm=2"), 47);
        assert_eq!(hash("qp-"), 14);
        assert_eq!(hash("pc=4"), 180);
        assert_eq!(hash("ot=9"), 9);
        assert_eq!(hash("ab=5"), 197);
        assert_eq!(hash("pc-"), 48);
        assert_eq!(hash("pc=6"), 214);
        assert_eq!(hash("ot=7"), 231);
    }

    #[test]
    fn test_part1() {
        assert_eq!(part1(EXAMPLE), 1320);
        assert_eq!(part1(INPUT), 511343);
    }

    #[test]
    fn test_part2() {
        assert_eq!(part2(EXAMPLE), 145);
        assert_eq!(part2(INPUT), 294474);
    }
}
