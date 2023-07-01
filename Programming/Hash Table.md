# Hash Table

TBD

```python
from collections import namedtuple


NOTHING = object()
DELETED = object()

LF_THRESHOLD = 0.5

# Collisions
# Items
# Values
# Rehashing

Pair = namedtuple('Pair', ['key', 'value'])


class HashTable(object):
    def __init__(self, capacity: int) -> None:
        self._pairs = [NOTHING,] * capacity
        self._keys = []

    def __len__(self) -> int:
        return len(self.items())

    def __setitem__(self, key: object, value: object):
        if self.load_factor() >= LF_THRESHOLD:
            self._rehash_and_grow()

        for idx, pair in self._probe(key):
            if pair is DELETED:
                continue
            if pair is NOTHING or pair.key == key:
                if value is DELETED:
                    self._pairs[idx] = DELETED
                else:
                    self._pairs[idx] = Pair(key, value)
                    if pair is NOTHING:
                        self._keys.append(key)
                return None

    def __getitem__(self, key: object):
        for _, pair in self._probe(key):
            if pair is NOTHING:
                raise KeyError(key)
            if pair is DELETED:
                continue
            if pair.key == key:
                return pair.value
        raise KeyError(key)

    def __delitem__(self, key):
        if key in self:
            self[key] = DELETED
            self._keys.remove(key)
        else:
            raise KeyError(key)

    def __contains__(self, key: object):
        try:
            self[key]
        except KeyError:
            return False
        return True

    def _probe(self, key):
        idx = hash(key) % len(self._pairs)
        for _ in range(len(self._pairs)):
            yield idx, self._pairs[idx]
            # wrap around the end of the array if necessary
            idx = (idx + 1) % len(self._pairs)

    def get(self, key, default=None):
        try:
            return self[key]
        except KeyError:
            return default

    def keys(self):
        return self._keys.copy()

    def items(self):
        return [Pair(key, self[key]) for key in self._keys]

    def values(self):
        return [pair.value for pair in self.items()]

    def _rehash_and_grow(self):
        new = HashTable(len(self._pairs * 2))
        for pair in self.items():
            new[pair.key] = pair.value
        self._pairs = new._pairs

    def load_factor(self):
        occupied_or_deleted = [
            slot for slot in self._pairs if slot is not NOTHING]
        return len(occupied_or_deleted) / len(self._pairs)


if __name__ == '__main__':
    ht = HashTable(1)

    ht["hola"] = "hello"
    ht[98.6] = 37
    ht[False] = True

    assert "hello" in ht.values()
    assert 37 in ht.values()
    assert True in ht.values()

    assert ht["hola"] == "hello"
    assert ht[98.6] == 37
    assert ht[False] is True

    assert len(ht.items()) == 3

    assert ht.keys() == ["hola", 98.6, False,]
    assert ht.items() == [("hola", "hello"),  (98.6, 37), (False, True)]

    del ht[98.6]

    assert len(ht.items()) == 2
    assert ht["hola"] == "hello"
    assert ht[False] is True
    assert 98.6 not in ht
    assert ht.keys() == ["hola",  False]

    ht[98.6] = 1337
    assert ht.keys() == ["hola", False, 98.6]
    assert ht.items() == [("hola", "hello"),  (False, True), (98.6, 1337)]

```