start-greeting = Salut ! Je suis un bot pour rechercher des livres dans la bibliothèque. Choisissez une action
start-choose-library = Choisissez une bibliothèque
start-choose-library-flibusta = Flibusta
start-choose-library-gutenberg = Projet Gutenberg
start-error-generic = Désolé, une erreur est survenue. Veuillez réessayer plus tard.
start-enter-title = Entrez le titre du livre
start-enter-author = Entrez le nom de l'auteur
start-choose-action = Choisissez une action
start-search-by-title-button = 📚 Rechercher par titre
start-search-by-author-button = 👤 Rechercher par auteur
cancel-button = ❌ Annuler

search-by-title-empty-query = Requête vide.
search-by-title-not_-found-title = Désolé, aucun livre n'a été trouvé.

Essayez une autre requête ou appuyez sur Annuler
search-by-title-found-books =
    { $total_books ->
        [one] Un livre trouvé
        [few] { $total_books } livres trouvés
        [many] { $total_books } livres trouvés
       *[other] { $total_books } livres trouvés
    }
search-by-title-not_-found-book-info = Désolé, aucune information trouvée pour un livre avec cet ID.
search-by-title-error-generic = Désolé, une erreur est survenue. Veuillez réessayer plus tard.
search-by-title-not_-found-download-link = Désolé, impossible d'obtenir le lien de téléchargement du livre.
search-by-title-only-one-format = Un seul format disponible pour ce livre : { $format }
search-by-title-download-started = Le téléchargement a commencé...
search-by-title-download-button-with_-format = Télécharger { $format }
search-by-title-download-button = Télécharger

search-by-author-empty-query = Requête vide.
search-by-author-not_-found-author = Désolé, aucun auteur n'a été trouvé.

Essayez une autre requête ou appuyez sur Annuler
search-by-author-found-authors =
    { $total_authors ->
        [one] Un auteur trouvé
        [few] { $total_authors } auteurs trouvés
        [many] { $total_authors } auteurs trouvés
       *[other] { $total_authors } auteurs trouvés
    }
search-by-author-not_-found-books = Désolé, aucun livre n'a été trouvé.
search-by-author-found-books =
    { $total_books ->
        [one] Un livre trouvé
        [few] { $total_books } livres trouvés
        [many] { $total_books } livres trouvés
       *[other] { $total_books } livres trouvés
    }
search-by-author-error-generic = Désolé, une erreur est survenue. Veuillez réessayer plus tard.
gutetenberg-call-to-action = Saisir la requête de recherche
gutenberg-listing-previous = 👈 Précédent
gutenberg-listing-next = 👉 Suivant
gutenberg-listing-book-title = Résultats de recherche pour "{ $query }"
