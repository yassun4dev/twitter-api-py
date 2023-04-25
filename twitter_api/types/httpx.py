from typing import Any, Callable, Mapping, TypeAlias

import httpx

Client: TypeAlias = httpx.Client
AsyncClient: TypeAlias = httpx.AsyncClient

Response: TypeAlias = httpx.Response

URLTypes: TypeAlias = httpx._types.URLTypes
ProxiesTypes: TypeAlias = httpx._types.ProxiesTypes
Limits: TypeAlias = httpx.Limits
VerifyTypes = httpx._types.VerifyTypes
Timeout: TypeAlias = httpx.Timeout
TimeoutTypes: TypeAlias = httpx._types.TimeoutTypes

BaseTransport: TypeAlias = httpx.BaseTransport
AsyncBaseTransport: TypeAlias = httpx.AsyncBaseTransport

EventHook = Mapping[str, list[Callable[..., Any]]]

DEFAULT_LIMITS = httpx._config.DEFAULT_LIMITS
DEFAULT_TIMEOUT_CONFIG = httpx._config.DEFAULT_TIMEOUT_CONFIG