import re
from collections.abc import Awaitable, Callable
from typing import Self

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware


class SlashNormalizerMiddleware(BaseHTTPMiddleware):
    async def dispatch(
        self: Self, request: Request, call_next: Callable[[Request], Awaitable[Response]]
    ) -> Response:
        normalized_path = re.sub(r"/+", "/", request.url.path)
        scope = dict(request.scope)
        scope["path"] = normalized_path
        normalized_request = Request(scope, receive=request.receive)

        return await call_next(normalized_request)
