package main

import (
	"fmt"
	"log"
	"os"
	"strconv"
	"strings"
)

func getInput(fname string) string {
	bytes, err := os.ReadFile(fname)
	if err != nil {
		log.Fatal(err)
	}
	return string(bytes[:])
}

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

// solvePart1 counts the number of "safe" level sequences based on difference rules.
// A sequence is safe if consecutive differences are between 1 and 3 (inclusive) and
// maintain the same trend (increasing or decreasing) throughout.
func solvePart1(input [][]int) (nSafeLevels int) {
	for _, report := range input {
		if len(report) < 2 {
			log.Fatalf("want report with len >= 2, got %v", report)
		}

		trend := increasing
		if report[0] > report[1] {
			trend = decreasing
		}

		isValidDiff := func(diff int) bool {
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

		valid := true
		for i := 1; i < len(report); i++ {
			if !isValidDiff(report[i] - report[i-1]) {
				valid = false
				break
			}
		}
		if valid {
			nSafeLevels++
		}
	}
	return nSafeLevels
}

func main() {
	input := getInput("input.txt")

	parsed, err := parseInput(input)
	if err != nil {
		log.Fatal(err)
	}

	solution1 := solvePart1(parsed)
	fmt.Println(solution1)
}
