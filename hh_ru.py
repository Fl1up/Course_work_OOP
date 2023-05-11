import requests
from classes import Engine, ParsingError


class Headhanter(Engine):
    """ Класс по поиску вакансий на хх.ру"""
    def __init__(self, keyword):
        self.__header = {
            "User-agent": "Mozila/5.0 (platform; rv:geckoversion) Gecko/geckotrail Firefox/firefoxversion"}
        self.__params = {
            "text": keyword,
            "page": 0,
            "per_page": 100
        }
        self.__vacancies = []

    @staticmethod
    def get_salary(salary):
        formatted_salary = [None, None]
        if salary and salary["from"] and salary["from"] != 0:
            formatted_salary[0] = salary["from"] if salary["currency"].lower() == "rur" else salary["from"] * 78
        if salary and salary["to"] and salary["to"] != 0:
            formatted_salary[1] = salary["to"] if salary["currency"].lower() == "rur" else salary["to"] * 78
            return formatted_salary

    def get_request(self):  # получения апи
        response = requests.get("https://api.hh.ru/vacancies",
                                headers=self.__header,
                                params=self.__params)
        if response.status_code != 200:
            raise ParsingError
        return response.json()["items"]

    def get_formatted_vacancies(self):  # сохранение в словарь
        formatted_vacancies = []
        for vacancy in self.__vacancies:
            salary_from, salary_to = self.get_salary(vacancy["salary"])
            formatted_vacancies.append({
                "id": vacancy["id"],
                "title": vacancy["name"],
                "url": vacancy["alternate_url"],
                "salary_from": salary_from,
                "salary_to": salary_to,
                "employer": vacancy["employer"]["name"],
                "api": "HeadHunter"
            })
            return formatted_vacancies

    def get_vacancies(self, pages_count=1):  # вывод о парсинге кол-ве вакансий и наличие ошибки
        while self.__params["page"] < pages_count:
            print(f"HeadHunter, парсинг страницы {self.__params['page'] + 1}", end=": ")
            try:
                values = self.get_request()
            except ParsingError:
                print("Ошибка получения данный ")
                break
            print(f"Найдено {len(values)} вакансий")
            self.__vacancies.extend(values)
            self.__params["page"] += 1