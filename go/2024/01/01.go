package main

import (
	"fmt"
	"log"
	"sort"
	"strconv"
	"strings"

	"github.com/garrettr/advent-of-code/go/advent"
)

// parseInput takes a string of space-separated number pairs (one pair per line)
// and returns two slices containing the left and right numbers respectively.
// Each line must contain exactly two numbers.
// Returns an error if the input is malformed or contains non-numbers.
func parseInput(input string) (left []int, right []int, err error) {
	lines := strings.Split(strings.TrimSpace(input), "\n")
	left = make([]int, len(lines))
	right = make([]int, len(lines))

	for i, line := range lines {
		parts := strings.Fields(line)
		if len(parts) != 2 {
			err = fmt.Errorf("line %d: expected 2 numbers, got %d", i+1, len(parts))
			return
		}

		l, lerr := strconv.Atoi(parts[0])
		if lerr != nil {
			err = fmt.Errorf("line %d: invalid left number: %v", i+1, parts[0])
			return
		}

		r, rerr := strconv.Atoi(parts[1])
		if rerr != nil {
			err = fmt.Errorf("line %d: invalid right number: %v", i+1, parts[1])
			return
		}

		left[i] = l
		right[i] = r
	}

	return
}

func zip[T any](a, b []T) [][2]T {
	length := min(len(a), len(b))
	result := make([][2]T, length)
	for i := 0; i < length; i++ {
		result[i] = [2]T{a[i], b[i]}
	}
	return result
}

func abs(x int) int {
	if x < 0 {
		return -x
	}
	return x
}

func solvePart1(left []int, right []int) (totalDistance int) {
	// Sort each slice
	sort.Ints(left)
	sort.Ints(right)
	pairs := zip(left, right)
	for _, pair := range pairs {
		totalDistance += abs(pair[0] - pair[1])
	}
	return
}

func solvePart2(left []int, right []int) (similarityScore int) {
	rightFreqs := make(map[int]int)
	for _, n := range right {
		// If key is not in the map, then v is the zero value for the map's element type.
		v := rightFreqs[n]
		rightFreqs[n] = v + 1
	}
	for _, n := range left {
		similarityScore += n * rightFreqs[n]
	}
	return
}

func main() {
	input := advent.GetInput("input.txt")

	left, right, err := parseInput(input)
	if err != nil {
		log.Fatal(err)
	}

	solution1 := solvePart1(left, right)
	fmt.Println(solution1)

	solution2 := solvePart2(left, right)
	fmt.Println(solution2)
}
