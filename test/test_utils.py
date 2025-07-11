import pytest

from src.utils import filter_vacancies, get_top_vacancies, get_vacancies_by_salary, sort_vacancies, vacancies_from_json
from src.vacancies import Vacancy


@pytest.fixture
def sample_data():
    return [
        {
            "name": "Python Dev",
            "alternate_url": "link1",
            "salary": {"from": 150000},
            "snippet": {"requirement": "Опыт работы с Django", "responsibility": "Разработка веб-приложений"},
        },
        {
            "name": "Backend Dev",
            "alternate_url": "link2",
            "salary": {"from": 120000},
            "snippet": {"requirement": "Flask, FastAPI", "responsibility": "Поддержка API"},
        },
        {
            "name": "Junior Dev",
            "alternate_url": "link3",
            "salary": {"from": 80000},
            "snippet": {"requirement": "Python, обучение", "responsibility": "Выполнение задач наставника"},
        },
    ]


def test_vacancies_from_json(sample_data):
    vacancies = vacancies_from_json(sample_data)
    assert all(isinstance(vacancy, Vacancy) for vacancy in vacancies)
    assert vacancies[0].title == "Python Dev"
    assert vacancies[1].salary == 120000
    assert "Django" in vacancies[0].description
    assert "веб-приложений" in vacancies[0].description


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

    ranged_min_only = get_vacancies_by_salary(vacancies, 120000, None)
    assert all(vac.salary >= 120000 for vac in ranged_min_only)

    ranged_max_only = get_vacancies_by_salary(vacancies, None, 90000)
    assert all(vac.salary <= 90000 for vac in ranged_max_only)

    ranged_none = get_vacancies_by_salary(vacancies, None, None)
    assert len(ranged_none) == len(vacancies)


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
