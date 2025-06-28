import io
from typing import Any, Literal

import httpx
from loguru import logger

from flibusta_bot import config

from . import schemas


class HttpClient:
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

    def __init__(self, base_url: str | None = None):
        self.base_url = base_url or config.LIBRARY_BASE_URL.rstrip("/") + "/"
        self.client = httpx.AsyncClient()

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.client.aclose()

    async def _make_request(
        self, path: str, headers: dict[str, Any]
    ) -> schemas.HttpResponse | None:
        url = f"{self.base_url}{path}"
        try:
            response = await self.client.get(url, headers=headers)
        except Exception as e:
            logger.error(f"Error while making request: {e} | {url=}")
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

    async def search_books(self, query: str) -> schemas.HttpResponse | None:
        query = query.replace(" ", "+")
        path = f"booksearch?ask={query}"
        headers = self.default_headers.copy()
        headers["referer"] = self.base_url
        return await self._make_request(path, headers=headers)

    async def get_book_info(
        self, book_id: str, previous_url: str
    ) -> schemas.HttpResponse | None:
        path = f"b/{book_id}"
        headers = self.default_headers.copy()
        headers["referer"] = f"{previous_url}"
        return await self._make_request(path, headers=headers)

    async def download_book(
        self, download_url: str
    ) -> schemas.BinaryHttpResponse | None:
        book = await self._download_book(download_url)
        return book

    async def get_download_book_url(
        self, book_id: str, format: Literal["epub", "fb2", "mobi"]
    ) -> str | None:
        path = f"b/{book_id}/{format}"
        url = f"{self.base_url}{path}"
        headers = self.default_headers.copy()
        headers["referer"] = f"{self.base_url}b/{book_id}"
        try:
            response = await self.client.get(
                url, headers=headers, follow_redirects=True
            )
        except Exception as e:
            logger.error(f"Error while getting download URL: {e} | {url=}")
            return None
        return str(response.url)

    async def _download_book(self, url: str) -> schemas.BinaryHttpResponse | None:
        try:
            response = await self.client.get(url, headers=self.default_headers)
            if response.status_code != 200:
                logger.error(
                    f"Error while downloading book: {response.status_code} | {url=}"
                )
                return None
            return schemas.BinaryHttpResponse(
                status_code=response.status_code,
                content=io.BytesIO(response.content),
                headers=dict(response.headers),
                url=url,
            )
        except Exception as e:
            logger.error(f"Error while downloading book: {e} | {url=}")
            return None

    async def get_file_metadata(self, url: str) -> dict[str, Any] | None:
        try:
            response = await self.client.head(url, headers=self.default_headers)
            if response.status_code != 200:
                logger.error(
                    f"Error while getting file metadata: {response.status_code} | {url=}"
                )
                return None
            return {
                "status_code": response.status_code,
                "headers": dict(response.headers),
                "url": url,
            }
        except Exception as e:
            logger.error(f"Error while getting file metadata: {e} | {url=}")
            return None
