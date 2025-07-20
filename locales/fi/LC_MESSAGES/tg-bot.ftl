start-greeting = Hei! Olen botti, joka etsii kirjoja kirjastosta. Valitse toiminto
start-choose-library = Valitse kirjasto
start-choose-library-flibusta = Flibusta
start-choose-library-gutenberg = Gutenberg-projekti
start-error-generic = Pahoittelut, tapahtui virhe. Yritä myöhemmin uudelleen.
start-enter-title = Anna kirjan nimi
start-enter-author = Anna kirjailijan nimi
start-choose-action = Valitse toiminto
start-search-by-title-button = 📚 Hae nimen perusteella
start-search-by-author-button = 👤 Hae kirjailijan perusteella
cancel-button = ❌ Peruuta

search-by-title-empty-query = Tyhjä kysely.
search-by-title-not_-found-title = Valitettavasti yhtään kirjaa ei löytynyt.

Kokeile toista hakua tai paina Peruuta-painiketta
search-by-title-found-books =
    { $total_books ->
        [one] Yksi kirja löytyi
        [few] { $total_books } kirjaa löytyi
        [many] { $total_books } kirjaa löytyi
       *[other] { $total_books } kirjaa löytyi
    }
search-by-title-not_-found-book-info = Valitettavasti kirjasta tällä ID:llä ei löytynyt tietoja.
search-by-title-error-generic = Pahoittelut, tapahtui virhe. Yritä myöhemmin uudelleen.
search-by-title-not_-found-download-link = Valitettavasti latauslinkkiä ei saatu.
search-by-title-only-one-format = Tälle kirjalle on saatavilla vain yksi formaatti: { $format }
search-by-title-download-started = Lataus aloitettu...
search-by-title-download-button-with_-format = Lataa { $format }
search-by-title-download-button = Lataa

search-by-author-empty-query = Tyhjä kysely.
search-by-author-not_-found-author = Valitettavasti yhtään kirjailijaa ei löytynyt.

Kokeile toista hakua tai paina Peruuta-painiketta
search-by-author-found-authors =
    { $total_authors ->
        [one] Yksi kirjailija löytyi
        [few] { $total_authors } kirjailijaa löytyi
        [many] { $total_authors } kirjailijaa löytyi
       *[other] { $total_authors } kirjailijaa löytyi
    }
search-by-author-not_-found-books = Valitettavasti yhtään kirjaa ei löytynyt.
search-by-author-found-books =
    { $total_books ->
        [one] Yksi kirja löytyi
        [few] { $total_books } kirjaa löytyi
        [many] { $total_books } kirjaa löytyi
       *[other] { $total_books } kirjaa löytyi
    }
search-by-author-error-generic = Pahoittelut, tapahtui virhe. Yritä myöhemmin uudelleen.
gutetenberg-call-to-action = Syötä hakukysely
gutenberg-listing-previous = 👈 Edellinen
gutenberg-listing-next = 👉 Seuraava
gutenberg-listing-book-title = Hakutulokset kyselylle "{ $query }"
 