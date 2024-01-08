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
    Regex::new(r"(?<id>[A-Z0-9]{3}) = \((?<left>[A-Z0-9]{3}), (?<right>[A-Z0-9]{3})\)").unwrap()
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

fn navigate(map: &Map, start: &str, end: &str) -> i32 {
    let mut steps = 0;
    let mut node = start;
    for (step, instruction) in map.instructions.chars().cycle().enumerate() {
        if node.ends_with(end) {
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

fn part1(input: &str) -> i32 {
    let map = parse_map(input);
    navigate(&map, "AAA", "ZZZ")
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
    let map = parse_map(input);
    let start_nodes = map
        .nodes
        .keys()
        .filter(|&node| node.ends_with('A'))
        .collect::<Vec<_>>();
    let path_lens: Vec<u64> = start_nodes
        .iter()
        .map(|start_node| navigate(&map, start_node, "Z") as u64)
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
