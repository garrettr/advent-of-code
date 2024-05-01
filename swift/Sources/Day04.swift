import Foundation

struct Card: Equatable {
    let id: Int
    let winningNumbers: Set<Int>
    let numbers: Set<Int>

    var winners: Set<Int> {
        self.winningNumbers.intersection(self.numbers)
    }
}

extension Card {
    enum InitializationError: Error, Equatable, CustomStringConvertible {
        case invalidFormat(String)
        case invalidCardID(String)
        case invalidNumbers(String)

        var description: String {
            switch self {
            case .invalidFormat(let description):
                return "Invalid format: \(description)"
            case .invalidCardID(let description):
                return "Invalid card ID: \(description)"
            case .invalidNumbers(let description):
                return "Invalid numbers: \(description)"
            }
        }
    }

    init?(fromDescription description: String) throws {
        let components = description.components(separatedBy: ": ")
        guard components.count == 2 else {
            throw InitializationError.invalidFormat(description)
        }

        guard let id = Int(components[0].split(separator: " ", omittingEmptySubsequences: true)[1]) else {
            throw InitializationError.invalidCardID(components[0])
        }

        let numbersLists = components[1].components(separatedBy: " | ")
        guard numbersLists.count == 2 else {
            throw InitializationError.invalidNumbers(components[1])
        }

        let winningNumbers = numbersLists[0].components(separatedBy: .whitespaces).compactMap { Int($0) }
        let numbers = numbersLists[1].components(separatedBy: .whitespaces).compactMap { Int($0) }

        self.id = id
        self.winningNumbers = Set(winningNumbers)
        self.numbers = Set(numbers)
    }
}

struct Day04: AdventDay {
    var data: String

    var cards: [Card] {
        data.trimmingCharacters(in: .newlines)
            .components(separatedBy: .newlines)
            .compactMap {
                do {
                    let card = try Card(fromDescription: $0)
                    return card
                } catch {
                    print("\(error)")
                }
                return nil
            }
    }

    func part1() -> Any {
        cards.map(\.winners.count)
             .filter { $0 > 0 }
             .map { pow(2, $0 - 1)}
             .reduce(0, +)
    }

//    func part2() -> Any {
//        0
//    }
}
