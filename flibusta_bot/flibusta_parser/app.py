from __future__ import annotations

from . import html_parser, schemas
from .http_client import HttpClient

UrlPages = list[str]


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
        self, book_info: schemas.BookListingData, previous_url: str | None = None
    ) -> schemas.BookInfoData | None:
        previous_url = previous_url or self.http_client.base_url
        response = await self.http_client.get_book_info(book_info.book_id, previous_url)
        if not response:
            return None
        book_data = html_parser.parse_book_info(response.content, book_info)
        return book_data
