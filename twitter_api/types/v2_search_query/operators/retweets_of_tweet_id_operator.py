from twitter_api.types.v2_tweet.tweet_id import TweetId

from .operator import InvertibleOperator, Operator, StandaloneOperator


class RetweetsOfTweetIdOperator(
    InvertibleOperator[Operator],
    StandaloneOperator[Operator],
):
    def __init__(self, id: TweetId):
        self._value = id

    def __str__(self) -> str:
        return f"retweets_of_tweet_id:{self._value}"
