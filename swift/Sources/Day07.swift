import Foundation

enum CamelCard: Int, Comparable {
    case joker = 1
    case two, three, four, five, six, seven, eight, nine, ten
    case jack, queen, king, ace

    init?(character: Character, withJokersWild jokersWild: Bool) {
        switch character {
        case "2"..."9":
            self.init(rawValue: Int(String(character))!)
        case "T":
            self = .ten
        case "J":
            self = jokersWild ? .joker : .jack
        case "Q":
            self = .queen
        case "K":
            self = .king
        case "A":
            self = .ace
        default:
            return nil
        }
    }

    static func < (lhs: Self, rhs: Self) -> Bool {
        lhs.rawValue < rhs.rawValue
    }
}

struct Hand {
    let cards: [CamelCard]
    let bid: Int
    let jokersWild: Bool

    enum HandType: Comparable {
        case highCard, onePair, twoPair, threeOfAKind, fullHouse, fourOfAKind, fiveOfAKind
    }

    var type: HandType {
        var counter = Dictionary(grouping: cards, by: { $0 }).mapValues { $0.count }

        if jokersWild, let jokersCount = counter.removeValue(forKey: .joker) {
            let mostCommonCard = counter.max(by: { $0.value < $1.value })?.key ?? .ace
            counter[mostCommonCard, default: 0] += jokersCount
        }

        switch Array(counter.values).sorted(by: >) {
        case [5]:
            return .fiveOfAKind
        case [4, 1]:
            return .fourOfAKind
        case [3, 2]:
            return .fullHouse
        case [3, 1, 1]:
            return .threeOfAKind
        case [2, 2, 1]:
            return .twoPair
        case [2, 1, 1, 1]:
            return .onePair
        default:
            return .highCard
        }
    }
}

extension Hand {
    init?(fromString string: String, withJokersWild jokersWild: Bool = false) {
        let parts = string.split(separator: " ")
        guard parts.count == 2 else {
            return nil
        }
        let cards = parts[0].map { CamelCard(character: $0, withJokersWild: jokersWild)! }
        let bid = Int(parts[1])!
        self.init(cards: cards, bid: bid, jokersWild: jokersWild)
    }
}

struct Day07: AdventDay {
    var data: String

    var lines: [Substring] {
        data.trimmingCharacters(in: .newlines).split(separator: "\n")
    }

    func hands(withJokersWild jokersWild: Bool) -> [Hand] {
        lines.map { Hand(fromString: String($0), withJokersWild: jokersWild)! }
    }

    func calculateWinnings(withHands hands: [Hand]) -> Int {
        hands.sorted { lhs, rhs -> Bool in
            if lhs.type != rhs.type {
                lhs.type < rhs.type
            } else {
                lhs.cards.lexicographicallyPrecedes(rhs.cards)
            }
        }
        .enumerated()
        .map { index, hand in hand.bid * (index + 1) }
        .reduce(0, +)
    }

    func part1() -> Any {
        calculateWinnings(withHands: hands(withJokersWild: false))
    }

    func part2() -> Any {
        calculateWinnings(withHands: hands(withJokersWild: true))
    }
}
