class Vacancy:
    """ Класс получения информации """
    __slots__ = ("id", "title", "url", "salary_from", "salary_to", "employer", "api")

    def __init__(self, id, title, url, salary_from, salary_to, employer, api):

        self.id = id
        if not isinstance(title, str):
            raise ValueError("Параметр должен быть строкой")
        if len(title) > 100:
            raise ValueError("Название должно быть не более 100 символов")
        self.title = title
        if not isinstance(url, str):
            raise ValueError("Параметр должен быть строкой")
        if not url.startswith("http"):
            raise ValueError("URL должен начинаться с http")
        self.url = url
        if salary_from is not None and salary_from < 0:
            raise ValueError("Значение salary_from не может быть отрицательным")
        self.salary_from = salary_from
        if salary_to is not None and salary_to < 0:
            raise ValueError("Значение salary_to не может быть отрицательным")
        self.salary_to = salary_to
        if not isinstance(api, str):
            raise ValueError("Параметр должен быть строкой")
        self.employer = employer
        if not isinstance(api, str):
            raise ValueError("Параметр должен быть строкой")
        self.api = api

        @property
        def title(self):
            return self._title

        @title.setter
        def title(self, value):
            if not isinstance(value, str):
                raise ValueError("Параметр должен быть строкой")
            if len(value) > 100:
                raise ValueError("Название должно быть не более 100 символов")
            self._title = value

        @property
        def url(self):
            return self._url

        @url.setter
        def url(self, value):
            if not isinstance(value, str):
                raise ValueError("Параметр должен быть строкой")
            if not value.startswith("http"):
                raise ValueError("URL должен начинаться с http")
            self._url = value

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