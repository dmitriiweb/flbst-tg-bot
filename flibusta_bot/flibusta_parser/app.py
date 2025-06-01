from __future__ import annotations

import re

from . import html_parser, schemas
from .http_client import HttpClient

UrlPages = list[str]
attacment_re = re.compile(r'filename="?([^";]+)"?')


class App:
    def __init__(self):
        self.http_client = HttpClient()

    async def __aenter__(self) -> App:
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.http_client.__aexit__(exc_type, exc_val, exc_tb)

    async def search_book(
        self, query: str
    ) -> tuple[UrlPages, list[schemas.BookListingData]]:
        response = await self.http_client.search_books(query)
        if not response:
            return [], []

        url_pages = html_parser.get_all_pages_in_listing(response.content, response.url)
        first_page_books = html_parser.parse_listing(response.content)

        return url_pages, first_page_books if first_page_books else []

    async def get_listing_by_url(
        self, url: str, previous_url: str | None
    ) -> list[schemas.BookListingData]:
        headers = self.http_client.default_headers.copy()
        headers["referer"] = previous_url or self.http_client.base_url
        response = await self.http_client.client.get(url, headers=headers)
        if response.status_code != 200:
            return []

        books = html_parser.parse_listing(response.text)
        return books if books else []

    async def get_book_info(
        self, book_id: str | int, previous_url: str | None = None
    ) -> schemas.BookInfoData | None:
        previous_url = previous_url or self.http_client.base_url
        response = await self.http_client.get_book_info(str(book_id), previous_url)
        if not response:
            return None
        book_data = html_parser.parse_book_info(response.content, book_id)
        return book_data

    async def get_download_url(self, url: str) -> str | None:
        url_split = url.split("/")
        book_id = url_split[-2]
        book_format = url_split[-1]
        result = await self.http_client.get_download_book_url(book_id, book_format)
        return result

    async def download_book(self, url: str) -> schemas.BinaryHttpResponse | None:
        response = await self.http_client.download_book(url)
        if not response:
            return None
        return response

    async def get_filename_from_metadata(self, url: str) -> str | None:
        metadata = await self.http_client.get_file_metadata(url)
        if not metadata:
            return None
        headers = metadata.get("headers", {})
        content_disposition = headers.get("content-disposition")
        if not content_disposition:
            return None
        # Example: 'attachment; filename="example.fb2"'

        match = attacment_re.search(content_disposition)
        if match:
            return match.group(1)
        return None
