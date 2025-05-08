import pytest

from main import BooksCollector

class TestBooksCollector:


    def test_add_new_book_adding_four_books_success(self, collection):
        books = ['Война и мир', 'Мастер и Маргарита', 'Радикальное прощение', 'Гарри Потер']
        for book in books:
            collection.add_new_book(book)
        assert len(collection.get_books_genre()) == 4


    def test_add_new_book_check_genre_success(self, collection):
        first_book = 'Ромео и Джульетта'
        collection.add_new_book(first_book)
        assert collection.get_book_genre(first_book) == ''

    @pytest.mark.parametrize('book',
                             ['', 'Радикальное прощение Радикальное прощение Радикальное прощение']
                             )
    def test_add_new_book_add_incorrect_name_not_added(self, book, collection):
        collection.add_new_book(book)
        assert len(collection.get_books_genre()) == 0


    def test_add_new_book_add_double_books_not_added(self, collection):
        books = ['Война и мир', 'Война и мир']
        for book in books:
            collection.add_new_book(book)
        assert len(collection.get_books_genre()) == 1


    def test_set_book_genre_added(self, collection):
        first_book = 'Властелин колец'
        genre = 'Фантастика'
        collection.add_new_book(first_book)
        collection.set_book_genre(first_book, genre)
        assert collection.get_book_genre(first_book) == genre


    def test_set_book_genre_changed(self, collection):
        first_book = 'Властелин колец'
        genre = 'Фантастика'
        other_genre = 'Детективы'
        collection.add_new_book(first_book)
        collection.set_book_genre(first_book, genre)
        collection.set_book_genre(first_book, other_genre)
        assert collection.get_book_genre(first_book) == other_genre


    def test_set_book_genre_missing_genre_not_added(self, collection):
        first_book = 'Властелин колец'
        missing_genre = 'Приключения'
        collection.add_new_book(first_book)
        collection.set_book_genre(first_book, missing_genre)
        assert collection.get_book_genre(first_book) == ''


    def test_get_books_with_specific_genre_success(self, collection_five_books):
        assert collection_five_books.get_books_with_specific_genre('Ужасы') == ['Чужой']


    def test_get_books_with_specific_genre_missing_book(self, collection_five_books):
        assert len(collection_five_books.get_books_with_specific_genre('Приключения')) == 0


    def test_get_books_for_children_success(self, collection_five_books):
        children_books = collection_five_books.get_books_for_children()
        assert len(children_books) == 3 and children_books == ['Властелин колец', 'Король лев', 'Сон в летнюю ночь']


    def test_add_book_in_favorites_add_one_book_added(self, collection):
        first_book = 'Хоббит'
        collection.add_new_book(first_book)
        collection.add_book_in_favorites(first_book)
        favorites = collection.get_list_of_favorites_books()
        assert len(favorites) == 1 and favorites[0] == first_book


    def test_add_book_in_favorites_add_missing_book_not_added(self, collection):
        first_book = 'Властелин колец'
        collection.add_book_in_favorites(first_book)
        assert len(collection.get_list_of_favorites_books()) == 0


    def test_add_book_in_favorites_add_double_books_not_added(self, collection):
        first_book = 'Властелин колец'
        collection.add_new_book(first_book)
        collection.add_book_in_favorites(first_book)
        collection.add_book_in_favorites(first_book)
        favorites = collection.get_list_of_favorites_books()
        assert len(favorites) == 1 and favorites[0] == first_book


    def test_delete_book_from_favorites_book_deleted(self, collection):
        first_book = 'Властелин колец'
        collection.add_new_book(first_book)
        collection.add_book_in_favorites(first_book)
        collection.delete_book_from_favorites(first_book)
        assert len(collection.get_list_of_favorites_books()) == 0


    def test_delete_book_from_favorites_missing_book_not_deleted(self, collection):
        first_book = 'Хоббит'
        second_book = 'Властелин колец'
        collection.add_new_book(first_book)
        collection.add_book_in_favorites(first_book)
        collection.delete_book_from_favorites(second_book)
        favorites = collection.get_list_of_favorites_books()
        assert len(favorites) == 1 and favorites[0] == first_book


@pytest.mark.parametrize("name, genre, expected_genre", [
    ("Название книги", "Фантастика", "Фантастика"),
    ("Другая книга", "Ужасы", "Ужасы"),
    ("Книга без жанра", "", ""),
    ("Название книги", "12345678901234567890123456789012345678901", ""), # Проверяем длинный жанр
])
def test_get_book_genre(collector, name, genre, expected_genre):
    collector.add_new_book(name)
    if genre:
        collector.set_book_genre(name, genre)
    assert collector.get_book_genre(name) == expected_genre

def test_get_book_genre_non_existing(collector):
    assert collector.get_book_genre("Несуществующая книга") is None

    @pytest.mark.parametrize("genre, expected", [("Фантастика", ["Название книги"]), ("Ужасы", [])])
    def test_get_books_genre(self, genre, expected):
        collector = BooksCollector()
        collector.add_new_book("Название книги")
        collector.set_book_genre("Название книги", "Фантастика")
        assert collector.get_books_genre(genre) == expected

    def test_get_books_genre(self):
        collector = BooksCollector()
        collector.add_new_book("Книга 1")
        collector.add_new_book("Книга 2")
        collector.set_book_genre("Книга 1", "Фантастика")
        assert collector.get_books_genre() == {"Книга 1": "Фантастика", "Книга 2": ""}


    def test_get_list_of_favorites_books(self):
        collector = BooksCollector()
        collector.add_new_book("Книга 1")
        collector.add_new_book("Книга 2")
        collector.add_book_in_favorites("Книга 1")
        assert collector.get_list_of_favorites_books() == ["Книга 1"]