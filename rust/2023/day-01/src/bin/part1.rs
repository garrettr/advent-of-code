fn main() {
    let input = include_str!("input.txt");
    let output = part1(input);
    dbg!(output);
}

fn calibration_value(line: &str) -> i32 {
    let digits = line
        .chars()
        .filter_map(|c| c.to_digit(10).map(|n| n as i32))
        .collect::<Vec<i32>>();
    return 10 * digits.first().unwrap() + digits.last().unwrap();
}

fn part1(input: &str) -> String {
    input
        .lines()
        .map(calibration_value)
        .sum::<i32>()
        .to_string()
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_part1() {
        let example = include_str!("example.txt");
        let input = include_str!("input.txt");
        assert_eq!(part1(example), "142");
        assert_eq!(part1(input), "54304");
    }
}
