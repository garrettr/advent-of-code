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

#[derive(Debug, PartialEq, Eq)]
enum Conseq {
    Sent(String),
    Accepted,
    Rejected,
}

impl FromStr for Conseq {
    type Err = AplentyError;

    fn from_str(s: &str) -> Result<Self, Self::Err> {
        match s {
            "A" => Ok(Self::Accepted),
            "R" => Ok(Self::Rejected),
            workflow if workflow.chars().all(|c| c.is_ascii_lowercase()) => {
                Ok(Self::Sent(workflow.to_owned()))
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

fn part1(input: &str) -> u64 {
    let (workflows, parts) = input
        .split_once("\n\n")
        .expect("two sections separated by two newlines");

    let workflows: HashMap<String, Workflow> = workflows
        .lines()
        .map(|line| line.parse().unwrap())
        .map(|workflow: Workflow| (workflow.name.clone(), workflow))
        .collect();
    dbg!(workflows);
    0
}

fn part2(input: &str) -> () {}

fn main() {
    dbg!(part1(EXAMPLE));
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
        assert_eq!("A".parse(), Ok(Conseq::Accepted));
        assert_eq!("R".parse(), Ok(Conseq::Rejected));
        assert_eq!("abc".parse(), Ok(Conseq::Sent(String::from("abc"))));

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
                conseq: Conseq::Sent("qkq".to_owned())
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
                conseq: Conseq::Accepted
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
                conseq: Conseq::Rejected
            })
        );

        assert_eq!(
            "rfg".parse(),
            Ok(Rule {
                test: None,
                conseq: Conseq::Sent("rfg".to_owned())
            })
        );

        assert_eq!(
            "A".parse(),
            Ok(Rule {
                test: None,
                conseq: Conseq::Accepted
            })
        );

        assert_eq!(
            "R".parse(),
            Ok(Rule {
                test: None,
                conseq: Conseq::Rejected
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
                    conseq: Conseq::Rejected,
                },
                Rule {
                    test: None,
                    conseq: Conseq::Accepted,
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
                    conseq: Conseq::Sent("qs".to_owned()),
                },
                Rule {
                    test: Some(Test {
                        rating: Rating::M,
                        comparison: Comparison::LessThan,
                        value: 1801,
                    }),
                    conseq: Conseq::Sent("hdj".to_owned()),
                },
                Rule {
                    test: None,
                    conseq: Conseq::Rejected,
                },
            ]),
        };
        assert_eq!(input.parse(), Ok(expected));
    }

    #[test]
    fn test_part1() {
        // assert_eq!(part1(EXAMPLE), ());
        // assert_eq!(part1(INPUT), ());
    }

    #[test]
    fn test_part2() {
        // assert_eq!(part2(EXAMPLE), ());
        // assert_eq!(part2(INPUT), ());
    }
}
