package main

import (
	"testing"

	"github.com/garrettr/advent-of-code/go/advent"
)

const example = "xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))"
const example2 = "xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))"

type TestCase struct {
	name   string
	solver func(string) int
	input  string
	want   int
}

func TestSolve(t *testing.T) {
	input := advent.GetInput("input.txt")
	testCases := []TestCase{
		{"Part1_example", solvePart1, example, 161},
		{"Part1_input", solvePart1, input, 184576302},
		{"Part2_example", solvePart2, example2, 48},
		{"Part2_input", solvePart2, input, 118173507},
	}

	for _, tc := range testCases {
		t.Run(tc.name, func(t *testing.T) {
			solution := tc.solver(tc.input)
			if solution != tc.want {
				t.Fatalf("got solution %v, want %v", solution, tc.want)
			}
		})
	}
}
