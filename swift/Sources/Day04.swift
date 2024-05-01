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

        let idComponents = components[0].split(separator: " ", omittingEmptySubsequences: true)
        guard idComponents.count == 2, let id = Int(idComponents[1]) else {
            throw InitializationError.invalidCardID(components[0])
        }

        let numbersLists = components[1].components(separatedBy: " | ")
        guard numbersLists.count == 2 else {
            throw InitializationError.invalidNumbers(components[1])
        }

        let winningNumbers = Set(numbersLists[0].split(separator: " ").compactMap { Int($0) })
        let numbers = Set(numbersLists[1].split(separator: " ").compactMap { Int($0) })

        self.init(id: id, winningNumbers: winningNumbers, numbers: numbers)
    }
}

struct Day04: AdventDay {
    var data: String

    var cards: [Card] {
        data.trimmingCharacters(in: .newlines)
            .split(separator: "\n")
            .compactMap {
                do {
                    return try Card(fromDescription: String($0))
                } catch {
                    print("Initialization failed: \(error)")
                    return nil
                }
            }
    }

    func part1() -> Any {
        cards.map(\.winners.count)
             .filter { $0 > 0 }
             .map { 1 << ($0 - 1) }
             .reduce(0, +)
    }

    func part2() -> Any {
        var cardCounts = Array(repeating: 1, count: cards.count)
        for (i, card) in cards.enumerated() {
            for j in 0..<card.winners.count {
                cardCounts[i + j + 1] += cardCounts[i]
            }
        }
        return cardCounts.reduce(0, +)
    }
}
