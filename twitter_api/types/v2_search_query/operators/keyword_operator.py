from .operator import InvertibleOperator, Operator, StandaloneOperator


class KeywordOperator(
    InvertibleOperator[Operator],
    StandaloneOperator[Operator],
):
    def __init__(self, keyword: str) -> None:
        self._keyword = keyword

    def __str__(self) -> str:
        if " " in self._keyword:
            keyword = self._keyword.replace('"', r"\"")
            return f'"{keyword}"'
        else:
            return self._keyword
