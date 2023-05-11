import os
import requests
from classes import Engine, ParsingError


class SuperJob(Engine):
    """ Класс получения вакансий на суперджобс """

    def __init__(self, keyword):
        self.__header = {"X-Api-App-Id": os.getenv("SJ_API_KEY")}
        self.__params = {
            "keyword": keyword,
            "page": 0,
            "count": 100
        }
        self.__vacancies = []

    @staticmethod
    def get_salary(salary, currency):
        format_salary = None
        if salary and salary != 0:
            format_salary = salary if currency == "rub" else salary * 78
        return format_salary

    def get_request(self):  # апи
        response = requests.get("https://api.superjob.ru/2.0/vacancies/",
                                headers=self.__header,
                                params=self.__params)
        if response.status_code != 200:
            raise ParsingError
        return response.json()["objects"]

    def get_formatted_vacancies(self):  # сохранение в словарь
        formatted_vacancies = []
        for vacancy in self.__vacancies:
            formatted_vacancies.append({
                "id": vacancy["id"],
                "title": vacancy["profession"],
                "url": vacancy["link"],
                "salary_from": self.get_salary(vacancy["payment_from"], vacancy["currency"]),
                "salary_to": self.get_salary(vacancy["payment_from"], vacancy["currency"]),
                "employer": vacancy["firm_name"],
                "api": "SupetJob"
            })
        return formatted_vacancies

    def get_vacancies(self, pages_count=1):  # вывод о парсинге кол-ве вакансий и наличие ошибки
        while self.__params["page"] < pages_count:
            print(f"SuperJob, парсинг страницы {self.__params['page'] + 1}", end=": ")
            try:
                values = self.get_request()
            except ParsingError:
                print(f"Ошибка получения данных")
                break
            print(f"Найдено {len(values)} вакансий")
            self.__vacancies.extend(values)
            self.__params["page"] += 1