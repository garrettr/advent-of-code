mod counter;
use counter::Counter;

const EXAMPLE: &str = include_str!("example.txt");
const INPUT: &str = include_str!("input.txt");

#[derive(Debug, PartialEq, Eq, Hash)]
struct Point(u32, u32);

impl Point {
    fn from_input(s: &str) -> Self {
        let (x, y) = s.split_once(',').expect("comma-separated coordinates");
        Self(
            x.parse().expect("integer x coordinate"),
            y.parse().expect("integer y coordinate"),
        )
    }
}

#[derive(Debug, PartialEq, Eq)]
struct Line(Point, Point);

impl Line {
    fn from_input(s: &str) -> Self {
        let (p1, p2) = s
            .split_once(" -> ")
            .expect("two points separated by \" -> \"");
        Self(Point::from_input(p1), Point::from_input(p2))
    }

    fn is_horizontal_or_vertical(&self) -> bool {
        let Line(Point(x1, y1), Point(x2, y2)) = self;
        x1 == x2 || y1 == y2
    }

    fn points(&self) -> Vec<Point> {
        use std::cmp::Ordering::*;
        let Line(Point(x1, y1), Point(x2, y2)) = self;
        // Trait objects for the win!
        let xs: Box<dyn Iterator<Item = u32>> = match x1.cmp(x2) {
            Less => Box::new(*x1..=*x2),
            Equal => Box::new(std::iter::repeat(*x1)),
            Greater => Box::new((*x2..=*x1).rev()),
        };
        let ys: Box<dyn Iterator<Item = u32>> = match y1.cmp(y2) {
            Less => Box::new(*y1..=*y2),
            Equal => Box::new(std::iter::repeat(*y1)),
            Greater => Box::new((*y2..=*y1).rev()),
        };
        xs.zip(ys).map(|(x, y)| Point(x, y)).collect()
    }
}

// TODO: Return an iterator instead of a Vec to avoid unnecessary allocations?
fn parse(input: &str) -> Vec<Line> {
    input.lines().map(|line| Line::from_input(line)).collect()
}

fn part1(input: &str) -> usize {
    let lines = parse(input);
    let horizontal_or_vertical_lines: Vec<_> = lines
        .iter()
        .filter(|line| line.is_horizontal_or_vertical())
        .collect();
    let points: Vec<_> = horizontal_or_vertical_lines
        .iter()
        .map(|line| line.points())
        .flatten()
        .collect();
    let counter: Counter<_> = points.iter().collect();
    let points_with_two_or_more_overlapping_lines: Vec<_> = counter
        .most_common(None)
        .iter()
        .filter_map(|(&point, &count)| if count > 1 { Some(point) } else { None })
        .collect();
    // TODO: try to rework the above into an iterator chain that only
    // `.collect()`s once, at the end.
    points_with_two_or_more_overlapping_lines.len()
}

fn part2(input: &str) -> usize {
    let lines = parse(input);
    let points: Vec<_> = lines.iter().map(|line| line.points()).flatten().collect();
    let counter: Counter<_> = points.iter().collect();
    let points_with_two_or_more_overlapping_lines: Vec<_> = counter
        .most_common(None)
        .into_iter()
        .filter_map(|(&point, &count)| if count > 1 { Some(point) } else { None })
        .collect();
    // TODO: try to rework the above into an iterator chain that only
    // `.collect()`s once, at the end.
    points_with_two_or_more_overlapping_lines.len()
}

fn main() {
    dbg!(part1(INPUT));
    dbg!(part2(INPUT));
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_point_from_input() {
        assert_eq!(Point::from_input("0,9"), Point(0, 9));
        assert_eq!(Point::from_input("7,4"), Point(7, 4));
    }

    #[test]
    fn test_line_from_input() {
        assert_eq!(
            Line::from_input("1,1 -> 1,3"),
            Line(Point(1, 1), Point(1, 3))
        );
        assert_eq!(
            Line::from_input("9,7 -> 7,7"),
            Line(Point(9, 7), Point(7, 7))
        );
    }

    #[test]
    fn test_line_is_horizontal_or_vertical() {
        assert_eq!(
            Line::from_input("1,1 -> 1,3").is_horizontal_or_vertical(),
            true
        );
        assert_eq!(
            Line::from_input("9,7 -> 7,7").is_horizontal_or_vertical(),
            true
        );
        assert_eq!(
            Line::from_input("1,1 -> 3,3").is_horizontal_or_vertical(),
            false
        );
        assert_eq!(
            Line::from_input("9,7 -> 7,9").is_horizontal_or_vertical(),
            false
        );
    }

    #[test]
    fn test_points() {
        assert_eq!(
            Line::from_input("1,1 -> 1,3").points(),
            vec![Point(1, 1), Point(1, 2), Point(1, 3)]
        );
        assert_eq!(
            Line::from_input("9,7 -> 7,7").points(),
            vec![Point(9, 7), Point(8, 7), Point(7, 7)]
        );
        assert_eq!(
            Line::from_input("1,1 -> 3,3").points(),
            vec![Point(1, 1), Point(2, 2), Point(3, 3)]
        );
        assert_eq!(
            Line::from_input("9,7 -> 7,9").points(),
            vec![Point(9, 7), Point(8, 8), Point(7, 9)]
        );
    }

    #[test]
    fn test_part1() {
        assert_eq!(part1(EXAMPLE), 5);
        assert_eq!(part1(INPUT), 7414);
    }

    #[test]
    fn test_part2() {
        assert_eq!(part2(EXAMPLE), 12);
        assert_eq!(part2(INPUT), 19676);
    }
}
