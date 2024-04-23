import Algorithms
import Foundation

struct Day01: AdventDay {
  var data: String

  var entities: [String] {
      data.components(separatedBy: .newlines)
  }

  func part1() -> Any {
      entities.map {
          let digits = $0.filter { $0.isWholeNumber }
          return Int(String([digits.first!, digits.last!]))!
      }.reduce(0, +)
  }

  func part2() -> Any {
      let digitWords = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]
      return entities.map {
          var digits: [Int] = []
          for index in $0.indices {
              if $0[index].isWholeNumber {
                  digits.append($0[index].wholeNumberValue!)
              } else {
                  for (wordIndex, word) in digitWords.enumerated() {
                      if $0[index...].hasPrefix(word) {
                          digits.append(wordIndex + 1)
                          break;
                      }
                  }
              }
          }
          return digits.first! * 10 + digits.last!
      }.reduce(0, +)
  }
}
