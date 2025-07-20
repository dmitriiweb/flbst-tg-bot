from __future__ import annotations

from flibusta_bot.parsers.gutenberg import html_parser

from . import schemas
from .http_client import HttpClient


class App:
    def __init__(self):
        self.http_client = HttpClient()

    async def __aenter__(self) -> App:
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.http_client.__aexit__(exc_type, exc_val, exc_tb)

    def get_download_url(self, book_id: str, download_format: str) -> str:
        return f"{self.http_client.base_url}ebooks/{book_id}.{download_format}"

    async def search_books(
        self, query: str, start_index: str | None = None
    ) -> tuple[list[schemas.BookListingData], str | None, str | None]:
        """
        Returns:
            tuple[list[schemas.BookListingData], str | None, str | None]:
                - list of books
                - next index or None if there is no next page
                - prev index or None if there is no previous page
        """
        response = await self.http_client.search_books(query, start_index)
        if not response:
            return [], None, None
        books = html_parser.parse_books(response.content)
        next_page = html_parser.get_next_page_url(response.content)
        prev_page = html_parser.get_prev_page_url(response.content)
        next_index = self.http_client.get_page_index(next_page)
        prev_index = self.http_client.get_page_index(prev_page)
        return books, next_index, prev_index

    async def get_book_info(self, book_id: str) -> schemas.BookInfoData | None:
        response = await self.http_client.get_book_info(book_id)
        if not response:
            return None
        return html_parser.parse_book_info(response.content)

    async def download_book(
        self, book_id: str, download_format: str
    ) -> schemas.BinaryHttpResponse | None:
        url = self.get_download_url(book_id, download_format)
        response = await self.http_client.download_book_by_url(url)
        if not response:
            return None
        return response.content
