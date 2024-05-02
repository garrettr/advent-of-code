import Foundation

enum CamelCard: Comparable {
    case Two, Three, Four, Five, Six, Seven, Eight, Nine, Ten, Jack, Queen, King, Ace

    init?(character: Character) {
        switch character {
        case "2":
            self = .Two
        case "3":
            self = .Three
        case "4":
            self = .Four
        case "5":
            self = .Five
        case "6":
            self = .Six
        case "7":
            self = .Seven
        case "8":
            self = .Eight
        case "9":
            self = .Nine
        case "T":
            self = .Ten
        case "J":
            self = .Jack
        case "Q":
            self = .Queen
        case "K":
            self = .King
        case "A":
            self = .Ace
        default:
            return nil
        }
    }
}

struct Hand {
    let cards: [CamelCard]
    let bid: Int

    enum Type_: Comparable {
        case HighCard, OnePair, TwoPair, ThreeOfAKind, FullHouse, FourOfAKind, FiveOfAKind
    }

    var type: Type_ {
        var counter: [CamelCard: Int] = [:]
        for card in cards {
            counter[card, default: 0] += 1
        }
        if counter.count == 1 {
            return .FiveOfAKind
        } else if counter.count == 2 {
            if Set(counter.values) == Set([4, 1]) {
                return .FourOfAKind
            } else {
                return .FullHouse
            }
        } else if counter.count == 3 {
            if Set(counter.values) == Set([3, 1, 1]) {
                return .ThreeOfAKind
            } else {
                return .TwoPair
            }
        } else if counter.count == 4 {
            return .OnePair
        }
        return .HighCard
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
            .compactMap { Hand(fromString: String($0))! }
    }

    func part1() -> Any {
        hands.sorted { a, b -> Bool in
            if a.type == b.type {
                for (aCard, bCard) in zip(a.cards, b.cards) {
                    if aCard == bCard {
                        continue
                    }
                    return aCard < bCard
                }
            }
            return a.type < b.type
        }.enumerated().map { i, hand in
            hand.bid * (i + 1)
        }.reduce(0, +)
    }

//    func part2() -> Any {
//        0
//    }
}
