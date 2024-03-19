use std::borrow::Borrow;
use std::collections::HashMap;
use std::hash::Hash;
use std::iter::FromIterator;
use std::ops::Index;

pub struct Counter<T> {
    map: HashMap<T, usize>,
}

impl<T> Counter<T> {
    pub fn new() -> Self {
        Self {
            map: HashMap::new(),
        }
    }
}

impl<T> Counter<T>
where
    T: Hash + Eq,
{
    pub fn insert(&mut self, value: T) -> bool {
        let mut newly_inserted = false;
        self.map
            .entry(value)
            .and_modify(|e| *e += 1)
            .or_insert_with(|| {
                newly_inserted = true;
                1
            });
        newly_inserted
    }

    pub fn get<Q>(&self, value: &Q) -> Option<&usize>
    where
        T: Borrow<Q>,
        Q: Hash + Eq + ?Sized,
    {
        self.map.get(value)
    }

    pub fn contains<Q>(&self, value: &Q) -> bool
    where
        T: Borrow<Q>,
        Q: Hash + Eq + ?Sized,
    {
        self.map.get(value).is_some()
    }

    pub fn len(&self) -> usize {
        self.map.len()
    }

    pub fn is_empty(&self) -> bool {
        self.len() == 0
    }

    pub fn most_common(&self, n: Option<usize>) -> Vec<(&T, &usize)> {
        let mut counts: Vec<_> = self.map.iter().collect();
        counts.sort_by_key(|c| *c.1 as isize * -1);
        if let Some(n) = n {
            counts.truncate(n)
        }
        counts
    }
}

impl<T, Q: ?Sized> Index<&Q> for Counter<T>
where
    T: Eq + Hash + Borrow<Q>,
    Q: Eq + Hash,
{
    type Output = usize;

    /// Returns a reference to the count of the supplied value, or 0 if the
    /// value isn't counted.
    fn index(&self, value: &Q) -> &Self::Output {
        self.get(value).unwrap_or(&0)
    }
}

impl<T> FromIterator<T> for Counter<T>
where
    T: Eq + Hash,
{
    fn from_iter<I>(iter: I) -> Self
    where
        I: IntoIterator<Item = T>,
    {
        let mut counter = Counter::new();
        for value in iter {
            counter.insert(value);
        }
        counter
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn insert() {
        let mut counter = Counter::new();
        assert_eq!(counter.len(), 0);
        assert!(counter.is_empty());

        assert!(counter.insert("foo"));
        assert_eq!(counter.len(), 1);
        assert!(!counter.is_empty());
        assert_eq!(counter.get(&"foo"), Some(&1));

        assert!(!counter.insert("foo"));
        assert_eq!(counter.len(), 1);
        assert!(!counter.is_empty());
        assert_eq!(counter.get(&"foo"), Some(&2));

        assert!(counter.insert("bar"));
        assert_eq!(counter.len(), 2);
        assert_eq!(counter.get(&"bar"), Some(&1));

        assert!(counter.contains(&"foo"));
        assert!(counter.contains(&"bar"));
        assert!(!counter.contains(&"baz"));
    }

    #[test]
    fn index() {
        let mut counter = Counter::new();
        assert_eq!(counter["foo"], 0);
        assert!(counter.insert("foo"));
        assert_eq!(counter["foo"], 1);
    }

    #[test]
    fn from_iterator() {
        let ints = vec![1, 2, 1, 3, 2, 1];
        let counter: Counter<_> = ints.iter().collect();
        assert_eq!(counter.len(), 3);
        assert_eq!(counter[&1], 3);
        assert_eq!(counter[&2], 2);
        assert_eq!(counter[&3], 1);

        let tuples = vec![(0, 0), (1, 1), (0, 0)];
        let counter: Counter<_> = tuples.iter().collect();
        assert_eq!(counter.len(), 2);
        assert_eq!(counter[&(0, 0)], 2);
        assert_eq!(counter[&(1, 1)], 1);
    }

    #[test]
    fn most_common() {
        let ints = vec![1, 2, 1, 3, 2, 1];
        let counter: Counter<_> = ints.iter().collect();

        let counts = counter.most_common(None);
        assert_eq!(counts.len(), 3);
        assert_eq!(counts[0], (&&1, &3));
        assert_eq!(counts[1], (&&2, &2));
        assert_eq!(counts[2], (&&3, &1));

        let counts = counter.most_common(Some(1));
        assert_eq!(counts.len(), 1);
        assert_eq!(counts[0], (&&1, &3));
    }
}
