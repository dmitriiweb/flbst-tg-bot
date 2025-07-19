from flibusta_bot.parsers import schemas
from flibusta_bot.parsers.base_http_client import BaseHttpClient


class HttpClient(BaseHttpClient):
    base_url = "https://www.gutenberg.org/"

    async def search_books(self, query: str) -> schemas.HttpResponse | None:
        query = query.replace(" ", "+")
        url = f"{self.base_url}ebooks/search/?query={query}"
        res = await self.make_request(url)
        return res
