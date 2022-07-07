from pprint import pprint


def salaryAnalizer(salary, vacancies):
    for vacancy in vacancies:
        vac_salary = vacancy['salary']
        minimal = vac_salary['min']
        maximal = vac_salary['max']
        pprint(vacancy)
        if salary > minimal and salary < maximal:
            pprint(vacancy)
