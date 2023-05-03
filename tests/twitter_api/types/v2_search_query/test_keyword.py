from twitter_api.types.v2_search_query.keyword import Keyword
from twitter_api.types.v2_search_query.search_query import SearchQuery


class TestKeyword:
    def test_keyword(self):
        assert str(Keyword("test")) == "test"

    def test_keyword_with_phrase(self):
        assert str(Keyword("test twitter")) == '"test twitter"'

    def test_keyword_with_phrase_double_quotes(self):
        assert str(Keyword('"test" twitter')) == r'"\"test\" twitter"'

    def test_query_build(self):
        assert str(SearchQuery.build(lambda q: q.keyword("test"))) == "test"
