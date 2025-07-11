from src.vacancies import Vacancy


def test_salary_validation():
    v1 = Vacancy("Dev", "url1", 100, "desc")
    assert v1.salary == 100
    v2 = Vacancy("Dev", "url2", -50, "desc")
    assert v2.salary is None
    v3 = Vacancy("Dev", "url3", None, "desc")
    assert v3.salary is None


def test_comparison_lt():
    v1 = Vacancy("Dev", "url1", 100, "desc")
    v2 = Vacancy("Dev", "url2", 200, "desc")
    v3 = Vacancy("Dev", "url3", None, "desc")
    v4 = Vacancy("Dev", "url4", None, "desc")

    assert v1 < v2
    assert not (v2 < v1)
    assert v3 < v1
    assert not (v1 < v3)
    assert not (v3 < v4)
    assert not (v4 < v3)
    assert (v1.__lt__("not a vacancy")) is NotImplemented


def test_comparison_eq():
    v1 = Vacancy("Dev", "url1", 150, "desc")
    v2 = Vacancy("Dev", "url2", 150, "desc")
    v3 = Vacancy("Dev", "url3", 100, "desc")
    v4 = Vacancy("Dev", "url4", None, "desc")
    v5 = Vacancy("Dev", "url5", None, "desc")

    assert v1 == v2
    assert v1 != v3
    assert v4 == v5
    assert (v1 == "not a vacancy") is False
