import asyncio
from flibusta_bot.parsers.gutenberg.app import App


async def main():
    async with App() as app:
        # Test search functionality
        print("=== Testing Search ===")
        books, next_page = await app.search_books("Leo tolstoy")
        
        print(f"Found {len(books)} books")
        print(f"Next page: {next_page}")
        
        for i, book in enumerate(books[:3], 1):
            print(f"{i}. {book.title} by {book.author}")
            print(f"   URL: {book.url}")
            print()
        
        # Test book info functionality
        if books:
            print("=== Testing Book Info ===")
            first_book = books[0]
            book_info = await app.get_book_info(first_book.url)
            
            if book_info:
                print(f"Title: {book_info.title}")
                print(f"Author: {book_info.author}")
                print(f"Description: {book_info.description[:200]}...")
                print(f"Download formats:")
                for download in book_info.download_urls:
                    print(f"  - {download.title}: {download.url}")
                    print(f"    File format: {download.file_format}")
                    print()
            else:
                print("Failed to get book info")


if __name__ == "__main__":
    asyncio.run(main()) 