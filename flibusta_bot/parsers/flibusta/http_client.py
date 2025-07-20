# -*- coding: utf-8 -*-
import io
from typing import Any, Literal

from loguru import logger

from flibusta_bot import config
from flibusta_bot.parsers.base_http_client import BaseHttpClient

from .. import schemas


class HttpClient(BaseHttpClient):
    base_url = config.LIBRARY_BASE_URL.rstrip("/") + "/"

    async def search_books(self, query: str) -> schemas.HttpResponse | None:
        query = query.replace(" ", "+")
        path = f"booksearch?ask={query}"
        headers = self.default_headers.copy()
        headers["referer"] = self.base_url
        return await self.make_request(f"{self.base_url}{path}", headers=headers)

    async def get_book_info(
        self, book_id: str, previous_url: str
    ) -> schemas.HttpResponse | None:
        path = f"b/{book_id}"
        headers = self.default_headers.copy()
        headers["referer"] = f"{previous_url}"
        return await self.make_request(f"{self.base_url}{path}", headers=headers)

    async def download_book(
        self, download_url: str
    ) -> schemas.BinaryHttpResponse | None:
        book = await self.download_book_by_url(download_url)
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

    async def get_author_books(self, author_url: str) -> schemas.HttpResponse | None:
        headers = self.default_headers.copy()
        headers["referer"] = self.base_url
        # author_url may be absolute or relative; ensure it's relative
        if author_url.startswith("http"):
            # Remove base_url if present
            if author_url.startswith(self.base_url):
                path = author_url[len(self.base_url) :]
            else:
                # fallback: treat as full URL
                path = author_url
        else:
            path = author_url.lstrip("/")
        return await self.make_request(f"{self.base_url}{path}", headers=headers)
