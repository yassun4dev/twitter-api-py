import asyncio
import time
from abc import ABCMeta, abstractmethod
from contextlib import asynccontextmanager, contextmanager
from logging import getLogger

from twitter_api.error import TwitterApiErrorCode, TwitterApiResponseFailed
from twitter_api.rate_limit.manager.checkers.rate_limit_checker import RateLimitChecker
from twitter_api.rate_limit.manager.rate_limit_manager import RateLimitManager
from twitter_api.rate_limit.rate_limit_info import RateLimitInfo
from twitter_api.warning import RateLimitOverWarning, UnmanagedRateLimitOverWarning

logger = getLogger(__file__)

DEFAULT_MIN_RANDOM_SLEEP_SECONDS = 5 * 60
DEFAULT_MAX_RANDOM_SLEEP_SECONDS = 15 * 60


class SleepRateLimitMixin(RateLimitChecker, RateLimitManager, metaclass=ABCMeta):
    """
    レートリミットに遭遇した場合、スリープする handler。
    """

    @abstractmethod
    def random_sleep_seconds(self) -> int:
        """
        予期しないレートリミットに遭遇した場合にランダムに休む時間[秒]。
        """

        ...

    @contextmanager
    def handle_rate_limit_sync(self, rate_limit_info: RateLimitInfo):
        while True:
            # レートリミットを超えてしまっていたら、必要な待ち時間分だけ待つ。
            if wait_time_seconds := self.check_limit_over(rate_limit_info):
                logger.warning(RateLimitOverWarning(rate_limit_info))
                time.sleep(wait_time_seconds)
                continue

            try:
                yield
                return

            except TwitterApiResponseFailed as error:
                # レートリミット以外のエラーなら上流に投げる。
                if error.status_code != TwitterApiErrorCode.TooManyRequests.value:
                    raise error

                # 予期しないレートリミットに遭遇した場合、投機的な待機を行う
                logger.warning(UnmanagedRateLimitOverWarning())
                time.sleep(self.random_sleep_seconds())

    @asynccontextmanager
    async def handle_rate_limit_async(self, rate_limit_info: RateLimitInfo):
        while True:
            # レートリミットを超えてしまっていたら、必要な待ち時間分だけ待つ。
            if wait_time_seconds := self.check_limit_over(rate_limit_info):
                logger.warning(RateLimitOverWarning(rate_limit_info))
                await asyncio.sleep(wait_time_seconds)
                continue

            try:
                yield
                return

            except TwitterApiResponseFailed as error:
                # レートリミットのエラーでないなら上流に投げる。
                if error.status_code != TwitterApiErrorCode.TooManyRequests.value:
                    raise error

                # 予期しないレートリミットに遭遇した場合、投機的な待機を行う
                logger.warning(UnmanagedRateLimitOverWarning())
                await asyncio.sleep(self.random_sleep_seconds())