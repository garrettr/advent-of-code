fn main() {
    let _example = include_str!("example2.txt");
    let input = include_str!("input.txt");
    dbg!(part1(input));
    dbg!(part2(input));
}

fn map_and_sum<F>(input: &str, f: F) -> i32
where
    F: Fn(&str) -> i32,
{
    input.lines().map(f).sum()
}

fn calibration_value(line: &str) -> i32 {
    let digits = line
        .chars()
        .filter_map(|c| c.to_digit(10).map(|n| n as i32))
        .collect::<Vec<i32>>();
    return 10 * digits.first().unwrap() + digits.last().unwrap();
}

fn part1(input: &str) -> String {
    map_and_sum(input, calibration_value).to_string()
}

const DIGITS_AS_STRS: [&str; 9] = ["1", "2", "3", "4", "5", "6", "7", "8", "9"];
const SPELLED_DIGITS: [&str; 9] = [
    "one", "two", "three", "four", "five", "six", "seven", "eight", "nine",
];

fn calibration_value2(line: &str) -> i32 {
    let digits = [DIGITS_AS_STRS, SPELLED_DIGITS].concat();

    let mut first = 0;
    let mut last = 0;
    for i in 0..line.len() {
        if first != 0 && last != 0 {
            break;
        }

        for (j, digit) in digits.iter().enumerate() {
            let digit_as_int = if j < 9 { j as i32 + 1 } else { j as i32 - 8 };
            if first == 0 && line[i..].starts_with(digit) {
                first = digit_as_int;
            }
            if last == 0 && line[line.len() - i - 1..].starts_with(digit) {
                last = digit_as_int;
            }
        }
    }

    return first * 10 + last;
}

fn part2(input: &str) -> String {
    map_and_sum(input, calibration_value2).to_string()
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

    #[test]
    fn test_part2() {
        let example = include_str!("example2.txt");
        let input = include_str!("input.txt");
        assert_eq!(part2(example), "281");
        assert_eq!(part2(input), "54418");
    }
}
