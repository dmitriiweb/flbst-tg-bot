from __future__ import annotations

from flibusta_bot.parsers.gutenberg import html_parser

from .http_client import HttpClient
from . import schemas

class App:
    def __init__(self):
        self.http_client = HttpClient()

    async def __aenter__(self) -> App:
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.http_client.__aexit__(exc_type, exc_val, exc_tb)


    async def search_books(self, query: str) -> tuple[list[schemas.BookListingData], str | None]:
        """
        Returns:
            tuple[list[schemas.BookListingData], str | None]:
                - list of books
                - next page url or None if there is no next page
        """
        response = await self.http_client.search_books(query)
        if not response:
            return [], None
        books = html_parser.parse_books(response.content)
        next_page = html_parser.get_next_page_url(response.content)
        return books, next_page

    async def get_book_info(self, url: str) -> schemas.BookInfoData | None:
        response = await self.http_client.make_request(url)
        if not response:
            return None
        return html_parser.parse_book_info(response.content)