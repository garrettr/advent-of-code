const EXAMPLE: &str = include_str!("example.txt");
const INPUT: &str = include_str!("input.txt");

fn part1(input: &str) -> i64 {}

fn part2(input: &str) -> i64 {}

fn main() {
    dbg!(part1(EXAMPLE));
    // dbg!(part2(INPUT));
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_part1() {
        assert_eq!(part1(EXAMPLE), 0);
        // assert_eq!(part1(INPUT), 0);
    }

    #[test]
    fn test_part2() {
        // assert_eq!(part2(EXAMPLE), 0);
        // assert_eq!(part2(INPUT), 0);
    }
}
