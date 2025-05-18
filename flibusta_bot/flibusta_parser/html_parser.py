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


def parse_listing(html: str) -> list[schemas.BookListingData] | None:
    tree = lh.fromstring(html)
    try:
        books = _parse_books_listing_data(tree)
    except Exception as e:
        logger.error(f"Error while parsing books listing data: {e}")
        return None
    return books


def _parse_books_listing_data(tree: lh.HtmlElement) -> list[schemas.BookListingData]:
    title_element = tree.xpath('//h3[contains(text(), "Найденные книги")]')[0]
    books_list = title_element.xpath("./following-sibling::ul[1]")[0].xpath("./li")
    parsed_books = []
    base_url = config.FLIBUSTA_BASE_URL.rsplit("/")[0]
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


def parse_book_info(
    html: str, book_data: schemas.BookListingData
) -> schemas.BookInfoData:
    tree: lh.HtmlElement = lh.fromstring(html)
    try:
        description_title = tree.xpath('//h2[contains(text(), "Аннотация")]')[0]
        description = description_title.xpath("./following-sibling::p[1]/text()")[0]
    except Exception as _:
        return schemas.BookInfoData(
            **book_data.to_dict(), description="", download_urls=[]
        )
    description = description or ""
    links_for_download = _get_download_links(tree)
    return schemas.BookInfoData(
        **book_data.to_dict(),
        description=description.strip(),
        download_urls=links_for_download,
    )


def _get_download_links(tree: lh.HtmlElement) -> list[schemas.BookDownloadLinks]:
    download_links = []
    target_formats: list[schemas.BookFormat] = ["epub", "fb2", "mobi"]
    for i in target_formats:
        try:
            link = tree.xpath(f'//a[contains(text(), "{i}")]/@href')[0]
        except Exception as _:
            continue
        if not link:
            continue
        url = f"{config.FLIBUSTA_BASE_URL}{link}"
        download_links.append(schemas.BookDownloadLinks(url=url, format=i))
    return download_links
