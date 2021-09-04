import re

from connect_to_sheets import get_values


def conv_dates(booked_date, my_date):
    b_day = int(booked_date[:2])
    b_month = int(booked_date[3:5])
    my_day = int(my_date[:2])
    my_month = int(my_date[3:5])
    # print(b_day, b_month, my_day, my_month)
    if b_month < my_month:
        return True
    elif b_month > my_month:
        return False
    else:
        if b_day < my_day:
            return True
        else:
            return False


def unrealized_prepays_calc(date: str):
    values = get_values(data['spreadsheet_id'], "'Приход'!B10:D347")
    values = [val for val in values['values'] if val]

    reg = r'\d\d\.\d\d'
    all_prepays = sum([int(val[0]) for val in values if val[2] == 'Предоплата' and not conv_dates(re.search(reg, val[1]).group(), date)])

    # all_prepays = [int(val[0]) for val in values if val[2] == 'Предоплата' and not conv_dates(re.search(reg, val[1]).group(), '15.07')]
    # all_p = [(val[1], int(val[0])) for val in values if val[2] == 'Предоплата' and not conv_dates(re.search(reg, val[1]).group(), '15.07')]

    return all_prepays


def print_prepays_calc_result():
    # Вывод в консоль для калькулятора предоплат
    # print(' Сумма предоплат людей, которые ещё не отжили: {}\n'.format(sum(all_prepays)))
    # i = 1
    # for n, c in all_p:
    #     print("{}. {}      ::{}".format(i, n, c))
    #     i += 1
    # Сохранение в файл
    # with open('prepays.txt', 'w') as file:
    #     i = 1
    #     for n, c in all_p:
    #         file.write("{}. {}      ::{}\n".format(i, n, c))
    #         i += 1