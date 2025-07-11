import json
import os
from abc import ABC, abstractmethod
from typing import Any, Dict, List, cast


class AbstractFileSave(ABC):
    """Абстрактный класс для работы с файлами хранения вакансий."""

    @abstractmethod
    def load_vacancy(self) -> List[Dict[str, Any]]:
        """Получение данных из файла."""
        pass

    @abstractmethod
    def add_vacancy(self, vacancy: Dict[str, Any]) -> None:
        """Добавление вакансии в файл."""
        pass

    @abstractmethod
    def delete_vacancy(self, vacancy: Dict[str, Any]) -> None:
        """Удаление одной вакансии из файла."""
        pass


class JsonFileSave(AbstractFileSave):
    """Класс для работы с JSON-файлом хранения вакансий."""

    def __init__(self, filename: str = "vacancies.json") -> None:
        """Инициализация с указанием имени файла."""
        self.__filename = filename

    def load_vacancy(self) -> List[Dict[str, Any]]:
        """Загрузка всех вакансий из файла."""
        if not os.path.exists(self.__filename):
            return []
        with open(self.__filename, "r", encoding="utf-8") as file:
            data = json.load(file)
            return cast(List[Dict[str, Any]], data)

    def add_vacancy(self, vacancy: Dict[str, Any]) -> None:
        """Добавление вакансии в файл без дублирования."""
        data = self.load_vacancy()
        if vacancy not in data:
            data.append(vacancy)
            self.save(data)

    def delete_vacancy(self, vacancy: Dict[str, Any]) -> None:
        """Удаление вакансии из файла."""
        data = self.load_vacancy()
        if vacancy in data:
            data.remove(vacancy)
            self.save(data)

    def save(self, data: List[Dict[str, Any]]) -> None:
        """Сохранение данных в файл."""
        with open(self.__filename, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
