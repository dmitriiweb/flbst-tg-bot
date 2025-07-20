start-greeting = Hai! Saya adalah bot untuk mencari buku di perpustakaan. Pilih sebuah tindakan
start-choose-library = Pilih perpustakaan
start-choose-library-flibusta = Flibusta
start-choose-library-gutenberg = Proyek Gutenberg
start-error-generic = Maaf, terjadi kesalahan. Silakan coba lagi nanti.
start-enter-title = Masukkan judul buku
start-enter-author = Masukkan nama penulis
start-choose-action = Pilih sebuah tindakan
start-search-by-title-button = 📚 Cari berdasarkan judul
start-search-by-author-button = 👤 Cari berdasarkan penulis
cancel-button = ❌ Batal

search-by-title-empty-query = Kueri kosong.
search-by-title-not_-found-title = Maaf, tidak ada buku yang ditemukan.

Coba kueri lain atau tekan Batal
search-by-title-found-books =
    { $total_books ->
        [one] Satu buku ditemukan
        [few] { $total_books } buku ditemukan
        [many] { $total_books } buku ditemukan
       *[other] { $total_books } buku ditemukan
    }
search-by-title-not_-found-book-info = Maaf, tidak ada informasi yang ditemukan untuk buku dengan ID ini.
search-by-title-error-generic = Maaf, terjadi kesalahan. Silakan coba lagi nanti.
search-by-title-not_-found-download-link = Maaf, tidak bisa mendapatkan tautan unduhan untuk buku tersebut.
search-by-title-only-one-format = Hanya satu format yang tersedia untuk buku ini: { $format }
search-by-title-download-started = Pengunduhan dimulai...
search-by-title-download-button-with_-format = Unduh { $format }
search-by-title-download-button = Unduh

search-by-author-empty-query = Kueri kosong.
search-by-author-not_-found-author = Maaf, tidak ada penulis yang ditemukan.

Coba kueri lain atau tekan Batal
search-by-author-found-authors =
    { $total_authors ->
        [one] Satu penulis ditemukan
        [few] { $total_authors } penulis ditemukan
        [many] { $total_authors } penulis ditemukan
       *[other] { $total_authors } penulis ditemukan
    }
search-by-author-not_-found-books = Maaf, tidak ada buku yang ditemukan.
search-by-author-found-books =
    { $total_books ->
        [one] Satu buku ditemukan
        [few] { $total_books } buku ditemukan
        [many] { $total_books } buku ditemukan
       *[other] { $total_books } buku ditemukan
    }
search-by-author-error-generic = Maaf, terjadi kesalahan. Silakan coba lagi nanti.
gutetenberg-call-to-action = Masukkan kueri pencarian
gutenberg-listing-previous = 👈 Sebelumnya
gutenberg-listing-next = 👉 Berikutnya
gutenberg-listing-book-title = Hasil pencarian untuk "{ $query }"
