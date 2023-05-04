import requests


class Job:
    def __init__(self, title, company, location, to_salary, salary, strong):
        self.title = title
        self.company = company
        self.location = location
        self.to_salary = to_salary
        self.salary = salary
        self.strong = strong

    def __str__(self):
        return f"{self.title} ({self.company}) -{self.to_salary} {self.salary} руб. в {self.location} \n{self.strong}"


class JobSearch:
    """
    Создаем класс для фильтрации полученной информации.
    Создаем пустой словарь.

    Действия со словарем:
    1- добавление.
    2- удаление.

    Фильтруем по регистру

    Создаем файл и записываем информацию

    Открываем файл и чистаем с него информацию
    """

    def init(self):
        self.jobs = []

    def add_job(self, job):
        self.jobs.append(job)

    def remove_job(self, job):
        self.jobs.remove(job)

    def filter_jobs(self, keyword=None, location=None, salary=None):
        filtered_jobs = []
        for job in self.jobs:
            if keyword and keyword.lower() not in job.title.lower():
                continue
            if location and location.lower() not in job.location.lower():
                continue
            if salary and job.salary < salary:
                continue
            filtered_jobs.append(job)
        return filtered_jobs

    def save_to_file(self, filename):
        with open(filename, "w") as file:
            for job in self.jobs:
                file.write(f"{job.title}\t{job.company}\t{job.location}\t{job.salary}\t{job.strong}\n")

    def load_from_file(self, filename):
        with open(filename, "r") as file:
            for line in file:
                title, company, location, salary, strong = line.strip().split("\t")
                job = Job(title, company, location, int(salary), strong)
                self.add_job(job)


class HeadHunterAPI(JobSearch):
    def __init__(self, area=1, per_page=None):
        super().init()
        self.area = area
        self.per_page = per_page

    def search(self, keyword=None, location=None, to_salary=None, salary=None, strong=None):
        api = "https://api.hh.ru/vacancies"
        params = {
            "text": keyword,  # ключ слово
            "area": self.area,  # локация
            "to_salary": to_salary,
            "salary": salary,  # зарплата
            "only_with_salary": True,  # только с зарплатой
            "strong": strong,  # требования
            "per_page": 100,  # количество результатов на странице
            "page": 0  # начальная страница
        }
        if location:
            params["area"] = location
        while True:
            response = requests.get(api, params=params)
            data = response.json()
            for item in data["items"]:
                title = item["name"]
                company = item["employer"]["name"]
                location = item["area"]["name"]
                salary = item["salary"]["from"]
                to_salary = item["salary"]["to"]
                strong = item["snippet"]["requirement"]
                job = Job(title, company, location, to_salary, salary, strong)
                self.add_job(job)
            if data["pages"] <= params["page"]:  # если достигнута последняя страница
                break
            params["page"] += 1  # увеличиваем номер страницы

    def print_jobs(self):
        for i, job in enumerate(self.jobs):
            if i == self.per_page:
                break
            else:
                print(f"{i + 1}. {job.title}\nКомпания: {job.company}\nГород: {job.location}\nТербования: {job.strong}")
                if job.salary:
                    if job.to_salary != None:
                        print(f"Заработная плата: {job.salary} до {job.to_salary}")
                else:
                    print(f"Заработная плата: до {job.to_salary}")
