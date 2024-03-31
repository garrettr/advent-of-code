use std::collections::{HashMap, HashSet};

const EXAMPLE: &str = include_str!("example.txt");
const INPUT: &str = include_str!("input.txt");

#[derive(Debug, PartialEq, Eq, Hash, Clone, Copy)]
struct GridPoint(i8, i8);

#[derive(Debug)]
struct Grid(HashMap<GridPoint, u8>);

impl Grid {
    fn from_str(s: &str) -> Self {
        let mut inner = HashMap::new();
        for (row, line) in s.lines().enumerate() {
            for (col, c) in line.chars().enumerate() {
                inner.insert(
                    GridPoint(row.try_into().unwrap(), col.try_into().unwrap()),
                    c.to_digit(10).unwrap().try_into().unwrap(),
                );
            }
        }
        Self(inner)
    }

    fn find_adjacent(&self, point: &GridPoint) -> Vec<GridPoint> {
        let mut adjacent: Vec<GridPoint> = Vec::with_capacity(4);
        for (x_offset, y_offset) in [-1, 1, 0, 0].iter().zip([0, 0, -1, 1].iter()) {
            let point = GridPoint(point.0 + x_offset, point.1 + y_offset);
            if self.0.contains_key(&point) {
                adjacent.push(point);
            }
        }
        adjacent
    }

    fn find_low_points(&self) -> Vec<GridPoint> {
        let mut low_points = Vec::new();
        for (point, height) in self.0.iter() {
            let heights = self
                .find_adjacent(point)
                .iter()
                .map(|point| self.0[point])
                .collect::<Vec<_>>();
            if height < heights.iter().min().unwrap() {
                low_points.push(point.clone());
            }
        }
        low_points
    }

    fn find_basins(&self) -> Vec<HashSet<GridPoint>> {
        let mut basins = Vec::new();
        for low_point in self.find_low_points() {
            let mut basin: HashSet<GridPoint> = HashSet::new();
            let mut candidates = vec![low_point];
            while !candidates.is_empty() {
                let point = candidates.pop().unwrap();
                if self.0[&point] < 9 {
                    basin.insert(point);
                    let adjacent_points = self
                        .find_adjacent(&point)
                        .into_iter()
                        .collect::<HashSet<_>>();
                    let unvisted = &adjacent_points - &basin;
                    candidates.extend(unvisted.into_iter());
                }
            }
            basins.push(basin);
        }
        basins
    }
}

fn part1(input: &str) -> u32 {
    let grid = Grid::from_str(input);
    let low_points = grid.find_low_points();
    low_points
        .iter()
        .map(|low_point| grid.0[low_point] as u32 + 1)
        .sum()
}

fn part2(input: &str) -> u32 {
    let grid = Grid::from_str(input);
    let mut basins = grid.find_basins();
    basins.sort_by_key(|basin| basin.len());
    basins
        .iter()
        .rev()
        .take(3)
        .map(|basin| basin.len() as u32)
        .product()
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
        assert_eq!(part1(EXAMPLE), 15);
        assert_eq!(part1(INPUT), 458);
    }

    #[test]
    fn test_part2() {
        assert_eq!(part2(EXAMPLE), 1134);
        assert_eq!(part2(INPUT), 1391940);
    }
}
