import pytest

from tests.conftest import synthetic_monitoring_is_disable
from twitter_api.client.twitter_api_real_client import TwitterApiRealClient


class TestTwitterApiRealClient:
    @pytest.mark.skipif(**synthetic_monitoring_is_disable())
    def test_real_client(self, oauth2_app_real_client: TwitterApiRealClient):
        # インターフェースの未実装がないかをテストする。
        # TestTwitterApiMockClient はテストで必ずテストされるので、テスト不要。
        assert isinstance(oauth2_app_real_client, TwitterApiRealClient)

    @pytest.mark.skipif(**synthetic_monitoring_is_disable())
    def test_real_client_from_oauth2_bearer_token(self):
        assert isinstance(
            TwitterApiRealClient.from_oauth2_bearer_token_env(),
            TwitterApiRealClient,
        )

    @pytest.mark.skipif(**synthetic_monitoring_is_disable())
    def test_real_client_from_oauth2_app_env(self):
        assert isinstance(
            TwitterApiRealClient.from_oauth2_app_env(),
            TwitterApiRealClient,
        )

    @pytest.mark.skipif(**synthetic_monitoring_is_disable())
    def test_real_client_from_oauth1_app_env(self):
        assert isinstance(
            TwitterApiRealClient.from_oauth1_app_env(),
            TwitterApiRealClient,
        )
