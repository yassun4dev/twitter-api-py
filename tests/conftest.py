import os

import pytest

from tests.data import JsonDataLoader
from twitter_api.client.twitter_api_mock_client import TwitterApiMockClient
from twitter_api.client.twitter_api_real_client import TwitterApiRealClient


def synthetic_monitoring_is_disable() -> dict:
    """
    外形監視が無効であるかどうかを確認する。

    下記の環境変数を設定すると、実際に API を叩いてテストが行われる。

    ```env
    SYNTHETIC_MONITORING_TEST=true
    ```
    """

    return dict(
        condition=(
            "SYNTHETIC_MONITORING_TEST" not in os.environ
            or os.environ["SYNTHETIC_MONITORING_TEST"].lower() != "true"
        ),
        reason="外形監視が有効時（環境変数 SYNTHETIC_MONITORING_TEST が true ）に実行されます。",
    )


@pytest.fixture
def json_data_loader() -> JsonDataLoader:
    return JsonDataLoader()


@pytest.fixture
def real_oauth2_bearer_client() -> TwitterApiRealClient:
    return TwitterApiRealClient.from_oauth2_bearer_token_env()


@pytest.fixture
def real_oauth2_app_client() -> TwitterApiRealClient:
    return TwitterApiRealClient.from_oauth2_app_env()


@pytest.fixture
def real_oauth2_user_client() -> TwitterApiRealClient:
    return TwitterApiRealClient.from_oauth2_bearer_token_env("OAUTH2_USER_ACCESS_TOKEN")


@pytest.fixture
def real_auth1_user_client() -> TwitterApiRealClient:
    return TwitterApiRealClient.from_oauth1_user_env()


@pytest.fixture
def mock_oauth2_app_client() -> TwitterApiMockClient:
    return TwitterApiMockClient(
        oauth_version="2.0",
        rate_limit_target="app",
    )


@pytest.fixture
def mock_oauth2_user_client() -> TwitterApiMockClient:
    return TwitterApiMockClient(
        oauth_version="2.0",
        rate_limit_target="user",
    )


@pytest.fixture
def mock_oauth1_app_client() -> TwitterApiMockClient:
    return TwitterApiMockClient(
        oauth_version="1.0a",
        rate_limit_target="app",
    )


@pytest.fixture
def mock_oauth1_user_client() -> TwitterApiMockClient:
    return TwitterApiMockClient(
        oauth_version="1.0a",
        rate_limit_target="user",
    )
