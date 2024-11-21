import json
import os
from typing import List, Dict

DATA_FILE = 'library.json'


class Book:
    """
    Класс представляет книгу в библиотеке.

    Атрибуты:
        book_id (int): Уникальный идентификатор книги.
        title (str): Название книги.
        author (str): Автор книги.
        year (int): Год издания книги.
        status (str): Статус книги ("в наличии" или "выдана").
    """

    def __init__(self, book_id: int, title: str, author: str, year: int, status: str = "в наличии"):
        self.id = book_id
        self.title = title
        self.author = author
        self.year = year
        self.status = status

    def to_dict(self) -> Dict:
        """Преобразует объект книги в словарь."""
        return {
            "id": self.id,
            "title": self.title,
            "author": self.author,
            "year": self.year,
            "status": self.status
        }


def load_books() -> List[Book]:
    """Загружает список книг из файла."""
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return [
        Book(
            book_id=item.get('id'),
            title=item.get('title'),
            author=item.get('author'),
            year=item.get('year'),
            status=item.get('status', 'в наличии')
        )
        for item in data
    ]


def save_books(books: List[Book]) -> None:
    """Сохраняет список книг в файл."""
    with open(DATA_FILE, 'w', encoding='utf-8') as file:
        json.dump([book.to_dict() for book in books], file, ensure_ascii=False, indent=4)


def generate_id(books: List[Book]) -> int:
    """Генерирует уникальный идентификатор для новой книги."""
    return max((book.id for book in books), default=0) + 1


def add_book(books: List[Book]) -> None:
    """Добавляет новую книгу в библиотеку."""
    title = input("Введите название книги: ")
    author = input("Введите автора книги: ")
    try:
        year = int(input("Введите год издания книги: "))
    except ValueError:
        print("Год должен быть числом.")
        return
    book_id = generate_id(books)
    new_book = Book(book_id, title, author, year)
    books.append(new_book)
    save_books(books)
    print(f"Книга с id {book_id} добавлена.")


def delete_book(books: List[Book]) -> None:
    """Удаляет книгу из библиотеки по id."""
    try:
        book_id = int(input("Введите id книги для удаления: "))
    except ValueError:
        print("ID должен быть числом.")
        return
    for book in books:
        if book.id == book_id:
            books.remove(book)
            save_books(books)
            print(f"Книга с id {book_id} удалена.")
            return
    print("Книга с таким id не найдена.")


def search_books(books: List[Book]) -> None:
    """Ищет книги по заданному параметру."""
    print("Выберите параметр поиска:")
    print("1. Название")
    print("2. Автор")
    print("3. Год издания")
    choice = input("Введите номер параметра: ")
    if choice == '1':
        query = input("Введите название книги: ").lower()
        results = [book for book in books if query in book.title.lower()]
    elif choice == '2':
        query = input("Введите автора книги: ").lower()
        results = [book for book in books if query in book.author.lower()]
    elif choice == '3':
        try:
            year = int(input("Введите год издания книги: "))
        except ValueError:
            print("Год должен быть числом.")
            return
        results = [book for book in books if book.year == year]
    else:
        print("Неверный выбор.")
        return

    if results:
        print("Найденные книги:")
        for book in results:
            print(f"ID: {book.id}, Название: {book.title}, Автор: {book.author}, "
                  f"Год: {book.year}, Статус: {book.status}")
    else:
        print("Книги не найдены.")


def display_books(books: List[Book]) -> None:
    """Отображает все книги в библиотеке."""
    if not books:
        print("Библиотека пуста.")
        return
    print("Список всех книг:")
    for book in books:
        print(f"ID: {book.id}, Название: {book.title}, Автор: {book.author}, "
              f"Год: {book.year}, Статус: {book.status}")


def change_status(books: List[Book]) -> None:
    """Изменяет статус книги по id."""
    try:
        book_id = int(input("Введите id книги для изменения статуса: "))
    except ValueError:
        print("ID должен быть числом.")
        return
    for book in books:
        if book.id == book_id:
            new_status = input("Введите новый статус ('в наличии' или 'выдана'): ")
            if new_status in ["в наличии", "выдана"]:
                book.status = new_status
                save_books(books)
                print(f"Статус книги с id {book_id} изменен на '{new_status}'.")
                return
            else:
                print("Некорректный статус.")
                return
    print("Книга с таким id не найдена.")


def main_menu() -> None:
    """Основное меню приложения."""
    books = load_books()
    while True:
        print("\nУправление библиотекой:")
        print("1. Добавить книгу")
        print("2. Удалить книгу")
        print("3. Поиск книги")
        print("4. Отобразить все книги")
        print("5. Изменить статус книги")
        print("6. Выход")
        choice = input("Выберите действие: ")
        if choice == '1':
            add_book(books)
        elif choice == '2':
            delete_book(books)
        elif choice == '3':
            search_books(books)
        elif choice == '4':
            display_books(books)
        elif choice == '5':
            change_status(books)
        elif choice == '6':
            print("Выход из программы.")
            break
        else:
            print("Неверный выбор. Попробуйте снова.")


if __name__ == "__main__":
    main_menu()
