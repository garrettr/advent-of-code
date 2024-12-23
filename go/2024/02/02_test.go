package main

import (
	"reflect"
	"testing"
)

const example = `7 6 4 2 1
1 2 7 8 9
9 7 6 2 1
1 3 2 4 5
8 6 4 4 1
1 3 6 7 9`

func TestParseInput(t *testing.T) {
	wantParsed := [][]int{
		{7, 6, 4, 2, 1},
		{1, 2, 7, 8, 9},
		{9, 7, 6, 2, 1},
		{1, 3, 2, 4, 5},
		{8, 6, 4, 4, 1},
		{1, 3, 6, 7, 9},
	}

	parsed, err := parseInput(example)

	if err != nil {
		t.Errorf("got err %v, want nil", err)
	}
	if !reflect.DeepEqual(parsed, wantParsed) {
		t.Errorf("got parsed %v, want %v", parsed, wantParsed)
	}
}

// TestCase represents a single test scenario for solving puzzle parts
type TestCase struct {
	name   string
	solver func([][]int) int
	input  string
	want   int
}

func TestSolve(t *testing.T) {
	input := getInput("input.txt")
	testCases := []TestCase{
		{"Part1_example", solvePart1, example, 2},
		{"Part1_input", solvePart1, input, 660},
		{"Part2_example", solvePart2, example, 4},
		{"Part2_input", solvePart2, input, 689},
	}

	for _, tc := range testCases {
		t.Run(tc.name, func(t *testing.T) {
			parsed, err := parseInput(tc.input)
			if err != nil {
				t.Fatalf("parseInput got err %v, want nil", err)
			}

			solution := tc.solver(parsed)
			if solution != tc.want {
				t.Fatalf("got solution %v, want %v", solution, tc.want)
			}
		})
	}
}
