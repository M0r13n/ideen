# Type Hints (Python)

=> [Cheat Sheet](https://mypy.readthedocs.io/en/stable/cheat_sheet_py3.html)

## Don't be too harsh

- [Reasons to avoid static type checking](https://typing.readthedocs.io/en/latest/source/typing_anti_pitch.html)

> Type annotations can both help and hurt readability. While type annotations can serve both humans and machines, particularly complex annotations or changes to idioms serve machines more than they do humans. Readability counts.

> The cost-benefit ratio isn’t good enough. Pleasing static type checkers requires a non-zero amount of busy work. If this isn’t worth the extra confidence you get, you shouldn’t add static type checking.

## Generics

- `T = TypeVar('T')`
- `first(l: Sequence[T]) -> T` a sequence generic over the TypeVar T
- `class LoggedVar(Generic[T]): ...` generic class

```python
from typing import Generic, TypeVar, Sequence

T = TypeVar('T')


class Rotator(Generic[T]):

    def rotate(self, l: Sequence[T]) -> T:
        return l[::-1]

    def first(self, l: Sequence[T]) -> T:
        return l[0]

# Types are preserved if Rotator is type hinted with Rotator[int] -> a Rotator instance that operates on int's
r: Rotator[int] = Rotator()
x = r.rotate([1, 2, 3])
y = r.rotate((1, 2, 3))
z = r.first([10, 11, 12])

print(x, y, z)

```

## Callable Objects

- **must always be used with exactly two values**
	- argument list must be a list of types, a [ParamSpec](#paramspec), [Concatenate](#concatenate), or an ellipsis
	- the return type must be single type
- `Callable[[int], str]` takes a single argument of type `int` and returns a `str`
- `Callable[..., str]` takes any number of arguments and returns a `str`

## Protocol

Protocol classes are defined like this:

```python
class Proto(Protocol):
    def meth(self) -> int:
        ...
```

Such classes are primarily used with static type checkers that recognize structural subtyping (static duck-typing), for example:

```python
class C:
    def meth(self) -> int:
        return 0

def func(x: Proto) -> int:
    return x.meth()

func(C())  # Passes static type check
```

This is useful to check if certain classes implement *the protocol*. In this case `C` has a meth method that matches the signature of the protocol `Proto`.


## ParamSpec

- used to forward the parameter types **of one callable to another callable**

```python
from collections.abc import Callable
from typing import TypeVar, ParamSpec
import logging

T = TypeVar('T')
P = ParamSpec('P')

def add_logging(f: Callable[P, T]) -> Callable[P, T]:
    '''A type-safe decorator to add logging to a function.'''
    def inner(*args: P.args, **kwargs: P.kwargs) -> T:
        logging.info(f'{f.__name__} was called')
        return f(*args, **kwargs)
    return inner

@add_logging
def add_two(x: float, y: float) -> float:
    '''Add two numbers together.'''
    return x + y
```
