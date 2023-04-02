from datetime import datetime

import pytest

from tests.conftest import synthetic_monitoring_is_disable
from twitter_api.api.v2.endpoints.tweets.delete_tweet import (
    V2DeleteTweetResponseBody,
    V2DeleteTweetResponseBodyData,
)
from twitter_api.client.twitter_api_mock_client import TwitterApiMockClient
from twitter_api.client.twitter_api_real_client import TwitterApiRealClient


@pytest.mark.skipif(**synthetic_monitoring_is_disable())
class TestV2DeleteTweet:
    def test_delete_tweet(self, real_user_auth_v1_client: TwitterApiRealClient):
        tweet_text = f"テストツイート。{datetime.now().isoformat()}"

        tweet = (
            real_user_auth_v1_client.chain()
            .request("https://api.twitter.com/2/tweets")
            .post({"text": tweet_text})
            .data
        )

        real_response = (
            real_user_auth_v1_client.chain()
            .request("https://api.twitter.com/2/tweets/:id")
            .delete(tweet.id)
        )

        print(real_response.dict())

        assert real_response.data.deleted is True


class TestMockV2DeleteTweet:
    def test_mock_delete_tweet(self, mock_app_auth_v2_client: TwitterApiMockClient):
        expected_response = V2DeleteTweetResponseBody(
            data=V2DeleteTweetResponseBodyData(deleted=True)
        )

        assert (
            mock_app_auth_v2_client.chain()
            .inject_delete_response(
                "https://api.twitter.com/2/tweets/:id", expected_response
            )
            .request("https://api.twitter.com/2/tweets/:id")
            .delete("1234567890123456789")
            == expected_response
        )
