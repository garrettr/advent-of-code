use anyhow::{anyhow, Result};

const EXAMPLE: &str = include_str!("example.txt");
const INPUT: &str = include_str!("input.txt");

fn parse(input: &str) -> Result<Vec<i32>> {
    input
        .lines()
        .enumerate()
        .map(|(line_no, line)| {
            line.parse::<i32>()
                .map_err(|err| anyhow!("Error parsing line {}: {}", line_no + 1, err))
        })
        .collect()
}

fn part1(input: &str) -> Result<i32> {
    let depth_measurements = parse(input)?;
    Ok(depth_measurements
        .windows(2)
        .map(|window| if window[0] < window[1] { 1 } else { 0 })
        .sum())
}

fn part2(input: &str) -> Result<i32> {
    let depth_measurements = parse(input)?;
    Ok(depth_measurements
        .windows(3)
        .map(|window| window.iter().sum::<i32>())
        .collect::<Vec<_>>()
        .windows(2)
        .map(|window| if window[0] < window[1] { 1 } else { 0 })
        .sum())
}

fn main() {
    dbg!(part1(EXAMPLE).unwrap());
    dbg!(part2(INPUT).unwrap());
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_parse() {
        let input = "1\n2\n3\n";
        let result = parse(input);
        assert_eq!(result.unwrap(), vec![1, 2, 3]);
    }

    #[test]
    fn test_parse_error() {
        let input = "1\n2\n3\na\n";
        let result = parse(input);
        assert!(result.is_err_and(|result| result.to_string().contains("Error parsing line 4")));
    }

    #[test]
    fn test_part1() {
        assert_eq!(part1(EXAMPLE).unwrap(), 7);
        assert_eq!(part1(INPUT).unwrap(), 1711);
    }

    #[test]
    fn test_part2() {
        assert_eq!(part2(EXAMPLE).unwrap(), 5);
        assert_eq!(part2(INPUT).unwrap(), 1743);
    }
}
