import pytest

from tests.conftest import synthetic_monitoring_is_disable
from tests.data import JsonDataLoader
from twitter_api.api.resources.v2_tweets_search_stream_rules.post_v2_tweets_search_stream_rules import (
    PostV2TweetsSearchStreamRulesResponseBody,
)
from twitter_api.client.twitter_api_mock_client import TwitterApiMockClient
from twitter_api.client.twitter_api_real_client import TwitterApiRealClient


@pytest.mark.skipif(**synthetic_monitoring_is_disable())
class TestPostV2TweetsSearchStreamRules:
    def test_post_v2_search_stream_rules_when_add_case(
        self, real_oauth2_app_client: TwitterApiRealClient
    ):
        real_response = (
            real_oauth2_app_client.chain()
            .request("https://api.twitter.com/2/tweets/search/stream/rules")
            .post(
                {
                    "add": [
                        {"value": "cat has:media"},
                    ]
                },
                {"dry_run": True},
            )
        )

        print(real_response.json())

        assert True

    def test_post_v2_search_stream_rules_when_delete_case(
        self, real_oauth2_app_client: TwitterApiRealClient
    ):
        real_response = (
            real_oauth2_app_client.chain()
            .request("https://api.twitter.com/2/tweets/search/stream/rules")
            .post(
                {"delete": {"values": ["cat has:media"]}},
            )
        )

        print(real_response.json())

        assert True


class TestMockPostV2TweetsSearchStreamRules:
    @pytest.mark.parametrize(
        "json_filename",
        [
            "post_v2_search_stream_rules_response_create_rules.json",
            "post_v2_search_stream_rules_response_success.json",
        ],
    )
    def test_mock_post_v2_search_stream_rules(
        self,
        mock_oauth2_app_client: TwitterApiMockClient,
        json_data_loader: JsonDataLoader,
        json_filename: str,
    ):
        expected_response = PostV2TweetsSearchStreamRulesResponseBody.parse_obj(
            json_data_loader.load(json_filename)
        )

        assert (
            mock_oauth2_app_client.chain()
            .inject_post_response_body(
                "https://api.twitter.com/2/tweets/search/stream/rules",
                expected_response,
            )
            .request("https://api.twitter.com/2/tweets/search/stream/rules")
            .post(
                {
                    "add": [
                        {"value": "cat has:media"},
                    ]
                }
            )
        ) == expected_response