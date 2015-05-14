# python-lazylist
A lazily-evaluated list implementation for Python 3. Implements list indexing
syntax for generators. This is just the same as the regular list in Haskell.

-------------------------------------------------------------------------------

Create a LazyList `foo` from an iterable `bar` by passing it to the constructor:

```python
foo = LazyList(bar)         # takes O(1) time
```

You can use any iterable, but it makes most sense to use a generator or
something where you don't want all the values at once.

This is semantically equivalent to:

```python
foo = list(bar)             # takes O(n) time, where n == len(foo)
```

... and you can afterwards index into `foo` in exactly the same way. The
difference is that `list(bar)` will evaluate the entire iterable immediately
when the list is created, whereas `LazyList(bar)` will delay evaluation until
you ask for a particular element, at which point it will only evaluate as many
elements as it needs to get up to that one.

There are three implications of this:

1. The time and space complexity of the operations is different. `LazyList` is
   faster on object creation but slower each time you retrieve an element with
   an index higher than any you have retrieved so far. `list` is slow on object
   creation but fast for element accesses after that.

2. A LazyList is not mutable. You can only read, not write.

3. You can use an infinite sequence to create a LazyList, whereas if you tried
   to do this with a regular list, your program would hang.


For example
-----------

In this repository is an example program which shows how to construct a LazyList
from the (infinite) Fibonacci sequence. You can then index into the Fibonacci
sequence to get the _n_th element. And as long as you don't do something stupid
like ask for the last element or the length of the sequence then it will be as
fast and efficient as it could be. The amount of space it requires in memory is
proportional to the highest index that has been evaluated so far.


Slices
------

One subtlety of my implementation is the way that slices are treated. You can
get a slice of a LazyList with the same syntax as you would use for a regular
list. This will not cause the intervening elements to be evaluated immediately
(unless you pass in a negative index) and will instead return an iterator over
the specified range. The iterator contains a reference to the original LazyList,
so iterating over it will cause elements to be evaluated (and cached) in the
source. But this is just a plain iterator, not another LazyList, and is not
further sliceable nor indexable. This could probably be improved but I haven't
thought about it much because I don't use this feature.
