from datetime import datetime
from typing import Literal, NotRequired, Optional, TypedDict
from urllib import parse

from pydantic import Field

from twitter_api.api.resources.api_resources import ApiResources
from twitter_api.api.types.v2_expansion import Expansion
from twitter_api.api.types.v2_media.media import Media
from twitter_api.api.types.v2_media.media_field import MediaField
from twitter_api.api.types.v2_place.place import Place
from twitter_api.api.types.v2_place.place_field import PlaceField
from twitter_api.api.types.v2_poll.poll import Poll
from twitter_api.api.types.v2_poll.poll_field import PollField
from twitter_api.api.types.v2_scope import oauth2_scopes
from twitter_api.api.types.v2_search_query import SearchQuery
from twitter_api.api.types.v2_tweet.tweet import Tweet
from twitter_api.api.types.v2_tweet.tweet_detail import TweetDetail
from twitter_api.api.types.v2_tweet.tweet_field import TweetField
from twitter_api.api.types.v2_tweet.tweet_id import TweetId
from twitter_api.api.types.v2_user.user import User
from twitter_api.api.types.v2_user.user_field import UserField
from twitter_api.rate_limit.rate_limit_decorator import rate_limit
from twitter_api.types.comma_separatable import CommaSeparatable, comma_separated_str
from twitter_api.types.endpoint import Endpoint
from twitter_api.types.extra_permissive_model import ExtraPermissiveModel
from twitter_api.utils.datetime import rfc3339
from twitter_api.utils.functional import map_optional

ENDPOINT = Endpoint("GET", "https://api.twitter.com/2/tweets/search/all")

GetV2TweetsSearchAllQueryParameters = TypedDict(
    "GetV2TweetsSearchAllQueryParameters",
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


def _make_query(query: GetV2TweetsSearchAllQueryParameters) -> dict:
    return {
        "query": parse.quote(str(query["query"])),
        "start_time": map_optional(rfc3339, query.get("start_time")),
        "end_time": map_optional(rfc3339, query.get("end_time")),
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


class GetV2TweetsSearchAllResponseBodyMeta(ExtraPermissiveModel):
    result_count: int
    next_token: Optional[str] = None
    previous_token: Optional[str] = None


class GetV2TweetsSearchAllResponseBodyIncludes(ExtraPermissiveModel):
    users: list[User] = Field(default_factory=list)
    tweets: list[TweetDetail] = Field(default_factory=list)
    places: list[Place] = Field(default_factory=list)
    media: list[Media] = Field(default_factory=list)
    polls: list[Poll] = Field(default_factory=list)


class GetV2TweetsSearchAllResponseBody(ExtraPermissiveModel):
    data: list[Tweet]
    meta: GetV2TweetsSearchAllResponseBodyMeta
    includes: Optional[GetV2TweetsSearchAllResponseBodyIncludes] = None
    errors: Optional[list[dict]] = None


class GetV2TweetsSearchAllResources(ApiResources):
    @oauth2_scopes(
        "tweet.read",
        "users.read",
    )
    @rate_limit(ENDPOINT, "app", requests=300, mins=15)
    @rate_limit(ENDPOINT, "app", requests=1, seconds=1)
    def get(
        self, query: GetV2TweetsSearchAllQueryParameters
    ) -> GetV2TweetsSearchAllResponseBody:
        """
        ツイートの一覧を検索する。

        refer: https://developer.twitter.com/en/docs/twitter-api/tweets/search/api-reference/get-tweets-search-all
        """
        return self.request_client.get(
            endpoint=ENDPOINT,
            response_type=GetV2TweetsSearchAllResponseBody,
            query=_make_query(query) if query is not None else None,
        )
