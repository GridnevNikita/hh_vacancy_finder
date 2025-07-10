from src.models import Vacancy


def test_salary_validation():
    v1 = Vacancy("Dev", "url1", 100, "desc")
    assert v1.salary == 100

    v2 = Vacancy("Dev", "url2", -50, "desc")
    assert v2.salary == 0

    v3 = Vacancy("Dev", "url3", None, "desc")
    assert v3.salary == 0


def test_comparison_lt():
    v1 = Vacancy("Dev", "url1", 100, "desc")
    v2 = Vacancy("Dev", "url2", 200, "desc")
    assert v1 < v2
    assert not (v2 < v1)


def test_comparison_eq():
    v1 = Vacancy("Dev", "url1", 150, "desc")
    v2 = Vacancy("Dev", "url2", 150, "desc")
    v3 = Vacancy("Dev", "url3", 100, "desc")
    assert v1 == v2
    assert v1 != v3
    assert (v1 == "not a vacancy") is False
