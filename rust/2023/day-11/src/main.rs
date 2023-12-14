use core::cmp::{max, min};
use std::collections::HashSet;

const EXAMPLE: &str = include_str!("example.txt");
const INPUT: &str = include_str!("input.txt");

fn main() {
    dbg!(part1(INPUT));
    // dbg!(part2(INPUT));
}

fn find_rows_to_expand(universe: &Vec<&str>) -> HashSet<usize> {
    let mut rows_to_expand = HashSet::with_capacity(universe.len());
    for ri in 0..universe.len() {
        let mut empty = true;
        for ci in 0..universe[ri].len() {
            if &universe[ri][ci..ci + 1] == "#" {
                empty = false;
                break;
            }
        }
        if empty {
            rows_to_expand.insert(ri);
        }
    }
    rows_to_expand
}

fn find_cols_to_expand(universe: &Vec<&str>) -> HashSet<usize> {
    let mut cols_to_expand = HashSet::with_capacity(universe[0].len());
    for ci in 0..universe[0].len() {
        let mut empty = true;
        for ri in 0..universe.len() {
            if &universe[ri][ci..ci + 1] == "#" {
                empty = false;
                break;
            }
        }
        if empty {
            cols_to_expand.insert(ci);
        }
    }
    cols_to_expand
}

fn find_galaxies(universe: &Vec<&str>) -> Vec<(usize, usize)> {
    let mut galaxies = Vec::new();
    for ri in 0..universe.len() {
        for ci in 0..universe[ri].len() {
            if &universe[ri][ci..ci + 1] == "#" {
                galaxies.push((ri, ci));
            }
        }
    }
    galaxies
}

fn part1(input: &str) -> u64 {
    let universe = input.lines().collect::<Vec<_>>();
    let rows_to_expand = find_rows_to_expand(&universe);
    let cols_to_expand = find_cols_to_expand(&universe);
    let galaxies = find_galaxies(&universe);
    let expansion_factor = 2;

    let mut sum = 0;
    for i in 0..galaxies.len() {
        for j in i + 1..galaxies.len() {
            let g1 = galaxies[i];
            let g2 = galaxies[j];
            let row_start = min(g1.0, g2.0);
            let row_end = max(g1.0, g2.0);
            let col_start = min(g1.1, g2.1);
            let col_end = max(g1.1, g2.1);

            let mut shortest_path = 0;
            for r in row_start..row_end {
                if rows_to_expand.contains(&r) {
                    shortest_path += expansion_factor;
                } else {
                    shortest_path += 1;
                }
            }
            for c in col_start..col_end {
                if cols_to_expand.contains(&c) {
                    shortest_path += expansion_factor;
                } else {
                    shortest_path += 1;
                }
            }
            sum += shortest_path;
        }
    }

    sum
}

fn part2(input: &str) -> () {}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_part1() {
        assert_eq!(part1(EXAMPLE), 374);
        assert_eq!(part1(INPUT), 10313550);
    }

    #[test]
    fn test_part2() {
        // assert_eq!(part2(EXAMPLE), ()));
        // assert_eq!(part2(INPUT), ()));
    }
}
