package main

import (
	"reflect"
	"testing"
)

const example = `3   4
4   3
2   5
1   3
3   9
3   3`

func TestParseInput(t *testing.T) {
	wantSlice1 := []int{3, 4, 2, 1, 3, 3}
	wantSlice2 := []int{4, 3, 5, 3, 9, 3}

	slice1, slice2, err := parseInput(example)

	if err != nil {
		t.Errorf("got err %v, want nil", err)
	}
	if !reflect.DeepEqual(slice1, wantSlice1) {
		t.Errorf("got slice1 %v, want %v", slice1, wantSlice1)
	}
	if !reflect.DeepEqual(slice2, wantSlice2) {
		t.Errorf("got slice2 %v, want %v", slice2, wantSlice2)
	}
}
