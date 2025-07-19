from urllib.parse import parse_qs, urlparse

from flibusta_bot.parsers import schemas
from flibusta_bot.parsers.base_http_client import BaseHttpClient


class HttpClient(BaseHttpClient):
    base_url = "https://www.gutenberg.org/"

    @staticmethod
    def get_page_index(url: str | None) -> str | None:
        if url is None:
            return None
        url_data = urlparse(url)
        query_params = parse_qs(url_data.query)
        return query_params.get("start_index", ["0"])[0]

    async def search_books(
        self, query: str, start_index: str | None = None
    ) -> schemas.HttpResponse | None:
        query = query.replace(" ", "+")
        params = {
            "query": query,
        }
        if start_index is not None and start_index != "0":
            params["start_index"] = start_index
        url = f"{self.base_url}ebooks/search/"
        res = await self.make_request(url, params=params)
        return res
