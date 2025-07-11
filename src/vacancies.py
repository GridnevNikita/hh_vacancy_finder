class Vacancy:
    """Класс для представления вакансии."""

    __slots__ = ("title", "url", "salary", "description")

    def __init__(self, title: str, url: str, salary: int, description: str) -> None:
        """Инициализация вакансии с проверкой зарплаты."""
        self.title = title
        self.url = url
        self.salary = self._validate_salary(salary)
        self.description = description

    @staticmethod
    def _validate_salary(salary: int) -> int:
        """Возвращает 0, если зарплата None или меньше 0, иначе зарплату."""
        if salary is None or salary < 0:
            return 0
        return salary

    def __lt__(self, other: object) -> bool:
        """Сравнение зарплат: меньше ли текущая зарплата."""
        if not isinstance(other, Vacancy):
            return NotImplemented
        return self.salary < other.salary

    def __eq__(self, other: object) -> bool:
        """Проверяет равенство зарплат у вакансий."""
        if not isinstance(other, Vacancy):
            return NotImplemented
        return self.salary == other.salary
