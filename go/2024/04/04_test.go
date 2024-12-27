package main

import (
	"testing"

	"github.com/garrettr/advent-of-code/go/advent"
)

const example = `MMMSXXMASM
MSAMXMSMSA
AMXSXMAAMM
MSAMASMSMX
XMASAMXAMM
XXAMMXXAMA
SMSMSASXSS
SAXAMASAAA
MAMMMXMMMM
MXMXAXMASX`

func TestSolve(t *testing.T) {
	input := advent.GetInput("input.txt")
	testCases := map[string]advent.TestCase{
		"Part1_example": {Solver: solvePart1, Input: example, Want: 18},
		"Part1_input":   {Solver: solvePart1, Input: input, Want: 2454},
		// "Part2_example": {Solver: solvePart2, Input: example2, Want: 48},
		// "Part2_input":   {Solver: solvePart2, Input: input, Want: 118173507},
	}
	advent.RunSolveTests(t, testCases)
}
