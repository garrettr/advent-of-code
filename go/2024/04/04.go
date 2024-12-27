package main

import (
	"fmt"
	"log"
	"strings"

	"github.com/garrettr/advent-of-code/go/advent"
)

// Convert input text into a grid representation.
// All of the characters are ASCII characters, so representing them as bytes is safe and space efficient.
func parseInput(input string) ([][]byte, error) {
	lines := strings.Split(strings.TrimSpace(input), "\n")
	if len(lines) == 0 {
		return nil, fmt.Errorf("empty input")
	}

	grid := make([][]byte, len(lines))
	for i, line := range lines {
		grid[i] = []byte(line)
		// Validate all rows are the same length
		if i > 0 && len(grid[i]) != len(grid[0]) {
			err := fmt.Errorf("line %d: expected len %d, got %d", i+1, len(grid[0]), len(grid[i]))
			return nil, err
		}
	}

	return grid, nil
}

type Vertex struct {
	X int
	Y int
}

func (v *Vertex) Add(w Vertex) {
	v.X += w.X
	v.Y += w.Y
}

func (v *Vertex) Scale(i int) {
	v.X = v.X * i
	v.Y = v.Y * i
}

func findXmases(grid *[][]byte, x int, y int) (nXmases int) {
	directions := [8]Vertex{
		{-1, 0},  // ^
		{1, 0},   // v
		{0, -1},  // <
		{0, 1},   // >
		{-1, -1}, // ^<
		{-1, 1},  // ^>
		{1, -1},  // v<
		{1, 1},   // v>
	}
	var xmas [4]byte
	copy(xmas[:], "XMAS")

	height := len(*grid)
	width := len((*grid)[0])
	isValidPos := func(pos *Vertex) bool {
		return pos.X >= 0 && pos.X < height && pos.Y >= 0 && pos.Y < width
	}

	for _, direction := range directions {
		var candidate [4]byte
		for n := 0; n < 4; n++ {
			vec := direction
			vec.Scale(n)
			pos := Vertex{x, y}
			pos.Add(vec)
			if !isValidPos(&pos) {
				break
			}
			candidate[n] = (*grid)[pos.X][pos.Y]
		}
		if candidate == xmas {
			nXmases++
		}
	}
	return
}

func solvePart1(input string) (result int) {
	grid, err := parseInput(input)
	if err != nil {
		log.Fatal(err)
	}

	nXmases := 0
	for x, row := range grid {
		for y, elem := range row {
			if elem == 'X' {
				nXmases += findXmases(&grid, x, y)
			}
		}
	}
	return nXmases
}

// func solvePart2(input string) (result int) {
// 	return 0
// }

func main() {
	input := advent.GetInput("input.txt")

	solution1 := solvePart1(input)
	fmt.Println(solution1)

	// solution2 := solvePart2(input)
	// fmt.Println(solution2)
}
