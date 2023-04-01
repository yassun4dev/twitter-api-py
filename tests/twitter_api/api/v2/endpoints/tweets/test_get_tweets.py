from twitter_api.api.v2.endpoints.tweets.get_tweets import GetTweetsResponseBody
from twitter_api.api.v2.types.tweet.tweet import Tweet
from twitter_api.client.twitter_api_mock_client import TwitterApiMockClient


class TestV2GetTweets:
    def test_mock_get_tweets(self, mock_client: TwitterApiMockClient):
        tweet = Tweet(
            id="12345",
            text="tweet",
            edit_history_tweet_ids=["56789"],
        )

        response = GetTweetsResponseBody(data=[tweet for _ in range(10)])

        assert (
            mock_client.chain()
            .inject_get_response("/2/tweets", response)
            .request("/2/tweets")
            .get({"ids": list(map(lambda tweet: tweet.id, response.data))})
            == response
        )
