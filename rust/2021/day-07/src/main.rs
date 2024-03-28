const EXAMPLE: &str = include_str!("example.txt");
const INPUT: &str = include_str!("input.txt");

fn parse(input: &str) -> Vec<u64> {
    input
        .trim()
        .split(',')
        .map(|s| s.parse::<u64>().unwrap())
        .collect()
}

fn part1_fuel_cost(crab_position: u64, position: u64) -> u64 {
    crab_position.abs_diff(position)
}

fn range_sum(n: u64) -> u64 {
    n * (n + 1) / 2
}

fn part2_fuel_costs(crab_position: u64, position: u64) -> u64 {
    range_sum(crab_position.abs_diff(position))
}

fn calculate_fuel_costs(crab_positions: &[u64], cost_fn: fn(u64, u64) -> u64) -> Vec<u64> {
    let fueling_position_range =
        *crab_positions.iter().min().unwrap()..=*crab_positions.iter().max().unwrap();
    fueling_position_range
        .map(|position| {
            crab_positions
                .iter()
                .map(|&crab_position| cost_fn(crab_position, position))
                .sum()
        })
        .collect()
}

fn part1(input: &str) -> u64 {
    let crab_positions = parse(input);
    let fuel_costs = calculate_fuel_costs(&crab_positions, part1_fuel_cost);
    *fuel_costs.iter().min().unwrap()
}

fn part2(input: &str) -> u64 {
    let crab_positions = parse(input);
    let fuel_costs = calculate_fuel_costs(&crab_positions, part2_fuel_costs);
    *fuel_costs.iter().min().unwrap()
}

fn main() {
    dbg!(part1(EXAMPLE));
    dbg!(part2(EXAMPLE));
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_parse() {
        assert_eq!(parse("16,1,2,0,4"), vec![16, 1, 2, 0, 4]);
    }

    #[test]
    fn test_part1() {
        assert_eq!(part1(EXAMPLE), 37);
        assert_eq!(part1(INPUT), 341534);
    }

    #[test]
    fn test_part2() {
        assert_eq!(part2(EXAMPLE), 168);
        assert_eq!(part2(INPUT), 93397632);
    }
}
