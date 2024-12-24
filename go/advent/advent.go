package advent

import (
	"log"
	"os"
	"testing"
)

func GetInput(fname string) string {
	bytes, err := os.ReadFile(fname)
	if err != nil {
		log.Fatal(err)
	}
	return string(bytes[:])
}

func Abs(x int) int {
	if x < 0 {
		return -x
	}
	return x
}

func Zip[T any](a, b []T) [][2]T {
	length := min(len(a), len(b))
	result := make([][2]T, length)
	for i := 0; i < length; i++ {
		result[i] = [2]T{a[i], b[i]}
	}
	return result
}

type TestCase struct {
	Name   string
	Solver func(string) int
	Input  string
	Want   int
}

func RunSolveTests(t *testing.T, testCases []TestCase) {
	for _, tc := range testCases {
		t.Run(tc.Name, func(t *testing.T) {
			solution := tc.Solver(tc.Input)
			if solution != tc.Want {
				t.Fatalf("got solution %v, want %v", solution, tc.Want)
			}
		})
	}
}
