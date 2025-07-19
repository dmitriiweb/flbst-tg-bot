import urllib.parse

import lxml.html as lh
from loguru import logger

from flibusta_bot import config
from flibusta_bot.parsers import schemas


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
    container = tree.xpath(".//div[contains(., 'скачать')]")[0]
    links = container.xpath(".//a[starts-with(@href, '/b/')]/@href")
    target_links = [i for i in links if len(i.split("/")) == 4 and "read" not in i]
    download_links = []
    for i in target_links:
        format = i.split("/")[-1]
        download_links.append(schemas.BookDownloadLinks(url=i, format=format))
    return download_links


def parse_authors(html: str) -> list[schemas.AuthorListingData]:
    tree = lh.fromstring(html)
    try:
        ul_candidates_raw = tree.xpath(
            '//h3[contains(text(), "Найденные писатели")]/following-sibling::ul[1]'
        )
        if not isinstance(ul_candidates_raw, list):
            ul_candidates_raw = []
        authors_ul = next(
            (el for el in ul_candidates_raw if isinstance(el, lh.HtmlElement)), None
        )
        if authors_ul is None or not isinstance(authors_ul, lh.HtmlElement):
            return []
        authors_list = []
        if isinstance(authors_ul, lh.HtmlElement):
            li_candidates_raw = authors_ul.xpath("./li")
            if isinstance(li_candidates_raw, list):
                for li in li_candidates_raw:
                    if isinstance(li, lh.HtmlElement):
                        authors_list.append(li)
    except Exception as e:
        logger.error(f"Error while parsing authors listing: {e}")
        return []
    base_url = config.LIBRARY_BASE_URL.rstrip("/")
    authors = []
    for li in authors_list:
        try:
            if not isinstance(li, lh.HtmlElement):
                continue
            a_candidates_raw = li.xpath("./a") if isinstance(li, lh.HtmlElement) else []
            a_tag = next(
                (a for a in a_candidates_raw if isinstance(a, lh.HtmlElement)), None
            )
            if not a_tag:
                continue
            author_url = a_tag.get("href")
            author_name = a_tag.text_content().strip()
            authors.append(
                schemas.AuthorListingData(
                    name=author_name, author_url=f"{base_url}/{author_url}"
                )
            )
        except Exception as e:
            logger.error(f"Error parsing author li: {e}")
            continue
    return authors


def parse_listing_from_author(
    html: str, author_url: str
) -> list[schemas.BookListingData]:
    tree = lh.fromstring(html)
    base_url = config.LIBRARY_BASE_URL.rstrip("/")
    books = []
    try:
        book_links_raw = tree.xpath(
            '//a[starts-with(@href, "/b/") and not(contains(@href, "/read")) and not(contains(@href, "/fb2")) and not(contains(@href, "/epub")) and not(contains(@href, "/mobi"))]'
        )
        if not isinstance(book_links_raw, list):
            book_links_raw = []
        book_links = [a for a in book_links_raw if isinstance(a, lh.HtmlElement)]
        for a in book_links:
            book_href = a.get("href")
            title = a.text_content().strip()
            if not book_href or not book_href.startswith("/b/"):
                continue
            author = ""
            parent = a.getparent()
            while parent is not None:
                if not isinstance(parent, lh.HtmlElement):
                    break
                author_a = parent.xpath(
                    './/a[@href="{}" and contains(@class, "active")]'.format(author_url)
                )
                if author_a and isinstance(author_a[0], lh.HtmlElement):
                    author = author_a[0].text_content().strip()
                    break
                parent = parent.getparent()
            listing_data = schemas.BookListingData(
                title=title,
                book_url=f"{base_url}{book_href}",
                author=author,
                author_url=f"{base_url}{author_url}",
            )
            books.append(listing_data)
    except Exception as e:
        logger.error(f"Error parsing author book listing: {e}")
        return []
    return books
