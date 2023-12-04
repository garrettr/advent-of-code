use regex::Regex;

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

fn parse_games(input: &str) -> Vec<Game> {
    let mut games = Vec::new();
    let game_re = Regex::new(r"^Game (?<id>\d+)").unwrap();
    let cubes_re = Regex::new(r"(?<num>\d+) (?<color>red|green|blue)").unwrap();

    for line in input.lines() {
        let capture = game_re.captures(line).unwrap();
        let id = capture["id"].parse::<u32>().unwrap();

        let mut red = 0;
        let mut green = 0;
        let mut blue = 0;
        for capture in cubes_re.captures_iter(line) {
            match &capture["color"] {
                "red" => red = red.max(capture["num"].parse::<u32>().unwrap()),
                "green" => green = green.max(capture["num"].parse::<u32>().unwrap()),
                "blue" => blue = blue.max(capture["num"].parse::<u32>().unwrap()),
                _ => panic!("Unexpected color"),
            }
        }

        games.push(Game {
            id,
            red,
            green,
            blue,
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
