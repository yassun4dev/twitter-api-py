from twitter_api.types.v2_search_query.operators.operator import CompleteOperator
from twitter_api.types.v2_search_query.operators.point_radius_operator import (
    PointRadiusOperator,
)
from twitter_api.types.v2_search_query.search_query import SearchQuery, build


class TestPointRadiusOperator:
    def test_point_radius_operator_when_radius_km(self):
        assert (
            str(
                PointRadiusOperator(
                    longitude_deg=2.355128,
                    latitude_deg=48.861118,
                    radius_km=5,
                )
            )
            == "point_radius:[2.355128 48.861118 5km]"
        )

    def test_point_radius_operator_when_radius_mi(self):
        assert (
            str(
                PointRadiusOperator(
                    longitude_deg=2.355128,
                    latitude_deg=48.861118,
                    radius_mi=5,
                )
            )
            == "point_radius:[2.355128 48.861118 5mi]"
        )

    def test_query_complete(self):
        assert isinstance(
            build(
                lambda q: q.point_radius(
                    longitude_deg=2.355128,
                    latitude_deg=48.861118,
                    radius_km=5,
                )
            ),
            CompleteOperator,
        )

    def test_query_build_when_radius_km(self):
        assert (
            str(
                SearchQuery.build(
                    lambda q: q.point_radius(
                        longitude_deg=2.355128,
                        latitude_deg=48.861118,
                        radius_km=5,
                    )
                )
            )
            == "point_radius:[2.355128 48.861118 5km]"
        )

    def test_query_build_when_radius_mi(self):
        assert (
            str(
                SearchQuery.build(
                    lambda q: q.point_radius(
                        longitude_deg=2.355128,
                        latitude_deg=48.861118,
                        radius_mi=5,
                    )
                )
            )
            == "point_radius:[2.355128 48.861118 5mi]"
        )
