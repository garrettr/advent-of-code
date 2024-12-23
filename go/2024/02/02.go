package main

import (
	"strconv"
	"strings"
)

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

func main() {

}
