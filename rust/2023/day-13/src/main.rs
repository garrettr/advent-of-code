use std::iter::zip;

const EXAMPLE: &str = include_str!("example.txt");
const INPUT: &str = include_str!("input.txt");

fn distance(l: &str, r: &str) -> i32 {
    zip(l.bytes(), r.bytes())
        .map(|(a, b)| if a == b { 0 } else { 1 })
        .sum()
}

fn reflection_row(pattern: &[&str]) -> Option<i32> {
    for i in 1..pattern.len() {
        let (left, right) = pattern.split_at(i);
        if zip(left.iter().rev(), right)
            .map(|(&l, &r)| distance(l, r))
            .sum::<i32>()
            == 0
        {
            return Some(i as i32);
        }
    }
    None
}

fn transpose(input: &[&str]) -> Vec<String> {
    if input.is_empty() {
        return Vec::new();
    }

    let row_len = input[0].len();
    let mut transposed = vec![String::with_capacity(input.len()); row_len];
    for row in input {
        for (i, ch) in row.chars().enumerate() {
            transposed[i].push(ch);
        }
    }

    transposed
}

fn summarize(pattern: &str) -> i32 {
    let rows: Vec<_> = pattern.split('\n').collect();
    let row = reflection_row(&rows);
    if let Some(row) = row {
        return 100 * row;
    }

    let cols = transpose(&rows);
    let cols_as_str_slices: Vec<&str> = cols.iter().map(AsRef::as_ref).collect();
    let col = reflection_row(&cols_as_str_slices);
    if let Some(col) = col {
        return col;
    }

    panic!("no reflection found for pattern: {}", pattern);
}

fn part1(input: &str) -> i32 {
    input.split("\n\n").map(|pattern| summarize(pattern)).sum()
}

fn part2(input: &str) -> () {}

fn main() {
    dbg!(part1(INPUT));
    // dbg!(part2(INPUT));
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_part1() {
        assert_eq!(part1(EXAMPLE), 405);
        assert_eq!(part1(INPUT), 29213);
    }

    // #[test]
    // fn test_part2() {
    //     assert_eq!(part2(EXAMPLE), ());
    //     assert_eq!(part2(INPUT), ());
    // }
}
