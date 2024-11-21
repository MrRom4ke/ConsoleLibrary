import unittest
import os
from library import Book, load_books, save_books, generate_id

class TestLibrary(unittest.TestCase):

    def setUp(self):
        # Создаем тестовые данные
        self.test_books = [
            Book(1, "Преступление и наказание", "Фёдор Достоевский", 1866),
            Book(2, "Война и мир", "Лев Толстой", 1869)
        ]
        save_books(self.test_books)

    def tearDown(self):
        # Удаляем тестовый файл данных
        if os.path.exists('library.json'):
            os.remove('library.json')

    def test_add_book(self):
        # Проверяем добавление книги
        new_book = Book(generate_id(self.test_books), "Мастер и Маргарита", "Михаил Булгаков", 1940)
        self.test_books.append(new_book)
        save_books(self.test_books)
        books = load_books()
        self.assertEqual(len(books), 3)
        self.assertEqual(books[-1].title, "Мастер и Маргарита")

    def test_delete_book(self):
        # Проверяем удаление книги
        self.test_books.pop(0)
        save_books(self.test_books)
        books = load_books()
        self.assertEqual(len(books), 1)
        self.assertEqual(books[0].id, 2)

    def test_change_status(self):
        # Проверяем изменение статуса книги
        self.test_books[0].status = "выдана"
        save_books(self.test_books)
        books = load_books()
        self.assertEqual(books[0].status, "выдана")

    def test_generate_id(self):
        # Проверяем генерацию уникального ID
        new_id = generate_id(self.test_books)
        self.assertEqual(new_id, 3)

if __name__ == '__main__':
    unittest.main()
