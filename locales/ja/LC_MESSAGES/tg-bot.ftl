start-greeting = こんにちは！図書館で本を検索するためのボットです。アクションを選択してください
start-error-generic = 申し訳ありませんが、エラーが発生しました。後でもう一度お試しください。
start-enter-title = 書名を入力してください
start-enter-author = 著者名を入力してください
start-choose-action = アクションを選択してください
start-search-by-title-button = 📚 書名で検索
start-search-by-author-button = 👤 著者で検索
cancel-button = ❌ キャンセル

search-by-title-empty-query = クエリが空です。
search-by-title-not_-found-title = 申し訳ありませんが、本が見つかりませんでした。

別のクエリを試すか、キャンセルを押してください
search-by-title-found-books =
    { $total_books ->
        [one] 1冊の本が見つかりました
        [few] { $total_books } 冊の本が見つかりました
        [many] { $total_books } 冊の本が見つかりました
       *[other] { $total_books } 冊の本が見つかりました
    }
search-by-title-not_-found-book-info = 申し訳ありませんが、このIDの本の情報は見つかりませんでした。
search-by-title-error-generic = 申し訳ありませんが、エラーが発生しました。後でもう一度お試しください。
search-by-title-not_-found-download-link = 申し訳ありませんが、本のダウンロードリンクを取得できませんでした。
search-by-title-only-one-format = この本で利用できる形式は1つだけです: { $format }
search-by-title-download-started = ダウンロードが開始されました...
search-by-title-download-button-with_-format = { $format } をダウンロード
search-by-title-download-button = ダウンロード

search-by-author-empty-query = クエリが空です。
search-by-author-not_-found-author = 申し訳ありませんが、著者が見つかりませんでした。

別のクエリを試すか、キャンセルを押してください
search-by-author-found-authors =
    { $total_authors ->
        [one] 1人の著者が見つかりました
        [few] { $total_authors } 人の著者が見つかりました
        [many] { $total_authors } 人の著者が見つかりました
       *[other] { $total_authors } 人の著者が見つかりました
    }
search-by-author-not_-found-books = 申し訳ありませんが、本が見つかりませんでした。
search-by-author-found-books =
    { $total_books ->
        [one] 1冊の本が見つかりました
        [few] { $total_books } 冊の本が見つかりました
        [many] { $total_books } 冊の本が見つかりました
       *[other] { $total_books } 冊の本が見つかりました
    }
search-by-author-error-generic = 申し訳ありませんが、エラーが発生しました。後でもう一度お試しください。