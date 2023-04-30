import sys
from textwrap import dedent
from typing import Callable, Generic, Optional, Self, TextIO

from twitter_api.client.oauth_session.twitter_oauth1_session import TwitterOAuth1Session
from twitter_api.types.chainable import Chainable
from twitter_api.types.generic_client import TwitterApiGenericClient
from twitter_api.types.http import Url


class OAuth1Authorization(Chainable, Generic[TwitterApiGenericClient]):
    def __init__(
        self,
        authorization_url: Url,
        session: TwitterOAuth1Session[TwitterApiGenericClient],
    ) -> None:
        self.authorization_url = authorization_url
        self._session = session

    def open_request_url(self) -> Self:
        """
        ブラウザで認証画面を開く。
        """
        import webbrowser

        webbrowser.open(self.authorization_url)
        return self

    def print_request_url(
        self,
        message_function: Optional[Callable[[Url], str]] = None,
        file: TextIO = sys.stderr,
    ) -> Self:
        """
        コンソール上に認証画面の URL を出力する。
        """
        if message_function is None:

            def default_message_function(url: Url):
                return dedent(
                    f"""
                    =====================================================
                      Please open Authorization URL using your browser.
                    =====================================================

                    {url}

                    """
                )

            message_function = default_message_function

        print(message_function(self.authorization_url), file=file)

        return self

    def input_response_url(
        self,
        input_url: Optional[Url] = None,
        *,
        message_function: Optional[Callable[[], str]] = None,
        file: TextIO = sys.stderr,
    ):
        """
        認証画面で承認した後にリダイレクトされるコールバックURL を入力する。

        引数の input_url に値を入れると、プロンプトで問い合わせを行わない。
        """

        from twitter_api.client.oauth_flow.twitter_oauth1_access_token_client import (
            TwitterOAuth1AccessTokenClient,
        )

        if input_url is None:
            input_url = ""

        if message_function is None:

            def default_message_function():
                return "Please input Authorization Response URL: "

            message_function = default_message_function

        while True:
            if input_url != "":
                break

            file.write(message_function())
            input_url = input()

        return TwitterOAuth1AccessTokenClient(
            authorization_response_url=input_url,
            session=self._session,
        )
