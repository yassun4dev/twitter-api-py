from textwrap import dedent

import pytest

from tests.conftest import synthetic_monitoring_is_disable
from twitter_api.api.v2.endpoints.tweets.get_tweets import V2GetTweetsResponseBody
from twitter_api.api.v2.types.tweet.tweet import Tweet
from twitter_api.client.twitter_api_mock_client import TwitterApiMockClient
from twitter_api.client.twitter_api_real_client import TwitterApiRealClient


@pytest.fixture
def tweets() -> list[Tweet]:
    return [
        Tweet(
            id="1460323737035677698",
            text=dedent(
                # flake8: noqa E501
                """
                Introducing a new era for the Twitter Developer Platform! \n
                📣The Twitter API v2 is now the primary API and full of new features
                ⏱Immediate access for most use cases, or apply to get more access for free
                📖Removed certain restrictions in the Policy
                https://t.co/Hrm15bkBWJ https://t.co/YFfCDErHsg
                """
            ).strip(),
            edit_history_tweet_ids=["1460323737035677698"],
        )
    ]


@pytest.mark.skipif(**synthetic_monitoring_is_disable())
class TestV2GetTweets:
    def test_get_tweets(self, real_client: TwitterApiRealClient, tweets: list[Tweet]):
        expected_response = V2GetTweetsResponseBody(data=tweets)
        real_response = real_client.request("/2/tweets").get(
            {"ids": list(map(lambda tweet: tweet.id, tweets))}
        )

        print(real_response.dict())
        print(expected_response.dict())

        assert real_response == expected_response


@pytest.mark.skipif(**synthetic_monitoring_is_disable())
class TestMockV2GetTweets:
    def test_mock_get_tweets(self, mock_client: TwitterApiMockClient):
        tweet = Tweet(
            id="12345",
            text="tweet",
            edit_history_tweet_ids=["56789"],
        )

        response = V2GetTweetsResponseBody(data=[tweet for _ in range(10)])

        assert (
            mock_client.chain()
            .inject_get_response("/2/tweets", response)
            .request("/2/tweets")
            .get({"ids": list(map(lambda tweet: tweet.id, response.data))})
            == response
        )
