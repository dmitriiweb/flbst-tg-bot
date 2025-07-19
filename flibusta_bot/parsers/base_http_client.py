from typing import Any

import httpx
from loguru import logger

from flibusta_bot.parsers import schemas


class BaseHttpClient:
    default_headers = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "accept-language": "en-US,en;q=0.9,ru;q=0.8",
        "dnt": "1",
        "priority": "u=0, i",
        "sec-ch-ua": '"Chromium";v="134", "Not:A-Brand";v="24", "Google Chrome";v="134"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Linux"',
        "sec-fetch-dest": "document",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "same-origin",
        "sec-fetch-user": "?1",
        "upgrade-insecure-requests": "1",
        "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36",
    }

    def __init__(self):
        self.client = httpx.AsyncClient(follow_redirects=True, timeout=600)

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.client.aclose()

    async def make_request(
        self,
        url: str,
        headers: dict[str, Any] | None = None,
        params: dict[str, Any] | None = None,
    ) -> schemas.HttpResponse | None:
        headers = headers or self.default_headers
        try:
            response = await self.client.get(url, headers=headers, params=params)
        except Exception:
            logger.error(f"Error while making request: {url=}")
            return None
        if response.status_code != 200:
            logger.error(f"Error while making request: {response.status_code} | {url=}")
            return None
        return schemas.HttpResponse(
            status_code=response.status_code,
            content=response.text,
            headers=dict(response.headers),
            url=url,
        )
