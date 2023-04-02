from typing import Literal

from twitter_api.api.v2.endpoints.users.get_user import V2GetUser
from twitter_api.client.request.request_client import RequestClient

from .get_users import V2GetUsers

UsersUrl = Literal["https://api.twitter.com/2/users"]
UserUrl = Literal["https://api.twitter.com/2/users/:id"]


class V2User(V2GetUser):
    def __init__(self, client: RequestClient) -> None:
        self._client = client

    @property
    def request_client(self) -> RequestClient:
        return self._client


class V2Users(V2GetUsers):
    def __init__(self, client: RequestClient) -> None:
        self._client = client

    @property
    def request_client(self) -> RequestClient:
        return self._client