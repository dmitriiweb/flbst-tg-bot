start-greeting = ¡Hola! Soy un bot para buscar libros en la biblioteca. Elige una acción
start-choose-library = Elige una biblioteca
start-choose-library-flibusta = Flibusta
start-choose-library-gutenberg = Proyecto Gutenberg
start-error-generic = Lo siento, ha ocurrido un error. Por favor, inténtalo de nuevo más tarde.
start-enter-title = Ingresa el título del libro
start-enter-author = Ingresa el nombre del autor
start-choose-action = Elige una acción
start-search-by-title-button = 📚 Buscar por título
start-search-by-author-button = 👤 Buscar por autor
cancel-button = ❌ Cancelar

search-by-title-empty-query = Consulta vacía.
search-by-title-not_-found-title = Lo siento, no se encontró ningún libro.

Intenta con otra consulta o pulsa el botón Cancelar
search-by-title-found-books =
    { $total_books ->
        [one] Se encontró un libro
        [few] Se encontraron { $total_books } libros
        [many] Se encontraron { $total_books } libros
       *[other] Se encontraron { $total_books } libros
    }
search-by-title-not_-found-book-info = Lo siento, no se encontró información sobre un libro con ese ID.
search-by-title-error-generic = Lo siento, ha ocurrido un error. Por favor, inténtalo de nuevo más tarde.
search-by-title-not_-found-download-link = Lo siento, no se pudo obtener el enlace de descarga del libro.
search-by-title-only-one-format = Solo hay un formato disponible para este libro: { $format }
search-by-title-download-started = Descarga iniciada...
search-by-title-download-button-with_-format = Descargar { $format }
search-by-title-download-button = Descargar

search-by-author-empty-query = Consulta vacía.
search-by-author-not_-found-author = Lo siento, no se encontró ningún autor.

Intenta con otra consulta o pulsa el botón Cancelar
search-by-author-found-authors =
    { $total_authors ->
        [one] Se encontró un autor
        [few] Se encontraron { $total_authors } autores
        [many] Se encontraron { $total_authors } autores
       *[other] Se encontraron { $total_authors } autores
    }
search-by-author-not_-found-books = Lo siento, no se encontró ningún libro.
search-by-author-found-books =
    { $total_books ->
        [one] Se encontró un libro
        [few] Se encontraron { $total_books } libros
        [many] Se encontraron { $total_books } libros
       *[other] Se encontraron { $total_books } libros
    }
search-by-author-error-generic = Lo siento, ha ocurrido un error. Por favor, inténtalo de nuevo más tarde.
gutetenberg-call-to-action = Introducir consulta de búsqueda
gutenberg-listing-previous = 👈 Anterior
gutenberg-listing-next = 👉 Siguiente
gutenberg-listing-book-title = Resultados de búsqueda para "{ $query }"
 