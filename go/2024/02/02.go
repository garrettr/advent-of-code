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
	increasing = iota
	decreasing
)

func solvePart1(input [][]int) (nSafeLevels int) {
	for _, report := range input {
		trend := increasing
		if report[0] > report[1] {
			trend = decreasing
		}

		validDiff := func(diff int) bool {
			if diff < 0 && trend == increasing {
				return false
			}
			if diff > 0 && trend == decreasing {
				return false
			}
			if abs(diff) < 1 || abs(diff) > 3 {
				return false
			}
			return true
		}

		for i := range report[1:] {
			if !validDiff(report[i+1] - report[i]) {
				break
			}
			if i == len(report)-2 {
				nSafeLevels++
			}
		}
	}
	return
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
