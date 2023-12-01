# Mocking in Python

- the mocking module is part of the unittest framework
- part of the stdlib of Python3
- very useful for mocking

## Return Value vs. Side Effect

To my surprise, `return_value` and `side_effect` can not be used simultaneously.  When I think of a Side Effect, I imagine: **a change in the state of the program or system that is caused by a method but is not reflected in the return value**. The designers of the mocking lib, however, implemented `side_effect` in such way, that is **always** precedes `return_value`.

```python
In [1]: import unittest.mock

In [2]: mock = unittest.mock.MagicMock(return_value='1234', side_effect=1337)

In [4]: mock = unittest.mock.MagicMock(return_value='1234', side_effect=[1337,])

In [5]: mock()
Out[5]: 1337

```

