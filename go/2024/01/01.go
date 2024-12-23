package main

import (
	"strconv"
	"strings"
)

func parseInput(input string) (left []int, right []int, err error) {
	lines := strings.Split(strings.TrimSpace(input), "\n")
	left = make([]int, len(lines))
	right = make([]int, len(lines))
	for idx, line := range lines {
		parts := strings.Fields(line)

		var leftPart int
		leftPart, err = strconv.Atoi(parts[0])
		if err != nil {
			return
		}
		left[idx] = leftPart

		var rightPart int
		rightPart, err = strconv.Atoi(parts[1])
		if err != nil {
			return
		}
		right[idx] = rightPart
	}
	return
}

func main() {

}
