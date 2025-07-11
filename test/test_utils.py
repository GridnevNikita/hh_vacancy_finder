import pytest

from src.utils import filter_vacancies, get_top_vacancies, get_vacancies_by_salary, sort_vacancies, vacancies_from_json
from src.vacancies import Vacancy


@pytest.fixture
def sample_data():
    return [
        {"title": "Python Dev", "url": "link1", "salary": 150000, "description": "Опыт работы с Django"},
        {"title": "Backend Dev", "url": "link2", "salary": 120000, "description": "Flask, FastAPI"},
        {"title": "Junior Dev", "url": "link3", "salary": 80000, "description": "Python, обучение"},
    ]


def test_vacancies_from_json(sample_data):
    vacancies = vacancies_from_json(sample_data)
    assert all(isinstance(vacancy, Vacancy) for vacancy in vacancies)
    assert vacancies[0].title == "Python Dev"
    assert vacancies[1].salary == 120000


def test_filter_vacancies(sample_data):
    vacancies = vacancies_from_json(sample_data)
    filtered = filter_vacancies(vacancies, "django")
    assert len(filtered) == 1
    assert filtered[0].title == "Python Dev"


def test_get_vacancies_by_salary(sample_data):
    vacancies = vacancies_from_json(sample_data)
    ranged = get_vacancies_by_salary(vacancies, 100000, 160000)
    assert len(ranged) == 2
    for vac in ranged:
        assert 100000 <= vac.salary <= 160000


def test_sort_vacancies(sample_data):
    vacancies = vacancies_from_json(sample_data)
    sorted_vacs = sort_vacancies(vacancies)
    assert sorted_vacs[0].salary == 150000
    assert sorted_vacs[-1].salary == 80000


def test_get_top_vacancies(sample_data):
    vacancies = vacancies_from_json(sample_data)
    top = get_top_vacancies(vacancies, 2)
    assert len(top) == 2
    assert top[0].title == "Python Dev"
