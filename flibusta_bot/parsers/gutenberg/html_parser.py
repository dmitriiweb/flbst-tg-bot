import lxml.html as lxml

from . import schemas


def parse_books(html: str) -> list[schemas.BookListingData]:
    tree = lxml.fromstring(html)
    books = tree.xpath("//li[@class='booklink']")  # type: ignore
    result = []

    for book in books:  # type: ignore
        # Get the link element
        links = book.xpath(".//a[@class='link']")  # type: ignore
        if not links:
            continue

        link = links[0]  # type: ignore
        url = link.get("href", "")  # type: ignore

        # Convert relative URL to full URL
        if url.startswith("/"):
            url = f"https://www.gutenberg.org{url}"

        # Get the title
        titles = book.xpath(".//span[@class='title']")  # type: ignore
        if not titles:
            continue

        title_elem = titles[0]  # type: ignore
        title = title_elem.text_content().strip()  # type: ignore

        # Get the author (subtitle)
        subtitles = book.xpath(".//span[@class='subtitle']")  # type: ignore
        author = ""
        if subtitles:
            author = subtitles[0].text_content().strip()  # type: ignore

        result.append(schemas.BookListingData(title=title, author=author, url=url))

    return result


def get_next_page_url(html: str) -> str | None:
    tree = lxml.fromstring(html)
    next_links = tree.xpath("//a[text()='Next']")  # type: ignore

    if next_links:
        url = next_links[0].get("href")  # type: ignore
        # Convert relative URL to full URL
        if url and url.startswith("/"):
            url = f"https://www.gutenberg.org{url}"
        return url

    return None


def get_prev_page_url(html: str) -> str | None:
    tree = lxml.fromstring(html)
    prev_links = tree.xpath("//a[text()='Previous']")  # type: ignore

    if prev_links:
        url = prev_links[0].get("href")  # type: ignore
        # Convert relative URL to full URL
        if url and url.startswith("/"):
            url = f"https://www.gutenberg.org{url}"
        return url

    return None


def parse_book_info(html: str) -> schemas.BookInfoData | None:
    tree = lxml.fromstring(html)

    # Get title from h1 and extract just the title part (before " by ")
    title_elements = tree.xpath("//h1[@id='book_title']")  # type: ignore
    if not title_elements:
        return None

    full_title = title_elements[0].text_content().strip()  # type: ignore
    # Extract just the title part before " by "
    title = full_title.split(" by ")[0] if " by " in full_title else full_title

    # Get author from breadcrumb which has cleaner format
    author_elements = tree.xpath(
        "//div[@class='breadcrumbs']//a[contains(@href, '/ebooks/author/')]"
    )  # type: ignore
    author = ""
    if author_elements:
        author_text = author_elements[0].text_content().strip()  # type: ignore
        # Extract author from "99 by graf Leo Tolstoy" format
        if " by " in author_text:
            author = author_text.split(" by ")[1]
        else:
            author = author_text
    else:
        # Fallback to bibliographic table
        author_elements = tree.xpath(
            "//table[@id='about_book_table']//tr[th[text()='Author']]/td"
        )  # type: ignore
        if author_elements:
            author_text = author_elements[0].text_content().strip()  # type: ignore
            # Format "Tolstoy, Leo, graf, 1828-1910" to "graf Leo Tolstoy"
            if "," in author_text:
                parts = [part.strip() for part in author_text.split(",")]
                if len(parts) >= 3 and "graf" in parts[2]:
                    author = f"graf {parts[1]} {parts[0]}"
                else:
                    author = f"{parts[1]} {parts[0]}"
            else:
                author = author_text

    # Get description from summary text container
    description_elements = tree.xpath(
        "//div[@class='summary-text-container']//text()[normalize-space()]"
    )  # type: ignore
    description = ""
    if description_elements:
        # Get the first non-empty text content
        for elem in description_elements:  # type: ignore
            if isinstance(elem, str):
                text = elem.strip()
                if (
                    text
                    and not text.startswith("...")
                    and not text.startswith("Read More")
                    and not text.startswith("Show Less")
                ):
                    description = text
                    break

    # Get current URL (we'll need to pass this as parameter or extract from page)
    # For now, we'll construct it from the book ID in the page
    book_id_elements = tree.xpath(
        "//table[@id='about_book_table']//tr[th[text()='EBook-No.']]/td"
    )  # type: ignore
    book_id = ""
    if book_id_elements:
        book_id = book_id_elements[0].text_content().strip()  # type: ignore
    url = f"https://www.gutenberg.org/ebooks/{book_id}" if book_id else ""

    # Get download URLs from the download table
    download_urls = []
    download_rows = tree.xpath("//table[@id='download_options_table']//tr[td[2]/a]")  # type: ignore

    for row in download_rows:  # type: ignore
        # Get the format title
        title_elem = row.xpath(".//td[2]/a")  # type: ignore
        if not title_elem:
            continue

        format_title = title_elem[0].text_content().strip()  # type: ignore

        # Skip "Read now!" format
        if format_title == "Read now!" or "audio" in format_title.lower():
            continue

        # Get the download URL
        download_url = title_elem[0].get("href", "")  # type: ignore
        if download_url.startswith("/"):
            download_url = f"https://www.gutenberg.org{download_url}"

        download_urls.append(
            schemas.DownloadUrlData(title=format_title, url=download_url)
        )

    return schemas.BookInfoData(
        title=title,
        author=author,
        url=url,
        description=description,
        download_urls=download_urls,
    )
