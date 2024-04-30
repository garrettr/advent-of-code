struct Game: Equatable {
    let id: Int
    let rounds: [[String: Int]]

    func possible(withBag bag: [String: Int]) -> Bool {
        for round in rounds {
            for (color, count) in round {
                if count > bag[color]! {
                    return false
                }
            }
        }
        return true
    }
}

// If you want your custom value type to be initializable with the default initializer
// and memberwise initializer, and also with your own custom initializers, write your
// custom initializers in an extension rather than as part of the value type’s original implementation.
// - https://docs.swift.org/swift-book/documentation/the-swift-programming-language/initialization/
extension Game {
    init?(fromDescription description: String) {
        let components = description.components(separatedBy: ": ")

        guard components.count == 2 else {
            return nil
        }

        guard let id = Int(components[0].components(separatedBy: " ")[1]) else {
            return nil
        }

        var rounds: [[String: Int]] = []
        for round_description in components[1].components(separatedBy: "; ") {
            var round: [String: Int] = [:]
            for set_of_cubes_description in round_description.components(separatedBy: ", ") {
                let set_of_cubes_components = set_of_cubes_description.components(separatedBy: " ")
                guard let count = Int(set_of_cubes_components[0]) else {
                    return nil
                }
                let color = set_of_cubes_components[1]
                round[color] = count
            }
            rounds.append(round)
        }

        self.id = id
        self.rounds = rounds
    }
}

struct Day02: AdventDay {
    var data: String

    var lines: [String] {
        data.components(separatedBy: .newlines)
    }

    var games: [Game] {
        lines.compactMap { Game(fromDescription: $0) }
    }

    func part1() -> Any {
        games.filter {
            $0.possible(withBag: ["red": 12, "green": 13, "blue": 14])
        }.map { $0.id }.reduce(0, +)
    }

    //  func part2() -> Any {
    //      0
    //  }
}
