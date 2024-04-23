import Foundation

struct Day01: AdventDay {
  var data: String

  var lines: [String] {
      data.components(separatedBy: .newlines)
  }

  func part1() -> Any {
      lines.map { line in
          let digits = line.compactMap { $0.wholeNumberValue }
          return digits.first! * 10 + digits.last!
      }.reduce(0, +)
  }

  func part2() -> Any {
      let digitWords = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]
      return lines.map { line in
          let digits = line.indices.compactMap { index in
              if line[index].isWholeNumber {
                  line[index].wholeNumberValue!
              } else if let (wordIndex, _) = digitWords.enumerated().first(where: { line[index...].hasPrefix($1)}) {
                  wordIndex + 1
              } else {
                  nil
              }
          }
          return digits.first! * 10 + digits.last!
      }.reduce(0, +)
  }
}
