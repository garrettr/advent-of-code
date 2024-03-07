const EXAMPLE: &str = include_str!("example.txt");
const INPUT: &str = include_str!("input.txt");

fn parse(input: &str) -> Vec<i32> {
    input
        .lines()
        .map(|line| line.parse().unwrap())
        .collect::<Vec<i32>>()
}

fn part1(input: &str) -> i32 {
    parse(input)
        .windows(2)
        .map(|window| if window[0] < window[1] { 1 } else { 0 })
        .sum()
}

fn part2(input: &str) -> i32 {
    parse(input)
        .windows(3)
        .map(|window| window.iter().sum::<i32>())
        .collect::<Vec<_>>()
        .windows(2)
        .map(|window| if window[0] < window[1] { 1 } else { 0 })
        .sum()
}

fn main() {
    dbg!(part1(EXAMPLE));
    // dbg!(part2(INPUT));
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_part1() {
        assert_eq!(part1(EXAMPLE), 7);
        assert_eq!(part1(INPUT), 1711);
    }

    #[test]
    fn test_part2() {
        assert_eq!(part2(EXAMPLE), 5);
        assert_eq!(part2(INPUT), 1743);
    }
}
