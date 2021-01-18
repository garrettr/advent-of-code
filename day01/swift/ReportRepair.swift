import Foundation

let exampleInput = [1721, 979, 366, 299, 675, 1456]
let inputFileName = "../input.txt"

func find_two_numbers_that_sum(to number: Int, in numbers: [Int]) -> (a: Int, b: Int)? {
    for (index, a) in numbers.enumerated() {
        for b in numbers[index..<numbers.endIndex] {
            if a + b == number {
                return (a, b)
            }
        }
    }
    return nil
}

func solve_part_one(for numbers: [Int]) -> Int {
    let (a, b) = find_two_numbers_that_sum(to: 2020, in: numbers)!
    return a * b
}

assert(solve_part_one(for: exampleInput) == 514579)

let input = try! String(contentsOfFile: inputFileName)
let inputLines = input.split(separator: "\n")
let inputNumbers: [Int] = inputLines.map { Int($0)! }

print("solution for part 1: \(solve_part_one(for: inputNumbers))")
