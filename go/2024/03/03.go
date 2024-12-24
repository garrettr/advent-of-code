package main

import (
	"fmt"
	"log"
	"os"
	"regexp"
	"strconv"
)

func getInput(fname string) string {
	bytes, err := os.ReadFile(fname)
	if err != nil {
		log.Fatal(err)
	}
	return string(bytes[:])
}

func solvePart1(input string) (result int) {
	r := regexp.MustCompile(`mul\(([0-9]{1,3}),([0-9]{1,3})\)`)
	matches := r.FindAllStringSubmatch(input, -1)
	for _, match := range matches {
		x, _ := strconv.Atoi(match[1])
		y, _ := strconv.Atoi(match[2])
		result += x * y
	}
	return
}

func main() {
	input := getInput("input.txt")

	solution1 := solvePart1(input)
	fmt.Println(solution1)
}
