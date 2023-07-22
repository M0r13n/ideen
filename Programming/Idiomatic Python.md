# Idiomatic Python

## Decorators

```python
import typing


Param = typing.ParamSpec('Param')
RetType = typing.TypeVar('RetType')


def log_exception(
        error_cls: typing.Type[Exception]
) -> typing.Callable[[typing.Callable[Param, RetType]], typing.Callable[Param, RetType]]:
    def decorator(func: typing.Callable[Param, RetType]) -> typing.Callable[Param, RetType]:
        def wrapper(*args: Param.args, **kwargs: Param.kwargs) -> RetType:
            try:
                return func(*args, **kwargs)
            except error_cls:
                # do something
                raise
        return wrapper
    return decorator


if __name__ == '__main__':
    @log_exception(ValueError)
    def some_function() -> None:
        raise ValueError('err')

    some_function()

```