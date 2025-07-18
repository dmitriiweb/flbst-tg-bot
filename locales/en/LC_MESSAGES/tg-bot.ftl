start-greeting = Hi! I'm a bot for searching books in the library. Choose an action
start-choose-library = Choose a library
start-choose-library-flibusta = Flibusta
start-choose-library-gutenberg = Project Gutenberg
start-error-generic = Sorry, an error occurred. Please try again later.
start-enter-title = Enter the book title
start-enter-author = Enter the author's name
start-choose-action = Choose an action
start-search-by-title-button = 📚 Search by title
start-search-by-author-button = 👤 Search by author
cancel-button = ❌ Cancel

search-by-title-empty-query = Empty query.
search-by-title-not_-found-title = Sorry, no books were found.\n\nTry a different query or press Cancel
search-by-title-found-books =
    { $total_books ->
        [one] One book found
        [few] { $total_books } books found
        [many] { $total_books } books found
       *[other] { $total_books } books found
    }
search-by-title-not_-found-book-info = Sorry, no information found for a book with this ID.
search-by-title-error-generic = Sorry, an error occurred. Please try again later.
search-by-title-not_-found-download-link = Sorry, couldn't get the download link for the book.
search-by-title-only-one-format = Only one format is available for this book: { $format }
search-by-title-download-started = Download started...
search-by-title-download-button-with_-format = Download { $format }
search-by-title-download-button = Download

search-by-author-empty-query = Empty query.
search-by-author-not_-found-author = Sorry, no authors were found.\n\nTry a different query or press Cancel
search-by-author-found-authors =
    { $total_authors ->
        [one] One author found
        [few] { $total_authors } authors found
        [many] { $total_authors } authors found
       *[other] { $total_authors } authors found
    }
search-by-author-not_-found-books = Sorry, no books were found.
search-by-author-found-books =
    { $total_books ->
        [one] One book found
        [few] { $total_books } books found
        [many] { $total_books } books found
       *[other] { $total_books } books found
    }
search-by-author-error-generic = Sorry, an error occurred. Please try again later.
gutetenberg-call-to-action = Input search query