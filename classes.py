import json
from vacancy import Vacancy
from abc import ABC, abstractmethod

class Connector:
    """ Класс записи, сортировки и чтения информации"""
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



class Engine(ABC):
    """ абстрактный класс """
    @abstractmethod
    def get_request(self):
        pass

    @abstractmethod
    def get_vacancies(self):
        pass

