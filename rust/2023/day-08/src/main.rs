use once_cell::sync::Lazy;
use regex::Regex;
use std::collections::HashMap;

const EXAMPLE: &str = include_str!("example.txt");
const EXAMPLE2: &str = include_str!("example2.txt");
const EXAMPLE3: &str = include_str!("example3.txt");
const INPUT: &str = include_str!("input.txt");

#[derive(Debug)]
struct Map<'a> {
    instructions: &'a str,
    nodes: HashMap<&'a str, (&'a str, &'a str)>,
}

static NODE_RE: Lazy<Regex> = Lazy::new(|| {
    Regex::new(r"(?<id>[A-Z]{3}) = \((?<left>[A-Z]{3}), (?<right>[A-Z]{3})\)").unwrap()
});

fn parse_map<'a>(input: &'a str) -> Map<'a> {
    let (instructions, rest) = input.split_once("\n\n").unwrap();

    let mut nodes = HashMap::with_capacity(rest.lines().count());
    for line in rest.lines() {
        let (_full, [id, left, right]) = NODE_RE
            .captures(line)
            .map(|caps| caps.extract())
            .expect("Node definition matched by regular expression");
        nodes.insert(id, (left, right));
    }

    Map {
        instructions,
        nodes,
    }
}

fn part1(input: &str) -> i32 {
    let map = parse_map(input);
    let mut steps = 0;
    let mut node = "AAA";
    for (step, instruction) in map.instructions.chars().cycle().enumerate() {
        if node == "ZZZ" {
            steps = step;
            break;
        }
        node = match instruction {
            'L' => map.nodes[node].0,
            'R' => map.nodes[node].1,
            _ => panic!("Invalid node: {:?}", node),
        }
    }
    steps as i32
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
    fn test_part1() {
        assert_eq!(part1(EXAMPLE), 2);
        assert_eq!(part1(EXAMPLE2), 6);
        assert_eq!(part1(INPUT), 19667);
    }

    #[test]
    fn test_part2() {
        // assert_eq!(part2(EXAMPLE), ());
        // assert_eq!(part2(INPUT), ());
    }
}
