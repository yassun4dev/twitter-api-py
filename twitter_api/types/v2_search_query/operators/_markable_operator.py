from .operator import Operator, TOperator


class MarkableOperator(Operator[TOperator]):
    def __init__(self, value: str, prefix: str):
        self._value = value[len(prefix) :] if value.startswith(prefix) else value
        self._prefix = prefix

    def __str__(self) -> str:
        return f"{self._prefix}{self._value}"