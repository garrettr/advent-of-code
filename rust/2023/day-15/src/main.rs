const EXAMPLE: &str = include_str!("example.txt");
const INPUT: &str = include_str!("input.txt");

fn hash(s: &str) -> u32 {
    s.bytes()
        .fold(0, |acc, byte| ((acc + byte as u32) * 17) % 256)
}

fn part1(input: &str) -> u32 {
    input.trim().split(',').map(|step| hash(step)).sum()
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
    fn test_hash() {
        assert_eq!(hash("HASH"), 52);
        assert_eq!(hash("rn=1"), 30);
        assert_eq!(hash("cm-"), 253);
        assert_eq!(hash("qp=3"), 97);
        assert_eq!(hash("cm=2"), 47);
        assert_eq!(hash("qp-"), 14);
        assert_eq!(hash("pc=4"), 180);
        assert_eq!(hash("ot=9"), 9);
        assert_eq!(hash("ab=5"), 197);
        assert_eq!(hash("pc-"), 48);
        assert_eq!(hash("pc=6"), 214);
        assert_eq!(hash("ot=7"), 231);
    }

    #[test]
    fn test_part1() {
        assert_eq!(part1(EXAMPLE), 1320);
        assert_eq!(part1(INPUT), 511343);
    }

    #[test]
    fn test_part2() {
        // assert_eq!(part2(EXAMPLE), ());
        // assert_eq!(part2(INPUT), ());
    }
}
