from typing import Any, Dict, List

from src.vacancies import Vacancy


def vacancies_from_json(data: List[Dict[str, Any]]) -> List[Vacancy]:
    """Преобразует список словарей в список объектов Vacancy"""
    vacancies = []
    for i in data:
        title = i["title"]
        url = i["url"]
        salary = i["salary"]
        description = i["description"]
        vacancy = Vacancy(title, url, salary, description)
        vacancies.append(vacancy)
    return vacancies


def filter_vacancies(vacancies: List[Vacancy], filter_word: str) -> List[Vacancy]:
    """Фильтрует вакансии по ключевому слову в описании"""
    filtered = []
    for vacancy in vacancies:
        if filter_word.lower() in vacancy.description.lower():
            filtered.append(vacancy)
    return filtered


def get_vacancies_by_salary(vacancies: List[Vacancy], min_salary: int, max_salary: int) -> List[Vacancy]:
    """Возвращает вакансии, зарплата которых находится в указанном диапазоне"""
    return [vacancy for vacancy in vacancies if min_salary <= vacancy.salary <= max_salary]


def sort_vacancies(vacancies: List[Vacancy], reverse: bool = True) -> List[Vacancy]:
    """Сортирует вакансии по зарплате (по умолчанию по убыванию)"""
    return sorted(vacancies, reverse=reverse)


def get_top_vacancies(vacancies: List[Vacancy], top_n: int) -> List[Vacancy]:
    """Возвращает топ-N вакансий из списка"""
    return vacancies[:top_n]
