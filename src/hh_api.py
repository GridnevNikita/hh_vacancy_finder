from abc import ABC, abstractmethod
from typing import Any, Dict, List, cast

import requests


class AbstractAPI(ABC):
    """
    Абстрактный класс для работы с API платформ вакансий.
    Обязывает реализовать методы подключения и получения вакансий.
    """

    @abstractmethod
    def _connect(self) -> None:
        """Метод подключения к API"""
        pass

    @abstractmethod
    def get_vacancies(self, keyword: str) -> List[Dict]:
        """Получение вакансий по ключевому слову"""
        pass


class HeadHunterAPI(AbstractAPI):
    """
    Класс для работы с API hh.ru.
    Реализует методы подключения и получения вакансий.
    """

    def __init__(self, base_url: str = "https://api.hh.ru/vacancies"):
        self.__base_url = base_url

    def _connect(self) -> None:
        """Метод подключения к API"""
        response = requests.get(self.__base_url)
        response.raise_for_status()

    def get_vacancies(self, keyword: str, per_page: int = 20) -> List[Dict[str, Any]]:
        """Получение вакансий по ключевому слову"""
        self._connect()
        params: dict[str, str | int] = {"text": keyword, "per_page": per_page, "area": 113}
        response = requests.get(self.__base_url, params=params)
        response.raise_for_status()
        data = response.json()
        return cast(List[Dict[str, Any]], data.get("items", []))
