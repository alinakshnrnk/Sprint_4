from main import BooksCollector
import pytest
# класс TestBooksCollector объединяет набор тестов, которыми мы покрываем наше приложение BooksCollector
# обязательно указывать префикс Test
class TestBooksCollector:

    # пример теста:
    # обязательно указывать префикс test_
    # дальше идет название метода, который тестируем add_new_book_
    # затем, что тестируем add_two_books - добавление двух книг
    def test_add_new_book_add_two_books(self):
        # создаем экземпляр (объект) класса BooksCollector
        collector = BooksCollector()

        # добавляем две книги
        collector.add_new_book('Гордость и предубеждение и зомби')
        collector.add_new_book('Что делать, если ваш кот хочет вас убить')

        # проверяем, что добавилось именно две
        # словарь books_rating, который нам возвращает метод get_books_rating, имеет длину 2
        assert len(collector.get_books_genre()) == 2

    # напиши свои тесты ниже
    # чтобы тесты были независимыми в каждом из них создавай отдельный экземпляр класса BooksCollector()

    # проверяем, корректность работы метода установки жанра
    @pytest.mark.parametrize('book_name, genre', [('Алиса в Стране чудес', 'Фантастика'), ('Двенадцать стульев', 'Комедии')])
    def test_set_book_genre(self, book_name, genre):
        collector = BooksCollector()
        
        collector.add_new_book(book_name)
        collector.set_book_genre(book_name, genre)

        assert collector.get_books_genre().get(book_name) == genre

    # проверяем, корректность работы метода получения книг с определенным жанром
    def test_get_books_with_specific_genre(self):
        collector = BooksCollector()
        
        collector.add_new_book('Убийство в "Восточном экспрессе"')
        collector.set_book_genre('Убийство в "Восточном экспрессе"', 'Детективы')

        result = collector.get_books_with_specific_genre('Детективы')

        assert 'Убийство в "Восточном экспрессе"' in result

    # проверяем, корректность работы метода добавления новой книги при различных граничных значениях
    @pytest.mark.parametrize('book_name', ['', 'В' * 41])
    def test_add_new_book_invalid_names(self, book_name):
        collector = BooksCollector()
        
        collector.add_new_book(book_name)

        assert book_name not in collector.get_books_genre()

    @pytest.mark.parametrize('book_name', ['А', 'Б' * 40])
    def test_add_new_book_valid_names(self, book_name):
        collector = BooksCollector()
        
        collector.add_new_book(book_name)

        assert book_name in collector.get_books_genre()

    # проверяем, что книга может быть добавлена только один раз
    def test_add_book_twice(self):
        collector = BooksCollector()
        
        collector.add_new_book('Колодец и бабочка')
        collector.add_new_book('Колодец и бабочка')
        # книга должна быть в словаре только один раз
        assert list(collector.get_books_genre().keys()).count('Колодец и бабочка') == 1

    # проверяем, что книга с разрешенным жанром попадает в список для детей
    def test_get_books_for_children_with_allowed_genre(self):
        collector = BooksCollector()

        collector.add_new_book('Трое из Простоквашино')
        collector.set_book_genre('Трое из Простоквашино', 'Мультфильмы')

        result = collector.get_books_for_children()

        assert result == ['Трое из Простоквашино']

    # проверяем, что книга не попадает в список для детей, если у нее есть возрастной рейтинг
    @pytest.mark.parametrize('book_name, genre', [('Кладбище домашних животных', 'Ужасы'), ('Исчезнувшая', 'Детективы')])
    def test_books_with_age_rating_not_for_children(self, book_name, genre):
        collector = BooksCollector()

        collector.add_new_book(book_name)
        collector.set_book_genre(book_name, genre)

        children_books = collector.get_books_for_children()

        # проверяем для каждой книги из параметров
        assert book_name not in children_books

    # проверяем, что не существующая книга не добавляется в избранное
    def test_add_book_in_favorites_not_in_catalog(self):
        collector = BooksCollector()

        # добавляем несуществующую книгу в избранное
        collector.add_book_in_favorites('Хоббит')

        # список избранного должен остаться пустым
        assert collector.get_list_of_favorites_books() == []

    # проверяем, что добавление книги в избранное работает корректно
    def test_add_book_in_favorites_success(self):
        collector = BooksCollector()
        collector.add_new_book('Хоббит')

        collector.add_book_in_favorites('Хоббит')

        assert 'Хоббит' in collector.get_list_of_favorites_books()

    # проверяем, что мы не можем удалить книгу, которая не в избранном
    def test_delete_book_not_in_favorites_length(self):
        collector = BooksCollector()

        collector.add_new_book('Властилин колец: Возвращение короля')
        collector.add_book_in_favorites('Властилин колец: Возвращение короля')

        collector.delete_book_from_favorites('Властилин колец: Две крепости')

        assert len(collector.get_list_of_favorites_books()) == 1

    # проверяем, что метод delete_book_from_favorites работает корректно
    @pytest.mark.parametrize('book_name', ['Приключения Шерлока Холмса', 'Мастер и Маргарита','Дюна'])
    def test_delete_book_from_favorites(self, book_name):
        collector = BooksCollector()

        collector.add_new_book(book_name)
        collector.add_book_in_favorites(book_name)

        collector.delete_book_from_favorites(book_name)

        assert book_name not in collector.get_list_of_favorites_books()

    # проверяем, что метод get_book_genre возвращает корректный жанр
    def test_get_book_genre_returns_correct_genre(self):
        collector = BooksCollector()
        
        collector.add_new_book('Трое в лодке, не считая собаки')
        collector.set_book_genre('Трое в лодке, не считая собаки', 'Комедии')

        assert collector.get_book_genre('Трое в лодке, не считая собаки') == 'Комедии'

    # проверяем, что метод get_list_of_favorites_books возвращает список
    @pytest.mark.parametrize('book_name', ['Цветы для Элджернона', 'Мартин Иден', 'Сияние'])
    def test_get_list_of_favorites_books_returns_list(self, book_name):
        collector = BooksCollector()

        collector.add_new_book(book_name)
        collector.add_book_in_favorites(book_name)

        result = collector.get_list_of_favorites_books()

        assert result == [book_name]

    # проверяем, что метод get_books_genre возвращает словарь
    @pytest.mark.parametrize('book_name, genre', [('Стража! Стража!', 'Детективы'), ('Хроники Нарнии', 'Фантастика'), ('Мастер и Маргарита', 'Фантастика')])
    def test_get_books_genre_returns_dict(self, book_name, genre):
        collector = BooksCollector()

        collector.add_new_book(book_name)
        collector.set_book_genre(book_name, genre)

        result = collector.get_books_genre()

        assert result == {book_name: genre}