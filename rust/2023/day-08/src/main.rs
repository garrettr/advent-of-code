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

impl<'a> Map<'a> {
    const NODE_RE: Lazy<Regex> = Lazy::new(|| {
        Regex::new(r"(?<id>[A-Z0-9]{3}) = \((?<left>[A-Z0-9]{3}), (?<right>[A-Z0-9]{3})\)").unwrap()
    });

    fn from_str(s: &'a str) -> Map<'a> {
        let (instructions, rest) = s.split_once("\n\n").unwrap();

        let mut nodes = HashMap::with_capacity(rest.lines().count());
        for line in rest.lines() {
            let (_full, [id, left, right]) = Self::NODE_RE
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

    fn navigate(&self, start: &str, end: &str) -> u64 {
        let mut steps = 0;
        let mut node = start;
        for (step, instruction) in self.instructions.chars().cycle().enumerate() {
            if node.ends_with(end) {
                steps = step;
                break;
            }
            node = match instruction {
                'L' => self.nodes[node].0,
                'R' => self.nodes[node].1,
                _ => panic!("Invalid node: {:?}", node),
            }
        }
        steps as u64
    }
}

fn part1(input: &str) -> u64 {
    let map = Map::from_str(input);
    map.navigate("AAA", "ZZZ")
}

fn gcd(mut n: u64, mut m: u64) -> u64 {
    assert!(n != 0 && m != 0);
    while m != 0 {
        if m < n {
            std::mem::swap(&mut m, &mut n);
        }
        m %= n;
    }
    n
}

fn lcm(a: u64, b: u64) -> u64 {
    (a * b) / gcd(a, b)
}

fn part2(input: &str) -> u64 {
    let map = Map::from_str(input);
    let start_nodes: Vec<_> = map
        .nodes
        .keys()
        .filter(|&node| node.ends_with('A'))
        .collect();
    let path_lens: Vec<_> = start_nodes
        .iter()
        .map(|start_node| map.navigate(start_node, "Z"))
        .collect();
    path_lens.into_iter().reduce(|acc, x| lcm(acc, x)).unwrap()
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
        assert_eq!(part1(EXAMPLE), 2);
        assert_eq!(part1(EXAMPLE2), 6);
        assert_eq!(part1(INPUT), 19667);
    }

    #[test]
    fn test_part2() {
        assert_eq!(part2(EXAMPLE3), 6);
        assert_eq!(part2(INPUT), 19185263738117);
    }
}
