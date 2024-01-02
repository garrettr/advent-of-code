use {once_cell::sync::Lazy, regex::Regex, std::collections::HashMap};

#[allow(dead_code)]
const EXAMPLE: &str = include_str!("example.txt");
const INPUT: &str = include_str!("input.txt");

fn main() {
    dbg!(part1(INPUT));
    dbg!(part2(INPUT));
}

#[derive(Debug)]
struct Game {
    id: u32,
    red: u32,
    green: u32,
    blue: u32,
}

static GAME_RE: Lazy<Regex> = Lazy::new(|| Regex::new(r"^Game (?<id>\d+)").unwrap());
static CUBES_RE: Lazy<Regex> =
    Lazy::new(|| Regex::new(r"(?<num>\d+) (?<color>red|green|blue)").unwrap());

fn parse_games(input: &str) -> Vec<Game> {
    let mut games = Vec::new();

    for line in input.lines() {
        let capture = GAME_RE.captures(line).unwrap();
        let id = capture["id"].parse::<u32>().unwrap();

        let mut colors: HashMap<String, u32> = HashMap::with_capacity(3);
        for capture in CUBES_RE.captures_iter(line) {
            let num = capture["num"].parse::<u32>().unwrap();
            let color = capture.name("color").unwrap().as_str().to_owned();
            colors
                .entry(color)
                .and_modify(|count| *count = (*count).max(num))
                .or_insert(num);
        }

        games.push(Game {
            id,
            red: colors["red"],
            green: colors["green"],
            blue: colors["blue"],
        });
    }

    return games;
}

fn game_is_possible(game: &Game, red: u32, green: u32, blue: u32) -> bool {
    game.red <= red && game.green <= green && game.blue <= blue
}

fn part1(input: &str) -> u32 {
    parse_games(input)
        .iter()
        .filter(|game| game_is_possible(game, 12, 13, 14))
        .map(|game| game.id)
        .sum()
}

fn part2(input: &str) -> u32 {
    parse_games(input)
        .iter()
        .map(|game| game.red * game.green * game.blue)
        .sum()
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_part1() {
        assert_eq!(part1(EXAMPLE), 8);
        assert_eq!(part1(INPUT), 2149);
    }

    #[test]
    fn test_part2() {
        assert_eq!(part2(EXAMPLE), 2286);
        assert_eq!(part2(INPUT), 71274);
    }
}
