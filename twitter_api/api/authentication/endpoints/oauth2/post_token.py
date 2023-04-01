import base64
from typing import Literal, TypedDict

from twitter_api.client.request.request_client import RequestClient
from twitter_api.types.endpoint import Endpoint
from twitter_api.types.extra_permissive_model import ExtraPermissiveModel
from twitter_api.types.oauth import AccessToken, ApiKey, ApiSecret

Uri = Literal["/oauth2/token"]

ENDPOINT: Endpoint = Endpoint("POST", "/oauth2/token")

PostOauth2TokenRequestBody = TypedDict(
    "PostOauth2TokenRequestBody",
    {
        "grant_type": Literal["client_credentials"],
    },
)


class PostOauth2TokenResponseBody(ExtraPermissiveModel):
    token_type: Literal["bearer"]
    access_token: AccessToken


class PostOauth2Token:
    def __init__(self, client: RequestClient) -> None:
        self._client = client

    def post(
        self,
        api_key: ApiKey,
        api_secret: ApiSecret,
        request_body: PostOauth2TokenRequestBody,
    ) -> PostOauth2TokenResponseBody:
        # flake8: noqa E501
        """
        OAuth 2.0 のアプリ用のアクセストークンのセットを生成するために使用する。

        refer: https://developer.twitter.com/en/docs/authentication/api-reference/token
        """

        bearer_token = base64.b64encode(
            f"{api_key}:{api_secret}".encode(),
        )

        return self._client.post(
            endpoint=ENDPOINT,
            response_type=PostOauth2TokenResponseBody,
            auth=False,
            headers={
                "Authorization": f"Basic {bearer_token.decode()}",
                "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
            },
            query=request_body,
        )
