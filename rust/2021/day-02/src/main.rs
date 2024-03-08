use std::collections::HashMap;

const EXAMPLE: &str = include_str!("example.txt");
const INPUT: &str = include_str!("input.txt");

fn part1(input: &str) -> i32 {
    let mut commands: HashMap<String, i32> = HashMap::with_capacity(3);
    for line in input.lines() {
        let (command, value) = line
            .split_once(" ")
            .expect("two strings separated by a space");
        let value = value.parse().expect("value is an integer");
        commands
            .entry(command.to_string())
            .and_modify(|v| *v += value)
            .or_insert(value);
    }
    commands["forward"] * (commands["down"] - commands["up"])
}

fn part2(input: &str) -> () {}

fn main() {
    dbg!(part1(EXAMPLE));
    // dbg!(part2(INPUT));
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_part1() {
        assert_eq!(part1(EXAMPLE), 150);
        assert_eq!(part1(INPUT), 1727835);
    }

    #[test]
    fn test_part2() {
        // assert_eq!(part2(EXAMPLE), ());
        // assert_eq!(part2(INPUT), ());
    }
}
