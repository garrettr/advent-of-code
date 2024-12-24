package advent

import (
	"log"
	"os"
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
