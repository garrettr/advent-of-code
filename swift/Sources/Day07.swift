import Foundation

enum CamelCard: Int, Comparable {
    case two = 2, three, four, five, six, seven, eight, nine, ten
    case jack, queen, king, ace

    init?(character: Character) {
        switch character {
        case "2"..."9":
            self.init(rawValue: Int(String(character))!)
        case "T":
            self = .ten
        case "J":
            self = .jack
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

    enum Type_: Comparable {
        case highCard, onePair, twoPair, threeOfAKind, fullHouse, fourOfAKind, fiveOfAKind
    }

    var type: Type_ {
        let counter = Dictionary(grouping: cards, by: { $0 }).mapValues { $0.count }
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
    init?(fromString string: String) {
        let parts = string.split(separator: " ")
        guard parts.count == 2 else {
            return nil
        }
        let cards = parts[0].map { CamelCard(character: $0)! }
        let bid = Int(parts[1])!
        self.init(cards: cards, bid: bid)
    }
}

struct Day07: AdventDay {
    var data: String

    var hands: [Hand] {
        data.trimmingCharacters(in: .newlines)
            .split(separator: "\n")
            .map { Hand(fromString: String($0))! }
    }

    func part1() -> Any {
        hands.sorted { lhs, rhs -> Bool in
            if lhs.type == rhs.type {
                for (lhsCard, rhsCard) in zip(lhs.cards, rhs.cards) {
                    if lhsCard == rhsCard {
                        continue
                    }
                    return lhsCard < rhsCard
                }
            }
            return lhs.type < rhs.type
        }
        .enumerated()
        .map { index, hand in hand.bid * (index + 1) }
        .reduce(0, +)
    }

//    func part2() -> Any {
//        0
//    }
}
