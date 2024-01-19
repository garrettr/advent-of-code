use std::{
    cmp::Reverse,
    collections::{BinaryHeap, HashMap, HashSet},
    convert::Infallible,
    str::FromStr,
};

const EXAMPLE: &str = include_str!("example.txt");
const EXAMPLE2: &str = include_str!("example2.txt");
const INPUT: &str = include_str!("input.txt");

#[derive(Debug, Default, PartialEq, Eq, Hash, PartialOrd, Ord, Clone, Copy)]
struct GridPoint(i32, i32);

impl std::ops::Add for GridPoint {
    type Output = GridPoint;

    fn add(self, other: GridPoint) -> GridPoint {
        GridPoint(self.0 + other.0, self.1 + other.1)
    }
}

#[derive(Debug, PartialEq)]
struct Grid(HashMap<GridPoint, i32>);

#[derive(Debug, PartialEq)]
enum GridError {
    TryFromIntError(std::num::TryFromIntError),
    ToDigitError(char),
}

impl std::fmt::Display for GridError {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        match self {
            Self::TryFromIntError(e) => write!(f, "{}", e),
            Self::ToDigitError(c) => write!(f, "expected digit, got {}", c),
        }
    }
}

impl From<std::num::TryFromIntError> for GridError {
    fn from(e: std::num::TryFromIntError) -> Self {
        Self::TryFromIntError(e)
    }
}

// TODO: This was required for `i32::try_from(row)?`, but why?
impl From<Infallible> for GridError {
    fn from(_: Infallible) -> Self {
        unreachable!();
    }
}

impl FromStr for Grid {
    type Err = GridError;

    fn from_str(s: &str) -> Result<Self, Self::Err> {
        let mut grid = HashMap::new();
        for (row, line) in s.lines().enumerate() {
            for (col, c) in line.chars().enumerate() {
                let row = i32::try_from(row)?;
                let col = i32::try_from(col)?;
                let c = c.to_digit(10).ok_or(Self::Err::ToDigitError(c))?;
                grid.insert(GridPoint(row, col), c.try_into()?);
            }
        }
        Ok(Grid(grid))
    }
}

#[derive(Debug)]
enum Rotation {
    Clockwise,
    CounterClockwise,
}

#[derive(Debug, Clone, Copy, Default, PartialEq, Eq, PartialOrd, Ord, Hash)]
enum Direction {
    Up,
    #[default]
    Right,
    Down,
    Left,
}

#[derive(Debug, PartialEq)]
enum DirectionError {
    InvalidDiscriminant(i8),
}

impl std::fmt::Display for DirectionError {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        match self {
            Self::InvalidDiscriminant(n) => write!(f, "invalid discriminant: {}", n),
        }
    }
}

impl TryFrom<i8> for Direction {
    type Error = DirectionError;

    fn try_from(v: i8) -> Result<Self, Self::Error> {
        match v {
            0 => Ok(Direction::Up),
            1 => Ok(Direction::Right),
            2 => Ok(Direction::Down),
            3 => Ok(Direction::Left),
            _ => Err(DirectionError::InvalidDiscriminant(v)),
        }
    }
}

impl Direction {
    fn rotate(&self, towards: Rotation) -> Self {
        let offset = match towards {
            Rotation::Clockwise => 1,
            Rotation::CounterClockwise => -1,
        };
        Direction::try_from((*self as i8 + offset).rem_euclid(4))
            .expect("rem_euclid(4) should ensure this value is a valid discriminant")
    }

    fn offset(&self) -> GridPoint {
        match self {
            Direction::Up => GridPoint(-1, 0),
            Direction::Right => GridPoint(0, 1),
            Direction::Down => GridPoint(1, 0),
            Direction::Left => GridPoint(0, -1),
        }
    }
}

#[derive(Debug, Default, PartialEq, Eq, Hash, PartialOrd, Ord, Clone, Copy)]
struct Position {
    loc: GridPoint,
    facing: Direction,
}

impl Position {
    fn next(&self) -> GridPoint {
        self.loc + self.facing.offset()
    }

    fn step(&self) -> Self {
        Self {
            loc: self.next(),
            facing: self.facing,
        }
    }

    fn rotate_and_step(&self, towards: Rotation) -> Self {
        Self {
            loc: self.loc,
            facing: self.facing.rotate(towards),
        }
        .step()
    }
}

#[derive(Debug, Default, PartialEq, Eq, PartialOrd, Ord)]
struct State {
    cost: i32,
    pos: Position,
    steps: i32,
}

fn find_target(raw_grid: &str) -> GridPoint {
    let rows = raw_grid.lines().count();
    let cols = raw_grid.lines().nth(0).unwrap_or("").chars().count();
    GridPoint(
        (rows - 1).try_into().unwrap(),
        (cols - 1).try_into().unwrap(),
    )
}

fn _solve(input: &str, min_steps: i32, max_steps: i32) -> i32 {
    let grid: Grid = input.parse().expect("grid should be parsed");
    let target = find_target(input);

    // Start walking in both directions.
    let mut queue = BinaryHeap::from([
        Reverse(State {
            pos: Position {
                loc: GridPoint(0, 0),
                facing: Direction::Down,
            },
            ..Default::default()
        }),
        Reverse(State {
            pos: Position {
                loc: GridPoint(0, 0),
                facing: Direction::Right,
            },
            ..Default::default()
        }),
    ]);
    let mut seen: HashSet<(Position, i32)> = HashSet::new();

    while let Some(state) = queue.pop() {
        let State { cost, pos, steps } = state.0;

        if pos.loc == target && steps >= min_steps {
            return cost;
        }

        if seen.contains(&(pos, steps)) {
            continue;
        }
        seen.insert((pos, steps));

        if steps >= min_steps {
            let left = pos.rotate_and_step(Rotation::CounterClockwise);
            if grid.0.contains_key(&left.loc) {
                queue.push(Reverse(State {
                    cost: cost + grid.0[&left.loc],
                    pos: left,
                    steps: 1,
                }));
            }

            let right = pos.rotate_and_step(Rotation::Clockwise);
            if grid.0.contains_key(&right.loc) {
                queue.push(Reverse(State {
                    cost: cost + grid.0[&right.loc],
                    pos: right,
                    steps: 1,
                }));
            }
        }

        let forward = pos.step();
        if steps < max_steps && grid.0.contains_key(&forward.loc) {
            queue.push(Reverse(State {
                cost: cost + grid.0[&forward.loc],
                pos: forward,
                steps: steps + 1,
            }));
        }
    }

    -1
}

fn part1(input: &str) -> i32 {
    _solve(input, 0, 3)
}

fn part2(input: &str) -> i32 {
    _solve(input, 4, 10)
}

fn main() {
    dbg!(part1(INPUT));
    dbg!(part2(INPUT));
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_grid() {
        let s = "12\n34";
        let expected = Grid(HashMap::from([
            (GridPoint(0, 0), 1),
            (GridPoint(0, 1), 2),
            (GridPoint(1, 0), 3),
            (GridPoint(1, 1), 4),
        ]));
        assert_eq!(s.parse(), Ok(expected));

        let s = "12\n3j";
        assert_eq!(s.parse::<Grid>(), Err(GridError::ToDigitError('j')));
    }

    #[test]
    fn test_direction() {
        assert_eq!(
            Direction::try_from(-1),
            Err(DirectionError::InvalidDiscriminant(-1))
        );
        assert_eq!(
            Direction::try_from(4),
            Err(DirectionError::InvalidDiscriminant(4))
        );

        assert_eq!(Direction::Up.rotate(Rotation::Clockwise), Direction::Right);
        assert_eq!(
            Direction::Up.rotate(Rotation::CounterClockwise),
            Direction::Left
        );
        assert_eq!(
            Direction::Down
                .rotate(Rotation::Clockwise)
                .rotate(Rotation::Clockwise),
            Direction::Up
        );
    }

    #[test]
    fn test_position() {
        let position = Position {
            loc: GridPoint(0, 0),
            facing: Direction::Right,
        };

        assert_eq!(position.next(), GridPoint(0, 1));

        assert_eq!(
            position.step(),
            Position {
                loc: GridPoint(0, 1),
                facing: Direction::Right
            }
        );
        assert_eq!(
            position.step().step(),
            Position {
                loc: GridPoint(0, 2),
                facing: Direction::Right,
            }
        );

        assert_eq!(
            position.rotate_and_step(Rotation::Clockwise),
            Position {
                loc: GridPoint(1, 0),
                facing: Direction::Down,
            }
        );
        assert_eq!(
            position.rotate_and_step(Rotation::CounterClockwise),
            Position {
                loc: GridPoint(-1, 0),
                facing: Direction::Up
            }
        );
        assert_eq!(
            position
                .rotate_and_step(Rotation::CounterClockwise)
                .rotate_and_step(Rotation::CounterClockwise),
            Position {
                loc: GridPoint(-1, -1),
                facing: Direction::Left,
            }
        );
        assert_eq!(
            position
                .rotate_and_step(Rotation::CounterClockwise)
                .rotate_and_step(Rotation::Clockwise),
            Position {
                loc: GridPoint(-1, 1),
                facing: Direction::Right,
            }
        );
    }

    #[test]
    fn test_part1() {
        assert_eq!(part1(EXAMPLE), 102);
        assert_eq!(part1(INPUT), 1263);
    }

    #[test]
    fn test_part2() {
        assert_eq!(part2(EXAMPLE), 94);
        assert_eq!(part2(EXAMPLE2), 71);
        assert_eq!(part2(INPUT), 1411);
    }
}
