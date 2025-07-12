start-greeting = Привет! Я бот для поиска книг в библиотеке. Выберите действие
start-error-generic = Извините, произошла ошибка. Попробуйте позже.
start-enter-title = Введите название книги
start-enter-author = Введите автора книги
start-choose-action = Выберите действие
start-search-by-title-button = 📚 Поиск по названию
start-search-by-author-button = 👤 Поиск по автору
cancel-button = ❌ Отмена

search-by-title-empty-query = Пустой запрос.
search-by-title-not_-found-title = К сожалению, не удалось найти ни одной книги.\n\nПопробуйте найти книгу по другому запросу или нажмите кнопку Отмена
search-by-title-found-books =
    { $total_books ->
        [one] Найдена одна книга
        [few] Найдено { $total_books } книги
        [many] Найдено { $total_books } книг
       *[other] Найдено { $total_books } книг
    }
search-by-title-not_-found-book-info = К сожалению, не удалось найти информацию о книге с таким ID.
search-by-title-error-generic = Извините, произошла ошибка. Попробуйте позже.
search-by-title-not_-found-download-link = К сожалению, не удалось получить ссылку для скачивания книги.
search-by-title-only-one-format = Для данной книги доступен только один формат: {format}
search-by-title-download-started = Загрузка началась...

search-by-author-empty-query = Пустой запрос.
search-by-author-not_-found-author = К сожалению, не удалось найти ни одного автора.\n\nПопробуйте найти автора по другому запросу или нажмите кнопку Отмена
search-by-author-found-authors =
    { $total_authors ->
        [one] Найден один автор
        [few] Найдено { $total_authors } автора
        [many] Найдено { $total_authors } авторов
       *[other] Найдено { $total_authors } авторов
    }
search-by-author-not_-found-books = К сожалению, не удалось найти ни одной книги.
search-by-author-found-books =
    { $total_books ->
        [one] Найдена одна книга
        [few] Найдено { $total_books } книги
        [many] Найдено { $total_books } книг
       *[other] Найдено { $total_books } книг
    }
search-by-author-error-generic = Извините, произошла ошибка. Попробуйте позже.
