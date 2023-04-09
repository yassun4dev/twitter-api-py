import pytest

from tests.conftest import synthetic_monitoring_is_disable
from tests.contexts.check_oauth2_user_access_token import check_oauth2_user_access_token
from tests.data import JsonDataLoader
from twitter_api.api.resources.v2_dm_conversations.post_v2_dm_conversations import (
    PostV2DmConversationsResponseBody,
)
from twitter_api.api.types.v2_user.user_id import UserId
from twitter_api.client.twitter_api_mock_client import TwitterApiMockClient
from twitter_api.client.twitter_api_real_client import TwitterApiRealClient
from twitter_api.types.extra_permissive_model import has_extra_fields


@pytest.mark.skipif(**synthetic_monitoring_is_disable())
class TestGetV2UserFollowing:
    def test_get_v2_user_following(
        self,
        participant_id: UserId,
        participant_ids: list[UserId],
        real_oauth2_user_client: TwitterApiRealClient,
    ):
        with check_oauth2_user_access_token():
            response = (
                real_oauth2_user_client.chain()
                .request("https://api.twitter.com/2/dm_conversations")
                .post(
                    participant_id,
                    {
                        "conversation_type": "Group",
                        "participant_ids": participant_ids,
                        "message": {
                            "text": "Hello to you two, this is a new group conversation"
                        },
                    },
                )
            )

            print(response.json())

        assert not has_extra_fields(response)


class TestMockGetV2UserFollowing:
    @pytest.mark.parametrize(
        "json_filename",
        [
            "post_v2_dm_conversations.json",
        ],
    )
    def test_mock_get_v2_user_following(
        self,
        mock_oauth2_app_client: TwitterApiMockClient,
        json_data_loader: JsonDataLoader,
        json_filename: str,
    ):
        expected_response = PostV2DmConversationsResponseBody.parse_obj(
            json_data_loader.load(json_filename)
        )

        assert not has_extra_fields(expected_response)

        assert (
            mock_oauth2_app_client.chain()
            .inject_post_response_body(
                "https://api.twitter.com/2/dm_conversations",
                expected_response,
            )
            .request("https://api.twitter.com/2/dm_conversations")
            .post(
                "2244994945",
                {
                    "conversation_type": "Group",
                    "participant_ids": ["944480690", "906948460078698496"],
                    "message": {
                        "text": "Hello to you two, this is a new group conversation"
                    },
                },
            )
        ) == expected_response
