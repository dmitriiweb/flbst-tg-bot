from __future__ import annotations

from .http_client import HttpClient


class App:
    def __init__(self):
        self.http_client = HttpClient()

    async def __aenter__(self) -> App:
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.http_client.__aexit__(exc_type, exc_val, exc_tb)
