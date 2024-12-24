package main

import (
	"fmt"
	"log"
	"os"
	"regexp"
	"strconv"
)

var (
	multiplyPattern  = regexp.MustCompile(`mul\(([0-9]{1,3}),([0-9]{1,3})\)`)
	conditionPattern = regexp.MustCompile(`do(?:n't)?\(\)`)
)

func getInput(fname string) string {
	bytes, err := os.ReadFile(fname)
	if err != nil {
		log.Fatal(err)
	}
	return string(bytes[:])
}

func solvePart1(input string) (result int) {
	matches := multiplyPattern.FindAllStringSubmatch(input, -1)
	for _, match := range matches {
		x, _ := strconv.Atoi(match[1])
		y, _ := strconv.Atoi(match[2])
		result += x * y
	}
	return
}

func solvePart2(input string) (result int) {
	muls := multiplyPattern.FindAllStringSubmatchIndex(input, -1)
	conds := conditionPattern.FindAllStringSubmatchIndex(input, -1)

	isEnabled := true
	condIndex := 0
	for _, mul := range muls {
		for ; condIndex < len(conds) && conds[condIndex][0] < mul[0]; condIndex++ {
			switch cond := input[conds[condIndex][0]:conds[condIndex][1]]; cond {
			case "do()":
				isEnabled = true
			case "don't()":
				isEnabled = false
			default:
				log.Fatalf("expected do() or don't(), got %v", cond)
			}
		}

		if isEnabled {
			x, _ := strconv.Atoi(input[mul[2]:mul[3]])
			y, _ := strconv.Atoi(input[mul[4]:mul[5]])
			result += x * y
		}
	}

	return
}

func main() {
	input := getInput("input.txt")

	solution1 := solvePart1(input)
	fmt.Println(solution1)

	solution2 := solvePart2(input)
	fmt.Println(solution2)
}
