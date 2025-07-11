import pytest

from src.json_saver import JsonFileSave


@pytest.fixture
def json_saver(tmp_path):
    file = tmp_path / "test_vacancies.json"
    return JsonFileSave(filename=str(file))


def test_load_empty_file(json_saver):
    assert json_saver.load_vacancy() == []


def test_add_and_load_vacancy(json_saver):
    vacancy = {
        "title": "Python Developer",
        "url": "http://example.com",
        "salary": 100000,
        "description": "Test description",
    }
    json_saver.add_vacancy(vacancy)
    data = json_saver.load_vacancy()
    assert vacancy in data
    assert len(data) == 1


def test_no_duplicate_vacancies(json_saver):
    vacancy = {
        "title": "Python Developer",
        "url": "http://example.com",
        "salary": 100000,
        "description": "Test description",
    }
    json_saver.add_vacancy(vacancy)
    json_saver.add_vacancy(vacancy)
    data = json_saver.load_vacancy()
    assert len(data) == 1


def test_delete_vacancy(json_saver):
    vacancy = {
        "title": "Python Developer",
        "url": "http://example.com",
        "salary": 100000,
        "description": "Test description",
    }
    json_saver.add_vacancy(vacancy)
    json_saver.delete_vacancy(vacancy)
    data = json_saver.load_vacancy()
    assert vacancy not in data
