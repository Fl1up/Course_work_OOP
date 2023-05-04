from hh_ru import HeadHunterAPI

if __name__ == '__main__':
    #platforms = ["HeadHunter", "SuperJob"]
    #print(f"Выберите платформу {platforms}")
    #if input() == "HeadHunter":

    search_query = input("Введите поисковый запрос: ")
    filter_words = input("Введите ключевые слова для фильтрации вакансий: ").split()
    top_n = int(input("Введите количество вакансий для вывода в топ N: "))

    hh_vacancies = HeadHunterAPI(area=1, per_page=top_n)
    hh_vacancies.search(keyword=filter_words)
    hh_vacancies.print_jobs()

    #filtered_vacancies = filter_vacancies(hh_vacancies, superjob_vacancies, filter_words)
    #if not filtered_vacancies:
        #print("Нет вакансий, соответствующих заданным критериям.")
            # return







