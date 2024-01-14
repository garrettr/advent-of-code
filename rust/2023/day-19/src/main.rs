use once_cell::sync::Lazy;
use regex::Regex;
use std::collections::HashMap;
use std::str::FromStr;

const EXAMPLE: &str = include_str!("example.txt");
const INPUT: &str = include_str!("input.txt");

#[derive(Debug, PartialEq, Eq)]
enum AplentyError {
    ParseIntError(std::num::ParseIntError),
    ParseRatingError(String),
    ParsePartError(String),
    ParseComparisonError(String),
    ParseTestError(String),
    ParseConseqError(String),
    ParseRuleError(String),
    ParseWorkflowError(String),
}

// To satisfy the `Error` trait a `Display` implementation is also needed.
impl std::fmt::Display for AplentyError {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        match self {
            Self::ParseIntError(e) => write!(f, "{}", e),
            Self::ParseRatingError(s) => write!(f, "Invalid rating: {}", s),
            Self::ParsePartError(s) => write!(f, "Invalid part: {}", s),
            Self::ParseComparisonError(s) => write!(f, "Invalid comparison: {}", s),
            Self::ParseTestError(s) => write!(f, "Invalid test: {}", s),
            Self::ParseConseqError(s) => write!(f, "Invalid conseq: {}", s),
            Self::ParseRuleError(s) => write!(f, "Invalid rule: {}", s),
            Self::ParseWorkflowError(s) => write!(f, "Invalid workflow: {}", s),
        }
    }
}

// https://www.lurklurk.org/effective-rust/errors.html#nested-errors
impl From<std::num::ParseIntError> for AplentyError {
    fn from(e: std::num::ParseIntError) -> Self {
        Self::ParseIntError(e)
    }
}

#[derive(Debug, PartialEq, Eq, Hash)]
enum Rating {
    X,
    M,
    A,
    S,
}

impl FromStr for Rating {
    type Err = AplentyError;

    fn from_str(s: &str) -> Result<Self, Self::Err> {
        match s {
            "x" => Ok(Self::X),
            "m" => Ok(Self::M),
            "a" => Ok(Self::A),
            "s" => Ok(Self::S),
            _ => Err(Self::Err::ParseRatingError(s.to_owned())),
        }
    }
}

#[derive(Debug, PartialEq)]
struct Part(HashMap<Rating, i32>);

static RATING_RE: Lazy<Regex> =
    Lazy::new(|| Regex::new(r"(?<rating>[xmas])=(?<value>\d+)").unwrap());

impl FromStr for Part {
    type Err = AplentyError;

    fn from_str(s: &str) -> Result<Self, Self::Err> {
        let mut ratings = HashMap::with_capacity(4);
        for (_, [rating, value]) in RATING_RE.captures_iter(s).map(|c| c.extract()) {
            let rating = rating.parse()?;
            let value = value.parse().map_err(|_| {
                Self::Err::ParsePartError(format!("Invalid rating value {}", value))
            })?;
            ratings.insert(rating, value);
        }
        if ratings.len() != 4 {
            Err(Self::Err::ParsePartError(format!(
                "Expected 4 ratings, found {}: {:#?} => {:#?}",
                ratings.len(),
                s,
                ratings
            )))?
        }
        Ok(Part(ratings))
    }
}

impl Part {
    fn ratings_sum(&self) -> i32 {
        self.0.values().sum()
    }
}

#[derive(Debug, PartialEq, Eq)]
enum Comparison {
    LessThan,
    GreaterThan,
}

impl FromStr for Comparison {
    type Err = AplentyError;

    fn from_str(s: &str) -> Result<Self, Self::Err> {
        match s {
            "<" => Ok(Self::LessThan),
            ">" => Ok(Self::GreaterThan),
            _ => Err(Self::Err::ParseComparisonError(s.to_owned())),
        }
    }
}

#[derive(Debug, PartialEq, Eq)]
struct Test {
    rating: Rating,
    comparison: Comparison,
    value: i32,
}

static TEST_RE: Lazy<Regex> =
    Lazy::new(|| Regex::new(r"(?<rating>[xmas])(?<comparison><|>)(?<value>\d+)").unwrap());

impl FromStr for Test {
    type Err = AplentyError;

    fn from_str(s: &str) -> Result<Self, Self::Err> {
        let (_, [rating, comparison, value]) = TEST_RE
            .captures(s)
            .map(|caps| caps.extract())
            .ok_or(Self::Err::ParseTestError(s.to_owned()))?;
        let rating = rating.parse()?;
        let comparison = comparison.parse()?;
        let value = value.parse()?;
        Ok(Test {
            rating,
            comparison,
            value,
        })
    }
}

impl Test {
    fn test(&self, part: &Part) -> bool {
        use Comparison::*;
        match self.comparison {
            LessThan => part.0.get(&self.rating).unwrap() < &self.value,
            GreaterThan => part.0.get(&self.rating).unwrap() > &self.value,
        }
    }
}

#[derive(Debug, PartialEq, Eq, Clone)]
enum Conseq {
    Send(String),
    Accept,
    Reject,
}

impl FromStr for Conseq {
    type Err = AplentyError;

    fn from_str(s: &str) -> Result<Self, Self::Err> {
        match s {
            "A" => Ok(Self::Accept),
            "R" => Ok(Self::Reject),
            workflow if workflow.chars().all(|c| c.is_ascii_lowercase()) => {
                Ok(Self::Send(workflow.to_owned()))
            }
            _ => Err(Self::Err::ParseConseqError(s.to_owned())),
        }
    }
}

#[derive(Debug, PartialEq, Eq)]
struct Rule {
    test: Option<Test>,
    conseq: Conseq,
}

impl FromStr for Rule {
    type Err = AplentyError;

    fn from_str(s: &str) -> Result<Self, Self::Err> {
        let parts: Vec<&str> = s.splitn(2, ':').collect();
        let (test, conseq) = match parts.as_slice() {
            [conseq] => (None, conseq.parse()?),
            [test, conseq] => (Some(test.parse()?), conseq.parse()?),
            _ => Err(Self::Err::ParseRuleError(s.to_owned()))?,
        };
        Ok(Rule { test, conseq })
    }
}

impl Rule {
    fn test(&self, part: &Part) -> bool {
        match &self.test {
            Some(test) => test.test(part),
            None => true,
        }
    }
}

#[derive(Debug, PartialEq, Eq)]
struct Workflow {
    name: String,
    rules: Vec<Rule>,
}

static WORKFLOW_RE: Lazy<Regex> =
    Lazy::new(|| Regex::new(r"(?<name>[a-z]+)\{(?<rules>[a-zA-Z0-9<>:,]+)\}").unwrap());

impl FromStr for Workflow {
    type Err = AplentyError;

    fn from_str(s: &str) -> Result<Self, Self::Err> {
        let (_, [name, rules]) = WORKFLOW_RE
            .captures(s)
            .map(|caps| caps.extract())
            .ok_or(Self::Err::ParseWorkflowError(s.to_owned()))?;
        let rules: Result<Vec<Rule>, Self::Err> =
            rules.split(',').map(|rule| rule.parse()).collect();
        Ok(Self {
            name: name.to_owned(),
            rules: rules?,
        })
    }
}

impl Workflow {
    fn process_part(&self, part: &Part) -> Conseq {
        for rule in &self.rules {
            if rule.test(part) {
                return rule.conseq.clone();
            }
        }
        panic!("At least one rule should always match")
    }
}

#[derive(Debug)]
struct Workflows(HashMap<String, Workflow>);

impl FromStr for Workflows {
    type Err = AplentyError;

    fn from_str(s: &str) -> Result<Self, Self::Err> {
        let workflows: Result<HashMap<String, Workflow>, _> = s
            .lines()
            .map(|line| {
                line.parse::<Workflow>()
                    .map(|workflow| (workflow.name.clone(), workflow))
            })
            .collect();
        Ok(Self(workflows?))
    }
}

impl Workflows {
    fn process_part(&self, part: &Part) -> bool {
        use Conseq::*;
        let mut workflow_name = String::from("in");
        loop {
            let workflow = self.0.get(&workflow_name).unwrap();
            match workflow.process_part(part) {
                Send(to) => {
                    workflow_name = to;
                }
                Accept => {
                    return true;
                }
                Reject => {
                    return false;
                }
            }
        }
    }
}

fn part1(input: &str) -> i32 {
    let (workflows, parts) = input
        .split_once("\n\n")
        .expect("two sections separated by two newlines");
    let workflows: Workflows = workflows.parse().expect("successfully parsed workflows");
    let parts: Vec<Part> = parts.lines().map(|line| line.parse().unwrap()).collect();
    let accepted: Vec<_> = parts
        .iter()
        .filter(|&part| workflows.process_part(part))
        .collect();
    accepted.iter().map(|&part| part.ratings_sum()).sum()
}

fn part2(input: &str) -> () {}

fn main() {
    dbg!(part1(INPUT));
    // dbg!(part2(INPUT));
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_parse_rating() {
        assert_eq!("x".parse(), Ok(Rating::X));
        assert_eq!("m".parse(), Ok(Rating::M));
        assert_eq!("a".parse(), Ok(Rating::A));
        assert_eq!("s".parse(), Ok(Rating::S));

        assert_eq!(
            "z".parse::<Rating>(),
            Err(AplentyError::ParseRatingError("z".to_owned()))
        )
    }

    #[test]
    fn test_parse_part() {
        let expected = Part(HashMap::from([
            (Rating::X, 1),
            (Rating::M, 22),
            (Rating::A, 333),
            (Rating::S, 4444),
        ]));
        assert_eq!("{x=1,m=22,a=333,s=4444}".parse(), Ok(expected));

        assert!(matches!(
            "{x=1,m=22,a=jklol,s=4444}".parse::<Part>(),
            Err(AplentyError::ParsePartError(_))
        ));

        assert!(matches!(
            "{x=1,m=22,s=4444}".parse::<Part>(),
            Err(AplentyError::ParsePartError(_))
        ));

        assert!(matches!(
            "{x=1,m=22,a=333,j=4444}".parse::<Part>(),
            Err(AplentyError::ParsePartError(_))
        ));
    }

    #[test]
    fn test_parse_comparison() {
        assert_eq!("<".parse(), Ok(Comparison::LessThan));
        assert_eq!(">".parse(), Ok(Comparison::GreaterThan));

        assert_eq!(
            "!".parse::<Comparison>(),
            Err(AplentyError::ParseComparisonError("!".to_owned()))
        );
    }

    #[test]
    fn test_parse_test() {
        assert_eq!(
            "a<2006".parse(),
            Ok(Test {
                rating: Rating::A,
                comparison: Comparison::LessThan,
                value: 2006
            })
        );
        assert_eq!(
            "m>2090".parse(),
            Ok(Test {
                rating: Rating::M,
                comparison: Comparison::GreaterThan,
                value: 2090
            })
        );

        assert!(matches!(
            "b<1".parse::<Test>(),
            Err(AplentyError::ParseTestError(_))
        ));
        assert!(matches!(
            "x=1".parse::<Test>(),
            Err(AplentyError::ParseTestError(_))
        ));
        assert!(matches!(
            "x>foo".parse::<Test>(),
            Err(AplentyError::ParseTestError(_))
        ));
    }

    #[test]
    fn test_parse_conseq() {
        assert_eq!("A".parse(), Ok(Conseq::Accept));
        assert_eq!("R".parse(), Ok(Conseq::Reject));
        assert_eq!("abc".parse(), Ok(Conseq::Send(String::from("abc"))));

        assert_eq!(
            "ABC".parse::<Conseq>(),
            Err(AplentyError::ParseConseqError(String::from("ABC")))
        );
    }

    #[test]
    fn test_parse_rule() {
        assert_eq!(
            "a<2006:qkq".parse(),
            Ok(Rule {
                test: Some(Test {
                    rating: Rating::A,
                    comparison: Comparison::LessThan,
                    value: 2006
                }),
                conseq: Conseq::Send("qkq".to_owned())
            })
        );

        assert_eq!(
            "m>2090:A".parse(),
            Ok(Rule {
                test: Some(Test {
                    rating: Rating::M,
                    comparison: Comparison::GreaterThan,
                    value: 2090
                }),
                conseq: Conseq::Accept
            })
        );

        assert_eq!(
            "x>2440:R".parse(),
            Ok(Rule {
                test: Some(Test {
                    rating: Rating::X,
                    comparison: Comparison::GreaterThan,
                    value: 2440
                }),
                conseq: Conseq::Reject
            })
        );

        assert_eq!(
            "rfg".parse(),
            Ok(Rule {
                test: None,
                conseq: Conseq::Send("rfg".to_owned())
            })
        );

        assert_eq!(
            "A".parse(),
            Ok(Rule {
                test: None,
                conseq: Conseq::Accept
            })
        );

        assert_eq!(
            "R".parse(),
            Ok(Rule {
                test: None,
                conseq: Conseq::Reject
            })
        );
    }

    #[test]
    fn test_parse_workflow() {
        let input = "pv{a>1716:R,A}";
        let expected = Workflow {
            name: "pv".to_owned(),
            rules: Vec::from([
                Rule {
                    test: Some(Test {
                        rating: Rating::A,
                        comparison: Comparison::GreaterThan,
                        value: 1716,
                    }),
                    conseq: Conseq::Reject,
                },
                Rule {
                    test: None,
                    conseq: Conseq::Accept,
                },
            ]),
        };
        assert_eq!(input.parse(), Ok(expected));

        let input = "qqz{s>2770:qs,m<1801:hdj,R}";
        let expected = Workflow {
            name: "qqz".to_owned(),
            rules: Vec::from([
                Rule {
                    test: Some(Test {
                        rating: Rating::S,
                        comparison: Comparison::GreaterThan,
                        value: 2770,
                    }),
                    conseq: Conseq::Send("qs".to_owned()),
                },
                Rule {
                    test: Some(Test {
                        rating: Rating::M,
                        comparison: Comparison::LessThan,
                        value: 1801,
                    }),
                    conseq: Conseq::Send("hdj".to_owned()),
                },
                Rule {
                    test: None,
                    conseq: Conseq::Reject,
                },
            ]),
        };
        assert_eq!(input.parse(), Ok(expected));
    }

    #[test]
    fn test_part1() {
        assert_eq!(part1(EXAMPLE), 19114);
        assert_eq!(part1(INPUT), 362930);
    }

    // #[test]
    // fn test_part2() {
    //     assert_eq!(part2(EXAMPLE), ());
    //     assert_eq!(part2(INPUT), ());
    // }
}
