import asyncio

from flibusta_bot.flibusta_parser.app import App as ParserApp


async def main():
    query = "хаос"
    async with ParserApp() as app:
        search_results = await app.search_book(query)
        print(search_results[0])
        print()
        print(search_results[1])


if __name__ == "__main__":
    asyncio.run(main())
