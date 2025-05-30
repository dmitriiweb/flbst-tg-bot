from .tg_bot import App

"""
# from flibusta_bot.flibusta_parser.app import App as ParserApp

    query = "хаос"
    async with ParserApp() as app:
        search_results = await app.search_book(query)
        print(search_results[0])
        print()
        print(search_results[1])

"""


def main():
    app = App()
    app.run()


if __name__ == "__main__":
    main()
