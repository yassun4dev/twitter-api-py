import pytest

from tests.conftest import synthetic_monitoring_is_disable
from tests.data import JsonDataLoader
from twitter_api.api.resources.v2_user.get_v2_user import GetV2UserResponseBody
from twitter_api.client.twitter_api_mock_client import TwitterApiMockClient
from twitter_api.client.twitter_api_real_client import TwitterApiRealClient
from twitter_api.types.extra_permissive_model import has_extra_fields


@pytest.mark.skipif(**synthetic_monitoring_is_disable())
class TestGetV2User:
    def test_get_v2_user(
        self,
        real_oauth2_app_client: TwitterApiRealClient,
    ):
        response = (
            real_oauth2_app_client.chain()
            .request("https://api.twitter.com/2/users/:id")
            .get("2244994945")
        )

        print(response.json())

        assert not has_extra_fields(response)


class TestMockGetV2User:
    @pytest.mark.parametrize(
        "json_filename",
        [
            "get_v2_user_response.json",
        ],
    )
    def test_mock_get_v2_user(
        self,
        mock_oauth2_app_client: TwitterApiMockClient,
        json_data_loader: JsonDataLoader,
        json_filename: str,
    ):
        expected_response = GetV2UserResponseBody.parse_obj(
            json_data_loader.load(json_filename)
        )

        assert not has_extra_fields(expected_response)

        assert (
            mock_oauth2_app_client.chain()
            .inject_get_response_body(
                "https://api.twitter.com/2/users/:id", expected_response
            )
            .request("https://api.twitter.com/2/users/:id")
            .get("2244994945")
        ) == expected_response
