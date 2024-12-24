package main

import (
	"fmt"
	"log"
	"slices"
	"strconv"
	"strings"

	"github.com/garrettr/advent-of-code/go/advent"
)

// parseInput converts a string of space-separated numbers into a slice of integer slices.
// Each line in the input becomes a slice of integers.
func parseInput(input string) ([][]int, error) {
	lines := strings.Split(strings.TrimSpace(input), "\n")
	parsed := make([][]int, len(lines))
	for i, line := range lines {
		fields := strings.Fields(line)
		ns := make([]int, len(fields))
		for j, field := range fields {
			n, err := strconv.Atoi(field)
			if err != nil {
				return nil, err
			}
			ns[j] = n
		}
		parsed[i] = ns
	}
	return parsed, nil
}

func abs(x int) int {
	if x < 0 {
		return -x
	}
	return x
}

const (
	minValidDiff = 1
	maxValidDiff = 3

	increasing = iota
	decreasing
)

func isValidDiff(diff int, trend int) bool {
	switch {
	case diff < 0 && trend == increasing:
		return false
	case diff > 0 && trend == decreasing:
		return false
	case abs(diff) < minValidDiff || abs(diff) > maxValidDiff:
		return false
	}
	return true
}

func isValidReport(report []int) bool {
	if len(report) < 2 {
		log.Fatalf("want report with len > 1, got %v", report)
	}

	trend := increasing
	if report[0] > report[1] {
		trend = decreasing
	}

	valid := true
	for i := 1; i < len(report); i++ {
		if !isValidDiff(report[i]-report[i-1], trend) {
			valid = false
			break
		}
	}

	return valid
}

// solvePart1 counts the number of "safe" level sequences based on difference rules.
// A sequence is safe if consecutive differences are between 1 and 3 (inclusive) and
// maintain the same trend (increasing or decreasing) throughout.
func solvePart1(input [][]int) (nSafeLevels int) {
	for _, report := range input {
		if isValidReport(report) {
			nSafeLevels++
		}
	}
	return
}

func solvePart2(input [][]int) (nSafeLevels int) {
	for _, report := range input {
		if isValidReport(report) {
			nSafeLevels++
			continue
		}

		for i := 1; i <= len(report); i++ {
			dampenedReport := slices.Concat(report[:i-1], report[i:])
			if isValidReport(dampenedReport) {
				nSafeLevels++
				break
			}
		}
	}
	return
}

func main() {
	input := advent.GetInput("input.txt")

	parsed, err := parseInput(input)
	if err != nil {
		log.Fatal(err)
	}

	solution1 := solvePart1(parsed)
	fmt.Println(solution1)

	solution2 := solvePart2(parsed)
	fmt.Println(solution2)
}
