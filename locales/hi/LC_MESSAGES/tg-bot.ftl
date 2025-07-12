start-greeting = नमस्ते! मैं पुस्तकालय में किताबें खोजने के लिए एक बॉट हूँ। एक क्रिया चुनें
start-error-generic = क्षमा करें, एक त्रुटि हुई। कृपया बाद में पुन: प्रयास करें।
start-enter-title = पुस्तक का शीर्षक दर्ज करें
start-enter-author = लेखक का नाम दर्ज करें
start-choose-action = एक क्रिया चुनें
start-search-by-title-button = 📚 शीर्षक से खोजें
start-search-by-author-button = 👤 लेखक द्वारा खोजें
cancel-button = ❌ रद्द करें

search-by-title-empty-query = खाली प्रश्न।
search-by-title-not_-found-title = क्षमा करें, कोई किताब नहीं मिली।

एक अलग प्रश्न का प्रयास करें या रद्द करें दबाएं
search-by-title-found-books =
    { $total_books ->
        [one] एक किताब मिली
        [few] { $total_books } किताबें मिलीं
        [many] { $total_books } किताबें मिलीं
       *[other] { $total_books } किताबें मिलीं
    }
search-by-title-not_-found-book-info = क्षमा करें, इस आईडी वाली पुस्तक के लिए कोई जानकारी नहीं मिली।
search-by-title-error-generic = क्षमा करें, एक त्रुटि हुई। कृपया बाद में पुन: प्रयास करें।
search-by-title-not_-found-download-link = क्षमा करें, पुस्तक के लिए डाउनलोड लिंक नहीं मिल सका।
search-by-title-only-one-format = इस पुस्तक के लिए केवल एक प्रारूप उपलब्ध है: {format}
search-by-title-download-started = डाउनलोड शुरू हो गया है...

search-by-author-empty-query = खाली प्रश्न।
search-by-author-not_-found-author = क्षमा करें, कोई लेखक नहीं मिला।

एक अलग प्रश्न का प्रयास करें या रद्द करें दबाएं
search-by-author-found-authors =
    { $total_authors ->
        [one] एक लेखक मिला
        [few] { $total_authors } लेखक मिले
        [many] { $total_authors } लेखक मिले
       *[other] { $total_authors } लेखक मिले
    }
search-by-author-not_-found-books = क्षमा करें, कोई किताब नहीं मिली।
search-by-author-found-books =
    { $total_books ->
        [one] एक किताब मिली
        [few] { $total_books } किताबें मिलीं
        [many] { $total_books } किताबें मिलीं
       *[other] { $total_books } किताबें मिलीं
    }
search-by-author-error-generic = क्षमा करें, एक त्रुटि हुई। कृपया बाद में पुन: प्रयास करें।