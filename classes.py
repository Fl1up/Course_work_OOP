import json
import os
import requests
from abc import ABC, abstractmethod

""" класс ошибки """
class ParsingError(Exception):
    def __str__(self):
        return f"Ошибка получения данных по API"


""" класс получения информации """
class Vacancy:
    __slots__ = ("id", "title", "url", "salary_from", "salary_to", "employer", "api")

    def __init__(self, id, title, url, salary_from, salary_to, employer, api):

        self.id = id
        self.title = title
        self.url = url
        self.salary_from = salary_from
        self.salary_to = salary_to
        self.employer = employer
        self.api = api

    def __gt__(self, other):
        if not other.salary_from:
            return True
        elif not self.salary_from:
            return False
        return self.salary_from >= other.salary_from

    def __str__(self):
        salary_from = f"От {self.salary_from}" if self.salary_from else ""
        salary_to = f"До {self.salary_to}" if self.salary_to else ""
        if self.salary_from is None and self.salary_to is None:
            salary_from = "Не указанна"
        return f"Вакансия: \"{self.title}\" \nКомпания: \"{self.employer}\" \nЗарплата:{salary_from} {salary_to} \nUrl {self.url}"


""" класс записи,сортировки и чтения информации"""
class Connector:
    def __init__(self, keyword, vacancies_json):
        self.__fillname = f"{keyword.title()}.json"
        self.insert(vacancies_json)

    def insert(self, vacancies_json):
        with open(self.__fillname, "w", encoding="utf-8") as file:
            json.dump(vacancies_json, file, ensure_ascii=False, indent=4)

    def select(self):
        with open(self.__fillname, "r", encoding="utf-8") as file:
            date = json.load(file)
        vacancies = [Vacancy(x["id"], x["title"],x["url"], x["salary_from"], x["salary_to"], x["employer"], x["api"]) for x in
                     date]
        return vacancies

    def sorted_vacancies_by_salary_from_asc(self):
        vacancies = self.select()
        vacancies = sorted(vacancies, reverse=True)
        return vacancies

    def sorted_vacancies_by_salary_from_desc(self):
        vacancies = self.select()
        vacancies = sorted(vacancies, reverse=True)
        return vacancies

    def sorted_vacancies_by_salary_to_asc(self):
        vacancies = self.select()
        vacancies = sorted(vacancies, key=lambda x: x.salary_to if x.salary_to else 0)
        return vacancies


""" абстрактный класс """
class Engine(ABC):
    @abstractmethod
    def get_request(self):
        pass

    @abstractmethod
    def get_vacancies(self):
        pass


""" класс по поиску вакансий на хх.ру"""
class Headhanter(Engine):
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


""" класс получения вакансий на суперджобс """
class SuperJob(Engine):

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
