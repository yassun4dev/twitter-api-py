from datetime import datetime
from typing import Literal, NotRequired, Optional, TypeAlias, TypedDict

from twitter_api.api.resources.api_resources import ApiResources
from twitter_api.api.types.v2_expansion import Expansion
from twitter_api.api.types.v2_media.media_field import MediaField
from twitter_api.api.types.v2_place.place_field import PlaceField
from twitter_api.api.types.v2_poll.poll_field import PollField
from twitter_api.api.types.v2_search_query import SearchQuery
from twitter_api.api.types.v2_tweet.tweet_detail import TweetDetail
from twitter_api.api.types.v2_tweet.tweet_field import TweetField
from twitter_api.api.types.v2_tweet.tweet_id import TweetId
from twitter_api.api.types.v2_user.user_field import UserField
from twitter_api.client.request.request_client import RequestClient
from twitter_api.rate_limit.rate_limit_decorator import rate_limit
from twitter_api.types.comma_separatable import CommaSeparatable, comma_separated_str
from twitter_api.types.endpoint import Endpoint
from twitter_api.types.extra_permissive_model import ExtraPermissiveModel
from twitter_api.utils.functional import map_optional

ENDPOINT = Endpoint("GET", "https://api.twitter.com/2/tweets/search/recent")

GetV2TweetsSearchRecentQueryParameters = TypedDict(
    "GetV2TweetsSearchRecentQueryParameters",
    {
        "query": str | SearchQuery,
        "start_time": NotRequired[Optional[datetime]],
        "end_time": NotRequired[Optional[datetime]],
        "since_id": NotRequired[Optional[TweetId]],
        "until_id": NotRequired[Optional[TweetId]],
        "sort_order": NotRequired[Optional[Literal["recency", "relevancy"]]],
        "next_token": NotRequired[Optional[str]],
        "max_results": NotRequired[Optional[int]],
        "expansions": NotRequired[Optional[CommaSeparatable[Expansion]]],
        "place.fields": NotRequired[Optional[CommaSeparatable[PlaceField]]],
        "media.fields": NotRequired[Optional[CommaSeparatable[MediaField]]],
        "poll.fields": NotRequired[Optional[CommaSeparatable[PollField]]],
        "tweet.fields": NotRequired[Optional[CommaSeparatable[TweetField]]],
        "user.fields": NotRequired[Optional[CommaSeparatable[UserField]]],
    },
)


def _make_query(query: GetV2TweetsSearchRecentQueryParameters) -> dict:
    return {
        "query": str(query["query"]),
        "start_time": map_optional(lambda x: x.isoformat(), query.get("start_time")),
        "end_time": map_optional(lambda x: x.isoformat(), query.get("end_time")),
        "since_id": query.get("since_id"),
        "until_id": query.get("until_id"),
        "sort_order": query.get("sort_order"),
        "next_token": query.get("next_token"),
        "max_results": query.get("expansions"),
        "expansions": comma_separated_str(query.get("expansions")),
        "place.fields": query.get("place.fields"),
        "media.fields": query.get("media.fields"),
        "poll.fields": query.get("poll.fields"),
        "tweet.fields": comma_separated_str(query.get("tweet.fields")),
        "user.fields": comma_separated_str(query.get("user.fields")),
    }


class GetV2TweetsSearchRecentResponseBodyMeta(ExtraPermissiveModel):
    result_count: int
    next_token: Optional[str] = None


class GetV2TweetsSearchRecentResponseBody(ExtraPermissiveModel):
    data: Optional[list[TweetDetail]] = None
    meta: GetV2TweetsSearchRecentResponseBodyMeta


class GetV2TweetsSearchRecentResources(ApiResources):
    @rate_limit(ENDPOINT, "app", requests=450, mins=15)
    @rate_limit(ENDPOINT, "user", requests=180, mins=15)
    def get(
        self, query: GetV2TweetsSearchRecentQueryParameters
    ) -> GetV2TweetsSearchRecentResponseBody:
        # flake8: noqa E501
        """
        ツイートの一覧を検索する。

        refer: https://developer.twitter.com/en/docs/twitter-api/tweets/search/api-reference/get-tweets-search-recent
        """
        return self.request_client.get(
            endpoint=ENDPOINT,
            response_type=GetV2TweetsSearchRecentResponseBody,
            query=_make_query(query) if query is not None else None,
        )