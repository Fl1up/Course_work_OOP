from superJob import SuperJob
from classes import Connector
from hh_ru import Headhanter


def main():
    vacancies_json = []
    keyword = "Python"
    #keyword = input("Введите ключевое слово для поиска\n")
    if len(keyword) >= 50:
        raise ValueError("Название должно быть не более 100 символов")
    if not isinstance(keyword, str):
        raise ValueError("Параметр должен быть строкой")

    hh = Headhanter(keyword)
    sj = SuperJob(keyword)

    for api in (hh, sj):
        api.get_vacancies(pages_count=1)
        vacancies_json.extend(api.get_formatted_vacancies())

    connector = Connector(keyword=keyword, vacancies_json=vacancies_json)

    while True:
        command = input(
            "1 - вывести список вакансий:\n"
            "2 - отсортировать по минимальной зарплате:\n"
            "3 - отсортировать по минимальной зарплате (DESC):\n"
            "4 - отсортировать по максимальной зарплате (DESC):\n"
            "exit - для выхода.\n"
        )
        if command.lower() == "exit":
            return
        elif command == "1":
            vacancies = connector.select()
        elif command == "2":
            vacancies = connector.sorted_vacancies_by_salary_from_asc()
        elif command == "3":
            vacancies = connector.sorted_vacancies_by_salary_from_desc()
        elif command == "4":
            vacancies = connector.sorted_vacancies_by_salary_from_asc()

        for vacancy in vacancies:
            print(vacancy, end="\n\n")


if __name__ == "__main__":
    main()





