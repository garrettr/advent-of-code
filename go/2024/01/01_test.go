package main

import (
	"reflect"
	"testing"
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
		t.Errorf("got slice1 %v, want %v", left, wantLeft)
	}
	if !reflect.DeepEqual(right, wantRight) {
		t.Errorf("got slice2 %v, want %v", right, wantRight)
	}
}

func TestSolvePart1(t *testing.T) {
	input := getInput("input.txt")
	testCases := map[string]int{
		example: 11,
		input:   2000468,
	}

	for testCase, wantSolution := range testCases {
		left, right, err := parseInput(testCase)
		if err != nil {
			t.Fatalf("got err %v, want nil", err)
		}

		solution := solvePart1(left, right)
		if solution != wantSolution {
			t.Fatalf("got solution %v, want %v", solution, wantSolution)
		}
	}
}

func TestSolvePart2(t *testing.T) {
	input := getInput("input.txt")
	testCases := map[string]int{
		example: 31,
		input:   18567089,
	}

	for testCase, wantSolution := range testCases {
		left, right, err := parseInput(testCase)
		if err != nil {
			t.Fatalf("got err %v, want nil", err)
		}

		solution := solvePart2(left, right)
		if solution != wantSolution {
			t.Fatalf("got solution %v, want %v", solution, wantSolution)
		}
	}
}
