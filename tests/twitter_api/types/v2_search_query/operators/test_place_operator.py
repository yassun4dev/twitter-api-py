from twitter_api.types.v2_search_query.operators.operator import CompleteOperator
from twitter_api.types.v2_search_query.operators.place_operator import PlaceOperator
from twitter_api.types.v2_search_query.search_query import SearchQuery, build


class TestPlaceOperator:
    def test_place_operator_from_id(self):
        assert str(PlaceOperator("fd70c22040963ac7")) == "place:fd70c22040963ac7"

    def test_place_operator_from_full_name(self):
        assert str(PlaceOperator("seattle")) == "place:seattle"

    def test_place_operator_from_multi_word_full_name(self):
        assert str(PlaceOperator("new york city")) == 'place:"new york city"'

    def test_query_complete(self):
        assert isinstance(
            build(lambda q: q.place("seattle")),
            CompleteOperator,
        )

    def test_query_build_from_id(self):
        assert (
            str(SearchQuery.build(lambda q: q.place("fd70c22040963ac7")))
            == "place:fd70c22040963ac7"
        )

    def test_query_build_from_full_name(self):
        assert str(SearchQuery.build(lambda q: q.place("seattle"))) == "place:seattle"
