#!/usr/bin/env python3

from lazylist import LazyList

def fibonacci(a=0, b=1):
    while True:
        yield a
        a, b = b, a + b

lazyfib = LazyList(fibonacci())

print(lazyfib[0], lazyfib[3], lazyfib[10])      # prints 0, 2, 55
print(lazyfib[8], lazyfib[7])                   # prints 21, 13

for x in lazyfib[3:7]:
    print(x)                                    # prints 2, 3, 5, 8

for x in lazyfib[:5]:
    print(x)                                    # prints 0, 1, 1, 2, 3

c = 0
for x in lazyfib[10:]:
    if c >= 3:
        break
    print(x)                                    # prints 55, 89, 144
    c += 1

print(lazyfib[100])                             # prints 354224848179261915075

# This will not work
try:
    foo = lazyfib[5:10]
    print(foo[3])
except TypeError as err:
    # throws TypeError("'LazyListIterator' object does not support indexing")
    print(repr(err))

# The following works, but is memory-inefficient
foo = LazyList(lazyfib[5:10])
print(foo[3])                                   # prints 21
# The values 5, 8, 13, 21 are now stored twice: in the original lazyfib's cache,
# and also in foo's cache.


# Any of the following would cause the program to hang forever and eat all your
# memory. They would work if the generator you constructed with was finite,
# however (like a file stream).

if False:
    print(len(lazyfib))

if False:
    print(lazyfib[-7])

if False:
    foo = lazyfib[5:-1]

if False:
    for x in lazyfib[10:]:
        pass
