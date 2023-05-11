class ParsingError(Exception):
    """ Класс ошибки """
    def __str__(self):
        return f"Ошибка получения данных по API"

