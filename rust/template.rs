const EXAMPLE: &str = include_str!("example.txt");
const INPUT: &str = include_str!("input.txt");

fn part1(input: &str) -> () {}

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
        assert_eq!(part1(EXAMPLE), ());
        // assert_eq!(part1(INPUT), ());
    }

    #[test]
    fn test_part2() {
        // assert_eq!(part2(EXAMPLE), ());
        // assert_eq!(part2(INPUT), ());
    }
}
