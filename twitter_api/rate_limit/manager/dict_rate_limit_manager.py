from bisect import bisect_left
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Optional

from twitter_api.rate_limit.manager.rate_limit_manager import RateLimitManager
from twitter_api.rate_limit.rate_limit_info import RateLimitInfo


@dataclass
class RateLimitStatus:
    start_datetime: datetime
    request_datetimes: list[datetime]


class DictRateLimitManager(RateLimitManager):
    """
    単純なハッシュマップによるレートリミットの管理を行うマネージャ。

    Redis, RDS などで管理したい場合は、
    このクラスを参考に RateLimitManager を実装すればよい。
    """

    def __init__(self) -> None:
        self._store: dict[RateLimitInfo, RateLimitStatus] = {}

    def check_limit_over(
        self,
        rate_limit_info: RateLimitInfo,
        now: Optional[datetime] = None,
    ) -> bool:
        if now is None:
            now = datetime.now()

        if rate_limit_info not in self._store:
            self._store[rate_limit_info] = RateLimitStatus(
                start_datetime=now, request_datetimes=[now]
            )

        # 今回のデータを履歴に追加する。
        status = self._store[rate_limit_info]
        status.request_datetimes.append(now)

        # レートリミットの計算対象より過去のデータを履歴から消す。
        min_datetime = now - timedelta(seconds=rate_limit_info.total_seconds)
        index = bisect_left(status.request_datetimes, min_datetime)
        del status.request_datetimes[:index]

        # 窓に入っているデータの数が、制限を超えていたらリミットオーバ
        return len(status.request_datetimes) > rate_limit_info.requests