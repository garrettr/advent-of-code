package main

import (
	"fmt"
	"log"
	"slices"
	"strings"

	"github.com/garrettr/advent-of-code/go/advent"
)

type Grid [][]rune

const (
	PatternXMAS = "XMAS"
	PatternMAS  = "MAS"
)

var directions = [][2]int{
	{-1, 0},  // ^
	{1, 0},   // v
	{0, -1},  // <
	{0, 1},   // >
	{-1, -1}, // ^<
	{-1, 1},  // ^>
	{1, -1},  // v<
	{1, 1},   // v>
}

func findPatterns(grid *Grid, startX, startY int) (count int) {
	for _, dir := range directions {
		if isValidPattern(PatternXMAS, grid, startX, startY, dir) {
			count++
		}
	}
	return
}

func isValidPattern(pattern string, grid *Grid, startX, startY int, dir [2]int) bool {
	if !canFitPattern(pattern, grid, startX, startY, dir) {
		return false
	}

	candidate := make([]rune, len(pattern))
	for i := 0; i < len(pattern); i++ {
		x, y := startX+dir[0]*i, startY+dir[1]*i
		candidate[i] = (*grid)[x][y]
	}

	return string(candidate[:]) == pattern
}

func findPatterns2(grid *Grid, startX, startY int) int {
	pattern := []rune(PatternMAS)
	reversedPattern := []rune(PatternMAS)
	slices.Reverse(reversedPattern)

	diagonals := [][][2]int{
		{{-1, -1}, {0, 0}, {1, 1}},
		{{1, -1}, {0, 0}, {-1, 1}},
	}

	for _, diagonal := range diagonals {
		candidate := make([]rune, len(pattern))
		for i, point := range diagonal {
			x, y := startX+point[0], startY+point[1]
			if !(x >= 0 && x < len(*grid) && y >= 0 && y < len((*grid)[0])) {
				break
			}
			candidate[i] = (*grid)[x][y]
		}
		if !(slices.Equal(candidate, pattern) || slices.Equal(candidate, reversedPattern)) {
			return 0
		}
	}

	return 1
}

func canFitPattern(pattern string, grid *Grid, startX, startY int, dir [2]int) bool {
	lastOffset := len(pattern) - 1
	lastX, lastY := startX+dir[0]*lastOffset, startY+dir[1]*lastOffset
	return lastX >= 0 && lastX < len(*grid) && lastY >= 0 && lastY < len((*grid)[0])
}

// Convert input text into a grid representation.
func parseInput(input string) (Grid, error) {
	lines := strings.Split(strings.TrimSpace(input), "\n")
	if len(lines) == 0 {
		return nil, fmt.Errorf("empty input")
	}

	grid := make(Grid, len(lines))
	for i, line := range lines {
		grid[i] = []rune(line)
		// Validate all rows are the same length
		if i > 0 && len(grid[i]) != len(grid[0]) {
			err := fmt.Errorf("line %d: expected len %d, got %d", i+1, len(grid[0]), len(grid[i]))
			return nil, err
		}
	}

	return grid, nil
}

func solvePart1(input string) (patternCount int) {
	grid, err := parseInput(input)
	if err != nil {
		log.Fatal(err)
	}
	for x, row := range grid {
		for y, elem := range row {
			if elem == 'X' {
				patternCount += findPatterns(&grid, x, y)
			}
		}
	}
	return
}

func solvePart2(input string) (patternCount int) {
	grid, err := parseInput(input)
	if err != nil {
		log.Fatal(err)
	}
	for x, row := range grid {
		for y, elem := range row {
			if elem == 'A' {
				patternCount += findPatterns2(&grid, x, y)
			}
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
