package main

import (
	"testing"

	"github.com/garrettr/advent-of-code/go/advent"
)

const example = "xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))"
const example2 = "xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))"

func TestSolve(t *testing.T) {
	input := advent.GetInput("input.txt")
	testCases := []advent.TestCase{
		{Name: "Part1_example", Solver: solvePart1, Input: example, Want: 161},
		{Name: "Part1_input", Solver: solvePart1, Input: input, Want: 184576302},
		{Name: "Part2_example", Solver: solvePart2, Input: example2, Want: 48},
		{Name: "Part2_input", Solver: solvePart2, Input: input, Want: 118173507},
	}
	advent.RunSolveTests(t, testCases)
}
