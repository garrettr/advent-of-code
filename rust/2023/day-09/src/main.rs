use std::iter::zip;

const EXAMPLE: &str = include_str!("example.txt");
const INPUT: &str = include_str!("input.txt");

fn parse_histories(s: &str) -> Vec<Vec<i32>> {
    s.lines()
        .map(|line| {
            line.split_whitespace()
                .map(|n| n.parse::<i32>().unwrap())
                .collect::<Vec<_>>()
        })
        .collect()
}

fn analyze_history(history: Vec<i32>) -> Vec<Vec<i32>> {
    let mut analysis = vec![history];
    while !analysis.last().unwrap().iter().all(|&x| x == 0) {
        let last = analysis.last().expect("At least one element in analysis");
        let differences: Vec<_> = zip(last.iter(), last[1..].iter())
            .map(|(a, b)| b - a)
            .collect();
        analysis.push(differences);
    }
    analysis
}

fn extrapolate_next(analysis: &mut Vec<Vec<i32>>) -> i32 {
    for i in (0..analysis.len()).rev() {
        if i == analysis.len() - 1 {
            analysis[i].push(0);
        } else {
            let extrapolated = analysis[i].last().unwrap() + analysis[i + 1].last().unwrap();
            analysis[i].push(extrapolated);
        }
    }
    *analysis[0].last().unwrap()
}

fn extrapolate_back(analysis: &mut Vec<Vec<i32>>) -> i32 {
    for i in (0..analysis.len()).rev() {
        if i == analysis.len() - 1 {
            analysis[i].insert(0, 0);
        } else {
            let extrapolated = analysis[i].first().unwrap() - analysis[i + 1].first().unwrap();
            analysis[i].insert(0, extrapolated);
        }
    }
    *analysis[0].first().unwrap()
}

fn part1(input: &str) -> i32 {
    let histories: Vec<Vec<i32>> = parse_histories(input);
    histories
        .into_iter()
        .map(|history| analyze_history(history))
        .map(|mut analysis| extrapolate_next(&mut analysis))
        .sum()
}

fn part2(input: &str) -> i32 {
    parse_histories(input)
        .into_iter()
        .map(|history| analyze_history(history))
        .map(|mut analysis| extrapolate_back(&mut analysis))
        .sum()
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
        assert_eq!(part1(EXAMPLE), 114);
        assert_eq!(part1(INPUT), 1789635132);
    }

    #[test]
    fn test_part2() {
        assert_eq!(part2(EXAMPLE), 2);
        assert_eq!(part2(INPUT), 913);
    }
}
