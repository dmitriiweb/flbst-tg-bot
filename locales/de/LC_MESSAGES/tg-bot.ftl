start-greeting = Hallo! Ich bin ein Bot zum Suchen von Büchern in der Bibliothek. Wähle eine Aktion
start-error-generic = Entschuldigung, ein Fehler ist aufgetreten. Bitte versuche es später erneut.
start-enter-title = Gib den Buchtitel ein
start-enter-author = Gib den Namen des Autors ein
start-choose-action = Wähle eine Aktion
start-search-by-title-button = 📚 Nach Titel suchen
start-search-by-author-button = 👤 Nach Autor suchen
cancel-button = ❌ Abbrechen

search-by-title-empty-query = Leere Anfrage.
search-by-title-not_-found-title = Leider wurde kein Buch gefunden.\n\nVersuche es mit einer anderen Anfrage oder klicke auf Abbrechen
search-by-title-found-books =
    { $total_books ->
        [one] Ein Buch gefunden
        [few] { $total_books } Bücher gefunden
        [many] { $total_books } Bücher gefunden
       *[other] { $total_books } Bücher gefunden
    }
search-by-title-not_-found-book-info = Leider wurden keine Informationen zu einem Buch mit dieser ID gefunden.
search-by-title-error-generic = Entschuldigung, ein Fehler ist aufgetreten. Bitte versuche es später erneut.
search-by-title-not_-found-download-link = Leider konnte kein Download-Link für das Buch abgerufen werden.
search-by-title-only-one-format = Für dieses Buch ist nur ein Format verfügbar: { $format }
search-by-title-download-started = Download gestartet...
search-by-title-download-button-with_-format = { $format } herunterladen
search-by-title-download-button = Herunterladen

search-by-author-empty-query = Leere Anfrage.
search-by-author-not_-found-author = Leider wurde kein Autor gefunden.\n\nVersuche es mit einer anderen Anfrage oder klicke auf Abbrechen
search-by-author-found-authors =
    { $total_authors ->
        [one] Ein Autor gefunden
        [few] { $total_authors } Autoren gefunden
        [many] { $total_authors } Autoren gefunden
       *[other] { $total_authors } Autoren gefunden
    }
search-by-author-not_-found-books = Leider wurde kein Buch gefunden.
search-by-author-found-books =
    { $total_books ->
        [one] Ein Buch gefunden
        [few] { $total_books } Bücher gefunden
        [many] { $total_books } Bücher gefunden
       *[other] { $total_books } Bücher gefunden
    }
search-by-author-error-generic = Entschuldigung, ein Fehler ist aufgetreten. Bitte versuche es später erneut. 