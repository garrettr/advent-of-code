package main

import (
	"fmt"
	"log"
	"regexp"
	"strconv"

	"github.com/garrettr/advent-of-code/go/advent"
)

var (
	multiplyPattern  = regexp.MustCompile(`mul\(([0-9]{1,3}),([0-9]{1,3})\)`)
	conditionPattern = regexp.MustCompile(`do(?:n't)?\(\)`)
)

func solvePart1(input string) (result int) {
	matches := multiplyPattern.FindAllStringSubmatch(input, -1)
	for _, match := range matches {
		x, _ := strconv.Atoi(match[1])
		y, _ := strconv.Atoi(match[2])
		result += x * y
	}
	return
}

func processConditions(input string, conds [][]int, condIndex *int, mulPos int, enabled bool) bool {
	for ; *condIndex < len(conds) && conds[*condIndex][0] < mulPos; *condIndex++ {
		cond := input[conds[*condIndex][0]:conds[*condIndex][1]]
		switch cond {
		case "do()":
			enabled = true
		case "don't()":
			enabled = false
		default:
			log.Fatalf("expected do() or don't(), got %v", cond)
		}
	}
	return enabled
}

func solvePart2(input string) (result int) {
	muls := multiplyPattern.FindAllStringSubmatchIndex(input, -1)
	conds := conditionPattern.FindAllStringSubmatchIndex(input, -1)
	enabled := true
	condIndex := 0
	for _, mul := range muls {
		enabled = processConditions(input, conds, &condIndex, mul[0], enabled)
		if enabled {
			x, _ := strconv.Atoi(input[mul[2]:mul[3]])
			y, _ := strconv.Atoi(input[mul[4]:mul[5]])
			result += x * y
		}
	}
	return
}

func main() {
	input := advent.GetInput("input.txt")

	solution1 := solvePart1(input)
	fmt.Println(solution1)

	solution2 := solvePart2(input)
	fmt.Println(solution2)
}
