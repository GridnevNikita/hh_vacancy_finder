import pytest
from src.json_saver import JSONFileHandler


@pytest.fixture
def json_handler(tmp_path):
    # Создаём временный файл для тестов
    file = tmp_path / "test_vacancies.json"
    return JSONFileHandler(filename=str(file))


def test_load_empty_file(json_handler):
    # При отсутствии файла возвращается пустой список
    assert json_handler.load() == []


def test_add_and_load_vacancy(json_handler):
    vacancy = {
        "title": "Python Developer",
        "url": "http://example.com",
        "salary": 100000,
        "description": "Test description"
    }
    json_handler.add_vacancy(vacancy)
    data = json_handler.load()
    assert vacancy in data
    assert len(data) == 1


def test_no_duplicate_vacancies(json_handler):
    vacancy = {
        "title": "Python Developer",
        "url": "http://example.com",
        "salary": 100000,
        "description": "Test description"
    }
    json_handler.add_vacancy(vacancy)
    json_handler.add_vacancy(vacancy)
    data = json_handler.load()
    assert len(data) == 1  # Дубликаты не добавляются


def test_delete_vacancy(json_handler):
    vacancy = {
        "title": "Python Developer",
        "url": "http://example.com",
        "salary": 100000,
        "description": "Test description"
    }
    json_handler.add_vacancy(vacancy)
    json_handler.delete_vacancy(vacancy)
    data = json_handler.load()
    assert vacancy not in data
