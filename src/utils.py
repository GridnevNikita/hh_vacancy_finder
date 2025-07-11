from typing import Any, Dict, List, Optional

from src.vacancies import Vacancy


def vacancies_from_json(data: List[Dict[str, Any]]) -> List[Vacancy]:
    """Преобразует список словарей в список объектов Vacancy"""
    vacancies = []
    for item in data:
        title = item["name"]
        url = item["alternate_url"]
        salary_from = None
        salary = item.get("salary")
        if salary:
            salary_from = salary["from"]

        snippet = item.get("snippet", {})
        requirement = snippet.get("requirement") or ""
        responsibility = snippet.get("responsibility") or ""
        description = (requirement + "\n" + responsibility).strip()

        vacancy = Vacancy(title, url, salary_from, description)
        vacancies.append(vacancy)
    return vacancies


def filter_vacancies(vacancies: List[Vacancy], filter_word: str) -> List[Vacancy]:
    """Фильтрует вакансии по ключевому слову в описании"""
    filtered = []
    for vacancy in vacancies:
        if filter_word.lower() in vacancy.description.lower():
            filtered.append(vacancy)
    return filtered


def get_vacancies_by_salary(
    vacancies: List[Vacancy], min_salary: Optional[int] = None, max_salary: Optional[int] = None
) -> List[Vacancy]:
    """Возвращает вакансии, зарплата которых находится в указанном диапазоне"""
    filtered = []
    for vacancy in vacancies:
        salary = vacancy.salary or 0
        if min_salary is not None and salary < min_salary:
            continue
        if max_salary is not None and salary > max_salary:
            continue
        filtered.append(vacancy)
    return filtered


def sort_vacancies(vacancies: List[Vacancy], reverse: bool = True) -> List[Vacancy]:
    """Сортирует вакансии по зарплате (по умолчанию по убыванию)"""
    return sorted(vacancies, reverse=reverse)


def get_top_vacancies(vacancies: List[Vacancy], top_n: int) -> List[Vacancy]:
    """Возвращает топ-N вакансий из списка"""
    return vacancies[:top_n]
