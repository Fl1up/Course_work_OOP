class Vacancy:
    """ Класс получения информации """
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

    def __lt__(self, other):
        if not other.salary_from:
            return True
        elif not self.salary_from:
            return False
        return self.salary_from <= other.salary_from

    def __le__(self, other):
        if not other.salary_from:
            return True
        elif not self.salary_from:
            return False
        return self.salary_from <= other.salary_from

    def __ge__(self, other):
        if not other.salary_from:
            return True
        elif not self.salary_from:
            return False
        return self.salary_from >= other.salary_from

    def __eq__(self, other):
        if not other.salary_from:
            return True
        elif not self.salary_from:
            return False
        return self.salary_from == other.salary_from

    def __str__(self):
        salary_from = f"От {self.salary_from}" if self.salary_from else ""
        salary_to = f"До {self.salary_to}" if self.salary_to else ""
        if self.salary_from is None and self.salary_to is None:
            salary_from = "Не указанна"
        return f"Вакансия: \"{self.title}\" \nКомпания: \"{self.employer}\" \nЗарплата:{salary_from} {salary_to} \nUrl {self.url}"