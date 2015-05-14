#!/usr/bin/env python3

from collections.abc import Sequence, Iterator

__all__ = ['LazyList', 'LazyListIterator']

class LazyList(Sequence):
    def __init__(self, iterable):
        self._data = list()
        self._iter = iter(iterable)
        self._exhausted = False

    def __iter__(self):
        return LazyListIterator(self)

    def __bool__(self):
        try:
            self[0]
        except IndexError:
            return False
        else:
            return True

    def __len__(self):
        self._exhaust()
        return len(self._data)

    def __getitem__(self, key):
        if isinstance(key, slice):
            for s in (key.start, key.stop, key.step):
                if not (s is None or isinstance(s, int)):
                    raise TypeError("lazy-list slice indeces must be integers")
        elif not isinstance(key, int):
            raise TypeError("lazy-list key must be an integer or a slice")

        def negative(k):
            if isinstance(k, int):
                return k < 0
            if isinstance(k, slice):
                negative_start = k.start is not None and k.start < 0
                negative_stop  = k.stop  is not None and k.stop  < 0
                return negative_start or negative_stop

        if negative(key):
            self._exhaust()
            return self._data[key]

        if isinstance(key, slice):
            return LazyListIterator(self, key)

        if isinstance(key, int):
            while True:
                try:
                    return self._data[key]
                except IndexError:
                    try:
                        self._tick()
                    except StopIteration:
                        raise IndexError("lazy-list index out of range") from None

    def _exhaust(self):
        for item in self._iter:
            self._data.append(item)
        self._exhausted = True

    def _tick(self):
        try:
            item = next(self._iter)
        except StopIteration as err:
            self._exhausted = True
            raise err
        else:
            self._data.append(item)
            return item

    def __repr__(self):
        if self._exhausted:
            return "{}({})".format(
                type(self).__name__, repr(self._data))
        elif len(self._data) < 1:
            return "{}({})".format(
                type(self).__name__, repr(self._iter))
        else:
            return "{}({}... ] + {})".format(
                type(self).__name__, repr(self._data)[:-1], repr(self._iter))


class LazyListIterator(Iterator):
    def __init__(self, source, key=slice(None, None, None)):
        super().__init__()
        if not hasattr(source, '__getitem__'):
            raise TypeError("LazyListIterator(): source must be a Sequence")
        if not isinstance(key, slice):
            raise TypeError("LazyListIterator(): key must be a slice")
        if key.step == 0:
            raise ValueError("slice step cannot be zero")
        self._source = source
        self._cursor = 0 if key.start is None else key.start
        self._stop   = key.stop
        self._step   = 1 if key.step is None else key.step

    def __iter__(self):
        return self

    def __next__(self):
        if self._stop is not None:
            if self._step > 0 and self._cursor >= self._stop:
                raise StopIteration
            if self._step < 0 and self._cursor <= self._stop:
                raise StopIteration
        try:
            item = self._source[self._cursor]
        except IndexError:
            raise StopIteration from None
        else:
            self._cursor += self._step
            return item
