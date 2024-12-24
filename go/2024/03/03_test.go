package main

import (
	"testing"
)

const example = "xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))"

type TestCase struct {
	name   string
	solver func(string) int
	input  string
	want   int
}

func TestSolve(t *testing.T) {
	input := getInput("input.txt")
	testCases := []TestCase{
		{"Part1_example", solvePart1, example, 161},
		{"Part1_input", solvePart1, input, 184576302},
		// {"Part2_example", solvePart2, example, 4},
		// {"Part2_input", solvePart2, input, 689},
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
