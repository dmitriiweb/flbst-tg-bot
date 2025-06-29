import urllib.parse

import lxml.html as lh
from loguru import logger

from flibusta_bot import config
from flibusta_bot.flibusta_parser import schemas


def get_all_pages_in_listing(html: str, first_url: str) -> list[str]:
    tree: lh.HtmlElement = lh.fromstring(html)
    try:
        last_page_element = tree.xpath('.//li[@class="pager-last last"]/a/@href')[0]
    except Exception as _:
        return []
    if last_page_element is None:
        return []

    # Parse the page number from the query string robustly
    parsed = urllib.parse.urlparse(last_page_element)
    qs = urllib.parse.parse_qs(parsed.query)
    try:
        last_page_number = int(qs.get("page", [1])[0])
    except Exception:
        last_page_number = 1
    pages = [f"{first_url}&page={i}" for i in range(1, last_page_number + 1)]

    return pages


def parse_listing(html: str) -> list[schemas.BookListingData]:
    tree = lh.fromstring(html)
    try:
        books = _parse_books_listing_data(tree)
    except IndexError:
        return []
    except Exception as e:
        logger.error(f"Error while parsing books listing data: {e}")
        return []
    return books


def _parse_books_listing_data(tree: lh.HtmlElement) -> list[schemas.BookListingData]:
    title_element = tree.xpath('//h3[contains(text(), "Найденные книги")]')[0]
    books_list = title_element.xpath("./following-sibling::ul[1]")[0].xpath("./li")
    parsed_books = []
    base_url = config.LIBRARY_BASE_URL.rsplit("/")[0]
    for i in books_list:
        book_data = i.xpath("./a[1]")[0]
        book_link = book_data.get("href")
        book_title = book_data.text_content()
        book_author = i.xpath("./a[2]")[0]
        book_author_url = book_author.get("href")
        book_author_name = book_author.text_content()
        book_obj = schemas.BookListingData(
            title=book_title,
            book_url=f"{base_url}{book_link}",
            author=book_author_name,
            author_url=f"{base_url}{book_author_url}",
        )
        parsed_books.append(book_obj)
    return parsed_books


def parse_book_info(html: str, book_id: str | int) -> schemas.BookInfoData:
    tree: lh.HtmlElement = lh.fromstring(html)

    # Use provided book_id or try to extract it
    try:
        book_id = int(book_id)
    except (TypeError, ValueError):
        try:
            # Try to get ID from script tag
            script_text = tree.xpath('//script[contains(text(), "var bookId")]')[
                0
            ].text_content()
            book_id = int(script_text.split("=")[1].strip())
        except Exception:
            book_id = 0

    # Extract title and author
    title = ""
    author = ""
    author_url = ""
    book_url = f"{config.LIBRARY_BASE_URL}/b/{book_id}"

    try:
        title = tree.xpath('//h1[@class="title"]/text()')[0].strip()
        # Remove "(fb2)" or similar suffix if present
        if " (" in title:
            title = title.split(" (")[0].strip()
    except Exception:
        pass

    try:
        author_element = tree.xpath('//h1[@class="title"]/following-sibling::a[1]')[0]
        author = author_element.text_content().strip()
        author_url = f"{config.LIBRARY_BASE_URL}{author_element.get('href')}"
    except Exception:
        pass

    # Extract description
    description = ""
    try:
        description_title = tree.xpath('//h2[contains(text(), "Аннотация")]')[0]
        description = description_title.xpath("./following-sibling::p[1]/text()")[0]
    except Exception:
        pass

    # Extract hashtags/genres
    hashtags = []
    try:
        genre_links = tree.xpath('//p[@class="genre"]/a')
        for genre_link in genre_links:
            genre_text = genre_link.text_content().strip()
            hashtags.append(genre_text)
    except Exception:
        pass

    # Get download links
    links_for_download = _get_download_links(tree)

    # Create and return BookInfoData
    return schemas.BookInfoData(
        id=book_id,
        title=title,
        author=author,
        author_url=author_url,
        book_url=book_url,
        description=description.strip() if description else "",
        download_urls=links_for_download,
        hashtags=hashtags if hashtags else None,
    )


def _get_download_links(tree: lh.HtmlElement) -> list[schemas.BookDownloadLinks]:
    download_links = []
