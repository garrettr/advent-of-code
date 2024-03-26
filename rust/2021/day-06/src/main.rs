const EXAMPLE: &str = include_str!("example.txt");
const INPUT: &str = include_str!("input.txt");

// Instead of tracking each individual fish, just keep track of the sum of fish
// per day in the 7 day cycle. Add 2 days to the cycle for new fish, which spawn
// with their internal timer set to 8 days.
struct SpawnCycle([u64; 9]);

impl SpawnCycle {
    fn from_str(s: &str) -> Self {
        let mut cycle = [0; 9];
        for fish in s.trim().split(',').map(|s| s.parse::<usize>().unwrap()) {
            cycle[fish] += 1;
        }
        Self(cycle)
    }

    fn simulate_day(&mut self) {
        // Aging
        let mut prev_day_count = self.0.last().unwrap().clone();
        for day in (1..self.0.len()).rev() {
            let curr_day_count = prev_day_count;
            prev_day_count = self.0[day - 1];
            self.0[day] -= curr_day_count;
            self.0[day - 1] += curr_day_count;
        }
        // Spawning
        self.0[0] -= prev_day_count;
        self.0[6] += prev_day_count;
        self.0[8] += prev_day_count;
    }

    fn simulate(&mut self, days: u64) {
        for _ in 0..days {
            self.simulate_day();
        }
    }

    fn total_fishes(&self) -> u64 {
        self.0.iter().sum()
    }
}

fn part1(input: &str) -> u64 {
    let mut cycle = SpawnCycle::from_str(input);
    cycle.simulate(80);
    cycle.total_fishes()
}

fn part2(input: &str) -> u64 {
    let mut cycle = SpawnCycle::from_str(input);
    cycle.simulate(256);
    cycle.total_fishes()
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
        assert_eq!(part1(EXAMPLE), 5934);
        assert_eq!(part1(INPUT), 391671);
    }

    #[test]
    fn test_part2() {
        assert_eq!(part2(EXAMPLE), 26984457539);
        assert_eq!(part2(INPUT), 1754000560399);
    }
}
