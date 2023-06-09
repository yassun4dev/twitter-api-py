import pytest

from twitter_api.error import SearchQueryDoubleQuotedError
from twitter_api.types.v2_search_query.operators.cashtag_operator import CashtagOperator
from twitter_api.types.v2_search_query.operators.operator import CompleteOperator
from twitter_api.types.v2_search_query.search_query import SearchQuery, build


class TestCashtagOperator:
    def test_cashtag_operator(self):
        assert str(CashtagOperator("Twitter")) == "$Twitter"

    def test_cashtag_operator_with_mark(self):
        assert str(CashtagOperator("$Twitter")) == "$Twitter"

    def test_cashtag_operator_with_double_quote(self):
        with pytest.raises(SearchQueryDoubleQuotedError):
            CashtagOperator('$"Twitter"')

    def test_query_complete(self):
        assert isinstance(
            build(lambda q: q.cashtag("Twitter")),
            CompleteOperator,
        )

    def test_query_build(self):
        assert str(SearchQuery.build(lambda q: q.cashtag("Twitter"))) == "$Twitter"
