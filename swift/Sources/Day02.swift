struct Game: Equatable {
    let id: Int
    let rounds: [[String: Int]]

    func isPossible(withBag bag: [String: Int]) -> Bool {
        rounds.allSatisfy { round in
            round.allSatisfy { (color, count) in
                bag[color, default: 0] >= count
            }
        }
    }
}

// If you want your custom value type to be initializable with the default initializer
// and memberwise initializer, and also with your own custom initializers, write your
// custom initializers in an extension rather than as part of the value type’s original implementation.
// - https://docs.swift.org/swift-book/documentation/the-swift-programming-language/initialization/
extension Game {
    enum InitializationError: Error, Equatable {
        case invalidFormat(String)
        case invalidGameID(String)
        case invalidRoundFormat(String)
        case invalidCubeCount(String)
        case emptyRounds(String)
    }

    init?(fromDescription description: String) throws {
        let components = description.components(separatedBy: ": ")
        guard components.count == 2 else {
            throw InitializationError.invalidFormat(description)
        }

        guard let id = Int(components[0].components(separatedBy: " ")[1]) else {
            throw InitializationError.invalidGameID(components[0])
        }

        let rounds = try components[1].components(separatedBy: "; ").map { roundDescription -> [String: Int] in
            let roundComponents = roundDescription.components(separatedBy: ", ")
            return try Dictionary(uniqueKeysWithValues: roundComponents.map { setofCubesDescription -> (String, Int) in
                let setOfCubesComponents = setofCubesDescription.components(separatedBy: " ")
                guard setOfCubesComponents.count == 2 else {
                    throw InitializationError.invalidRoundFormat(setofCubesDescription)
                }
                guard let count = Int(setOfCubesComponents[0]) else {
                    throw InitializationError.invalidCubeCount(setOfCubesComponents[0])
                }
                return (setOfCubesComponents[1], count)
            })
        }

        guard !rounds.isEmpty else {
            throw InitializationError.emptyRounds(description)
        }

        self.id = id
        self.rounds = rounds
    }
}

struct Day02: AdventDay {
    var data: String

    var games: [Game] {
        data.components(separatedBy: .newlines).compactMap { try? Game(fromDescription: $0) }
    }

    func part1() -> Any {
        games.filter { $0.isPossible(withBag: ["red": 12, "green": 13, "blue": 14]) }
             .map(\.id)
             .reduce(0, +)
    }

    //  func part2() -> Any {
    //      0
    //  }
}
