use std::collections::HashSet;

const EXAMPLE: &str = include_str!("example.txt");
const INPUT: &str = include_str!("input.txt");

type Board = [[u32; 5]; 5];

fn parse_board(input: &str) -> Board {
    let mut board = [[0; 5]; 5];
    for (ri, row) in input.lines().enumerate() {
        for (ci, col) in row.split_whitespace().enumerate() {
            board[ri][ci] = col.parse().unwrap();
        }
    }
    board
}

fn parse(input: &str) -> (Vec<u32>, Vec<Board>) {
    let (numbers, boards) = input.trim().split_once("\n\n").unwrap();
    let numbers = numbers.split(',').map(|x| x.parse().unwrap()).collect();
    let boards = boards.split("\n\n").map(|s| parse_board(s)).collect();
    (numbers, boards)
}

fn transpose(board: &Board) -> Board {
    let mut transposed = [[0; 5]; 5];
    for row in 0..5 {
        for col in 0..5 {
            transposed[col][row] = board[row][col];
        }
    }
    transposed
}

fn won(board: &Board, numbers: &[u32]) -> bool {
    let numbers: HashSet<_> = numbers.iter().collect();
    for orthogonal in board.iter().chain(transpose(board).iter()) {
        let orthogonal: HashSet<_> = orthogonal.iter().collect();
        if numbers.is_superset(&orthogonal) {
            return true;
        }
    }
    false
}

fn score(board: &Board, numbers: &[u32]) -> u32 {
    let unmarked_numbers: Vec<_> = board
        .iter()
        .flatten()
        .filter(|n| !numbers.contains(n))
        .collect();
    unmarked_numbers.into_iter().sum::<u32>() * numbers.last().unwrap()
}

fn part1(input: &str) -> u32 {
    let (numbers, boards) = parse(input);
    for i in 5..numbers.len() {
        let drawn = &numbers[..i];
        for board in &boards {
            if won(board, &drawn) {
                return score(board, &drawn);
            }
        }
    }
    unreachable!("solution not found");
}

fn part2(input: &str) -> u32 {
    let (numbers, mut boards) = parse(input);
    for i in 5..numbers.len() {
        let drawn = &numbers[..i];
        let last_board = boards.last().unwrap().clone();
        boards.retain(|board| !won(board, &drawn));
        if boards.len() == 0 {
            return score(&last_board, &drawn);
        }
    }
    unreachable!("solution not found");
}

fn main() {
    dbg!(part1(INPUT));
    dbg!(part2(INPUT));
}

#[cfg(test)]
mod tests {
    use core::num;

    use super::*;

    #[test]
    fn test_parse_board() {
        let input = " 3 15  0  2 22
 9 18 13 17  5
19  8  7 25 23
20 11 10 24  4
14 21 16 12  6";
        let board = [
            [3, 15, 0, 2, 22],
            [9, 18, 13, 17, 5],
            [19, 8, 7, 25, 23],
            [20, 11, 10, 24, 4],
            [14, 21, 16, 12, 6],
        ];
        assert_eq!(parse_board(input), board);
    }

    #[test]
    fn test_parse() {
        let input = "7,4,9,5,11

22 13 17 11  0
8  2 23  4 24
21  9 14 16  7
6 10  3 18  5
1 12 20 15 19";
        let numbers = [7, 4, 9, 5, 11];
        let board = [
            [22, 13, 17, 11, 0],
            [8, 2, 23, 4, 24],
            [21, 9, 14, 16, 7],
            [6, 10, 3, 18, 5],
            [1, 12, 20, 15, 19],
        ];

        let (parsed_numbers, parsed_boards) = parse(input);

        assert_eq!(parsed_numbers, numbers);
        assert_eq!(parsed_boards.len(), 1);
        assert_eq!(parsed_boards[0], board);
    }

    #[test]
    fn test_transpose() {
        let board = [
            [22, 13, 17, 11, 0],
            [8, 2, 23, 4, 24],
            [21, 9, 14, 16, 7],
            [6, 10, 3, 18, 5],
            [1, 12, 20, 15, 19],
        ];
        let transposed = [
            [22, 8, 21, 6, 1],
            [13, 2, 9, 10, 12],
            [17, 23, 14, 3, 20],
            [11, 4, 16, 18, 15],
            [0, 24, 7, 5, 19],
        ];
        assert_eq!(transpose(&board), transposed);
    }

    #[test]
    fn test_part1() {
        assert_eq!(part1(EXAMPLE), 4512);
        assert_eq!(part1(INPUT), 58412);
    }

    #[test]
    fn test_part2() {
        assert_eq!(part2(EXAMPLE), 1924);
        assert_eq!(part2(INPUT), 10030);
    }
}
