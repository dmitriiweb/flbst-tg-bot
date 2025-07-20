start-greeting = Ciao! Sono un bot per la ricerca di libri in biblioteca. Scegli un'azione
start-choose-library = Scegli una biblioteca
start-choose-library-flibusta = Flibusta
start-choose-library-gutenberg = Progetto Gutenberg
start-error-generic = Spiacenti, si è verificato un errore. Riprova più tardi.
start-enter-title = Inserisci il titolo del libro
start-enter-author = Inserisci il nome dell'autore
start-choose-action = Scegli un'azione
start-search-by-title-button = 📚 Cerca per titolo
start-search-by-author-button = 👤 Cerca per autore
cancel-button = ❌ Annulla

search-by-title-empty-query = Query vuota.
search-by-title-not_-found-title = Spiacenti, nessun libro trovato.

Prova una query diversa o premi Annulla
search-by-title-found-books =
    { $total_books ->
        [one] Un libro trovato
        [few] { $total_books } libri trovati
        [many] { $total_books } libri trovati
       *[other] { $total_books } libri trovati
    }
search-by-title-not_-found-book-info = Spiacenti, nessuna informazione trovata per un libro con questo ID.
search-by-title-error-generic = Spiacenti, si è verificato un errore. Riprova più tardi.
search-by-title-not_-found-download-link = Spiacenti, non è stato possibile ottenere il link per il download del libro.
search-by-title-only-one-format = È disponibile un solo formato per questo libro: { $format }
search-by-title-download-started = Download avviato...
search-by-title-download-button-with_-format = Scarica { $format }
search-by-title-download-button = Scarica

search-by-author-empty-query = Query vuota.
search-by-author-not_-found-author = Spiacenti, nessun autore trovato.

Prova una query diversa o premi Annulla
search-by-author-found-authors =
    { $total_authors ->
        [one] Un autore trovato
        [few] { $total_authors } autori trovati
        [many] { $total_authors } autori trovati
       *[other] { $total_authors } autori trovati
    }
search-by-author-not_-found-books = Spiacenti, nessun libro trovato.
search-by-author-found-books =
    { $total_books ->
        [one] Un libro trovato
        [few] { $total_books } libri trovati
        [many] { $total_books } libri trovati
       *[other] { $total_books } libri trovati
    }
search-by-author-error-generic = Spiacenti, si è verificato un errore. Riprova più tardi.
gutetenberg-call-to-action = Inserisci la query di ricerca
gutenberg-listing-previous = 👈 Precedente
gutenberg-listing-next = 👉 Successivo
gutenberg-listing-book-title = Risultati della ricerca per "{ $query }"
