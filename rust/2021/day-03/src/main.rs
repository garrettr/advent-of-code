const EXAMPLE: &str = include_str!("example.txt");
const INPUT: &str = include_str!("input.txt");

fn parse(input: &str) -> Vec<Vec<u32>> {
    input
        .lines()
        .map(|line| line.chars().map(|c| c.to_digit(10).unwrap()).collect())
        .collect()
}

fn transpose(matrix: &Vec<Vec<u32>>) -> Vec<Vec<u32>> {
    let mut result = vec![];
    for i in 0..matrix[0].len() {
        let mut row = vec![];
        for j in 0..matrix.len() {
            row.push(matrix[j][i]);
        }
        result.push(row);
    }
    result
}

fn most_common_bit(row: &[u32]) -> u32 {
    let mut count = vec![0; 2];
    for bit in row {
        count[*bit as usize] += 1;
    }
    if count[0] == count[1] {
        1
    } else if count[0] > count[1] {
        0
    } else {
        1
    }
}

fn least_common_bit(row: &[u32]) -> u32 {
    let mut count = vec![0; 2];
    for bit in row {
        count[*bit as usize] += 1;
    }
    if count[0] == count[1] {
        0
    } else if count[0] > count[1] {
        1
    } else {
        0
    }
}

fn convert_bits_to_int(bits: &[u32]) -> u32 {
    bits.iter().fold(0, |acc, bit| acc * 2 + bit)
}

fn find_gamma_or_epsilon_rate(matrix: &Vec<Vec<u32>>, eval: fn(&[u32]) -> u32) -> u32 {
    let bits: Vec<u32> = matrix.iter().map(|row| eval(row)).collect();
    convert_bits_to_int(&bits)
}

fn part1(input: &str) -> u32 {
    let matrix = transpose(&parse(input));
    let gamma_rate = find_gamma_or_epsilon_rate(&matrix, most_common_bit);
    let epsilon_rate = find_gamma_or_epsilon_rate(&matrix, least_common_bit);
    gamma_rate * epsilon_rate
}

fn find_o2_generator_or_co2_scrubber_rating(
    bits: &Vec<Vec<u32>>,
    bit_criterion: fn(&[u32]) -> u32,
) -> u32 {
    let mut bits = bits.clone();
    let mut bits_by_position = transpose(&bits);
    for position in 0..bits_by_position.len() {
        if bits.len() == 1 {
            break;
        }
        let bit = bit_criterion(&bits_by_position[position]);
        bits.retain(|row| row[position] == bit);
        bits_by_position = transpose(&bits);
    }
    convert_bits_to_int(&bits[0])
}

fn part2(input: &str) -> u32 {
    let bits = parse(input);
    let o2_generator_rating = find_o2_generator_or_co2_scrubber_rating(&bits, most_common_bit);
    let co2_scrubber_rating = find_o2_generator_or_co2_scrubber_rating(&bits, least_common_bit);
    o2_generator_rating * co2_scrubber_rating
}

fn main() {
    dbg!(part1(INPUT));
    dbg!(part2(INPUT));
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_parse() {
        assert_eq!(parse("011010"), vec![vec![0, 1, 1, 0, 1, 0]]);
        assert_eq!(
            parse("110110\n101010"),
            vec![vec![1, 1, 0, 1, 1, 0], vec![1, 0, 1, 0, 1, 0]]
        );
    }

    #[test]
    fn test_transpose() {
        assert_eq!(
            transpose(&vec![vec![1, 2, 3], vec![4, 5, 6]]),
            vec![vec![1, 4], vec![2, 5], vec![3, 6]]
        );
    }

    #[test]
    fn test_most_common_bit() {
        assert_eq!(most_common_bit(&[0, 0, 1]), 0);
        assert_eq!(most_common_bit(&[0, 1, 1]), 1);
        assert_eq!(most_common_bit(&[0, 1, 0, 1]), 1);
        assert_eq!(most_common_bit(&[0, 1, 1, 0, 1, 0]), 1);
        assert_eq!(most_common_bit(&[0, 1, 0, 0, 1, 0]), 0);
    }

    #[test]
    fn test_least_common_bit() {
        assert_eq!(least_common_bit(&[0, 0, 1]), 1);
        assert_eq!(least_common_bit(&[0, 1, 1]), 0);
        assert_eq!(least_common_bit(&[0, 1, 0, 1]), 0);
        assert_eq!(least_common_bit(&[0, 1, 1, 0, 1, 0]), 0);
        assert_eq!(least_common_bit(&[0, 1, 0, 0, 1, 0]), 1);
    }

    #[test]
    fn test_convert_bits_to_ints() {
        assert_eq!(convert_bits_to_int(&[0]), 0);
        assert_eq!(convert_bits_to_int(&[1]), 1);
        assert_eq!(convert_bits_to_int(&[1, 0, 1, 0]), 10);
        assert_eq!(convert_bits_to_int(&[1, 0, 1, 1, 0, 1]), 45);
    }

    #[test]
    fn test_find_gamma_or_epsilon_rate() {
        let matrix = transpose(&parse(EXAMPLE));
        assert_eq!(find_gamma_or_epsilon_rate(&matrix, most_common_bit), 22);
        assert_eq!(find_gamma_or_epsilon_rate(&matrix, least_common_bit), 9);
    }

    #[test]
    fn test_find_o2_generator_or_co2_scrubber_rating() {
        let bits = parse(EXAMPLE);
        dbg!(&bits);
        assert_eq!(
            find_o2_generator_or_co2_scrubber_rating(&bits, most_common_bit),
            23
        );
        assert_eq!(
            find_o2_generator_or_co2_scrubber_rating(&bits, least_common_bit),
            10
        );
    }

    #[test]
    fn test_part1() {
        assert_eq!(part1(EXAMPLE), 198);
        assert_eq!(part1(INPUT), 2972336);
    }

    #[test]
    fn test_part2() {
        assert_eq!(part2(EXAMPLE), 230);
        assert_eq!(part2(INPUT), 3368358);
    }
}
