import os

from src.hh_api import HeadHunterAPI
from src.json_saver import JsonFileSave
from src.utils import filter_vacancies, get_top_vacancies, get_vacancies_by_salary, sort_vacancies, vacancies_from_json


def user_interaction() -> None:
    """
    Основная функция взаимодействия с пользователем.
    Позволяет искать, фильтровать, сортировать и сохранять вакансии.
    """

    keyword = input("Введите поисковый запрос (или 'выход' для завершения): ").strip()
    if not keyword or keyword.lower() == "выход":
        print("Выход из программы.")
        return

    while True:
        count_input = input("Сколько вакансий вы хотите получить? (Оставьте пустым для 20): ").strip()
        if not count_input:
            per_page = 20
            break
        if count_input.isdigit() and int(count_input) > 0:
            per_page = int(count_input)
            if per_page > 100:
                print("Максимум можно получить 100 вакансий за один запрос. Использую 100.")
                per_page = 100
            break
        print("Пожалуйста, введите положительное число или оставьте пустым.")

    hh_api = HeadHunterAPI()
    vacancies_data = hh_api.get_vacancies(keyword, per_page=per_page)

    if not vacancies_data:
        print("Вакансий по вашему запросу не найдено.")
        return

    print(f"Найдено {len(vacancies_data)} вакансий.")
    vacancies = vacancies_from_json(vacancies_data)

    # Фильтрация по ключевому слову
    while True:
        filter_answer = input("Хотите фильтровать вакансии по ключевому слову в описании? (да/нет): ").strip().lower()
        if filter_answer == "да":
            keyword_filter = (
                input("Введите ключевое слово для фильтрации (или напишите 'выход' для пропуска): ").strip().lower()
            )
            if keyword_filter != "выход":
                vacancies = filter_vacancies(vacancies, keyword_filter)
                print(f"После фильтрации осталось {len(vacancies)} вакансий.")
                if not vacancies:
                    print("Вакансий не найдено после фильтрации.")
                    return
            break
        elif filter_answer == "нет":
            break
        else:
            print("Некорректный ввод. Пожалуйста, введите 'да' или 'нет'.")

    # Фильтрация по зарплате
    salary_answer = input("Хотите фильтровать вакансии по зарплате? (да/нет): ").strip().lower()
    if salary_answer == "да":
        min_salary = None
        while True:
            min_salary_input = (
                input("Введите минимальную зарплату (или напишите 'выход' для пропуска): ").strip().lower()
            )
            if min_salary_input == "выход":
                break
            try:
                min_salary = int(min_salary_input)
                break
            except ValueError:
                print("Некорректный ввод. Пожалуйста, введите число или 'выход'.")

        max_salary = None
        while True:
            max_salary_input = (
                input("Введите максимальную зарплату (или напишите 'выход' для пропуска): ").strip().lower()
            )
            if max_salary_input == "выход":
                break
            try:
                max_salary = int(max_salary_input)
                break
            except ValueError:
                print("Некорректный ввод. Пожалуйста, введите число или 'выход'.")

        vacancies = get_vacancies_by_salary(vacancies, min_salary, max_salary)
        print(f"После фильтрации по зарплате осталось {len(vacancies)} вакансий.")
        if not vacancies:
            print("Вакансий не найдено после фильтрации по зарплате.")
            return

    # Сортировка вакансий
    sort_answer = input("Хотите отсортировать вакансии по зарплате? (да/нет): ").strip().lower()
    if sort_answer == "да":
        while True:
            order_answer = input("Желаете отсортировать вакансии по убыванию зарплаты? (да/нет): ").strip().lower()
            if order_answer == "да":
                vacancies = sort_vacancies(vacancies, reverse=True)
                print("Вакансии отсортированы по убыванию зарплаты.")
                break
            elif order_answer == "нет":
                vacancies = sort_vacancies(vacancies, reverse=False)
                print("Вакансии отсортированы по возрастанию зарплаты.")
                break
            else:
                print("Некорректный ввод. Пожалуйста, введите 'да' или 'нет'.")

    # Выбор количества вакансий для показа
    while True:
        try:
            top_n_input = input(f"Сколько вакансий показать? (Максимум {len(vacancies)}): ").strip()
            top_n = int(top_n_input)
            if top_n <= 0:
                print("Введите положительное число.")
                continue
            if top_n > len(vacancies):
                print(f"Всего найдено {len(vacancies)} вакансий, покажу все.")
                top_n = len(vacancies)
            vacancies = get_top_vacancies(vacancies, top_n)
            break
        except ValueError:
            print("Некорректный ввод. Пожалуйста, введите число.")

    print(f"Готовлю для вас {len(vacancies)} вакансий...")

    # Вывод вакансий на экран
    while True:
        show_answer = input("Хотели бы вы просмотреть вакансии прямо сейчас? (да/нет): ").strip().lower()
        if show_answer in ("да", "нет"):
            break
        else:
            print("Пожалуйста, введите 'да' или 'нет'.")

    if show_answer == "да":
        for vacancy in vacancies:
            print(f"{vacancy.title} | Зарплата: {vacancy.salary or 'не указана'} | Ссылка: {vacancy.url}")

    # Сохранение в файл
    while True:
        save_answer = (
            input("Желаете ли вы сохранить вакансии в файл для дальнейшего просмотра? (да/нет): ").strip().lower()
        )
        if save_answer in ("да", "нет"):
            break
        else:
            print("Пожалуйста, введите 'да' или 'нет'.")

    if save_answer == "да":
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        file_path = os.path.join(base_dir, "data", "vacancies.json")

        json_saver = JsonFileSave(file_path)
        data_to_save = [
            {
                "title": vacancy.title,
                "url": vacancy.url,
                "salary": vacancy.salary,
                "description": vacancy.description,
            }
            for vacancy in vacancies
        ]
        json_saver.save(data_to_save)
        print(f"Вакансии успешно сохранены в файл: {file_path}")

    print("Спасибо за использование программы. Всего хорошего!")


if __name__ == "__main__":
    user_interaction()
