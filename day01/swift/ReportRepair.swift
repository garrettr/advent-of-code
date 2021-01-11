let example = [1721, 979, 366, 299, 675, 1456]

func find_two_entries_that_sum_to_2020(in numbers: [Int]) -> (a: Int, b: Int) {
    for (index, value) in numbers.enumerated() {
        for value2 in numbers[index..<numbers.endIndex] {
            if value + value2 == 2020 {
                return (value, value2)
            }
        }
    }
    // TODO: replace with optional result type
    return (0, 0)
}

func solve_part_one(for numbers: [Int]) -> Int {
    let (a, b) = find_two_entries_that_sum_to_2020(in: numbers)
    return a * b
}

assert(solve_part_one(for: example) == 514579)
