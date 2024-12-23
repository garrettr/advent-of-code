package main

import (
	"reflect"
	"testing"
)

const example = `7 6 4 2 1
1 2 7 8 9
9 7 6 2 1
1 3 2 4 5
8 6 4 4 1
1 3 6 7 9`

func TestParseInput(t *testing.T) {
	wantParsed := [][]int{
		{7, 6, 4, 2, 1},
		{1, 2, 7, 8, 9},
		{9, 7, 6, 2, 1},
		{1, 3, 2, 4, 5},
		{8, 6, 4, 4, 1},
		{1, 3, 6, 7, 9},
	}

	parsed, err := parseInput(example)

	if err != nil {
		t.Errorf("got err %v, want nil", err)
	}
	if !reflect.DeepEqual(parsed, wantParsed) {
		t.Errorf("got parsed %v, want %v", parsed, wantParsed)
	}
}
