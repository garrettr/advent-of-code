package main

import (
	"fmt"
	"strconv"
	"strings"
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

func main() {

}
