package main

import (
	"reflect"
	"testing"

	"github.com/garrettr/advent-of-code/go/advent"
)

const example = `3   4
4   3
2   5
1   3
3   9
3   3`

func TestParseInput(t *testing.T) {
	wantLeft := []int{3, 4, 2, 1, 3, 3}
	wantRight := []int{4, 3, 5, 3, 9, 3}

	left, right, err := parseInput(example)

	if err != nil {
		t.Errorf("got err %v, want nil", err)
	}
	if !reflect.DeepEqual(left, wantLeft) {
		t.Errorf("got left %v, want %v", left, wantLeft)
	}
	if !reflect.DeepEqual(right, wantRight) {
		t.Errorf("got right %v, want %v", right, wantRight)
	}
}

type solverTestCase struct {
	name   string
	solver func([]int, []int) int
	input  string
	want   int
}

func TestSolve(t *testing.T) {
	input := advent.GetInput("input.txt")
	testCases := []solverTestCase{
		{
			"Part1_example",
			solvePart1,
			example,
			11,
		},
		{
			"Part1_input",
			solvePart1,
			input,
			2000468,
		},
		{
			"Part2_example",
			solvePart2,
			example,
			31,
		},
		{
			"Part2_input",
			solvePart2,
			input,
			18567089,
		},
	}

	for _, tc := range testCases {
		t.Run(tc.name, func(t *testing.T) {
			left, right, err := parseInput(tc.input)
			if err != nil {
				t.Fatalf("parseInput got err %v, want nil", err)
			}

			solution := tc.solver(left, right)
			if solution != tc.want {
				t.Fatalf("got solution %v, want %v", solution, tc.want)
			}
		})
	}
}
