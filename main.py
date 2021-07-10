from pprint import pprint
import re

from config import CREDENTIALS_FILE, GH_data
from connect_to_sheets import connect, get_values


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


def calc_return_pays():
    # Здесь пишу калькулятор неотживших предоплат

    valu = get_values(connect(CREDENTIALS_FILE), data['spreadsheet_id'], "'Приход'!B10:D347") 
    # pprint(valu)
    # x = 0
    # for val in valu:
    #     x += int(val[0])
    # print(x)
    reg = r'\d\d\.\d\d'
    all_prepays = sum([int(val[0]) for val in valu if val[2] == 'Предоплата' and not conv_dates(re.search(reg, val[1]).group(), '15.07')])
    print(all_prepays)

    # print(conv_dates('01.07', '10.07'))
    # reg = r'\d\d\.\d\d'
    # re.search(reg, '').group()

    # Здесь закончил писать калькулатор


def main():
    GH_number = int(input("Напиши 1, если нужна информация по Теплу, Напиши 2 - по Софии: "))
    if GH_number == 1:
        data = GH_data['teplo']
    else:
        data = GH_data['sofia']

    income = data['needed_avarege_cost'] * data['ROOMS_NUMBER'] * data['days_number']

    sold_days = get_values(connect(CREDENTIALS_FILE), data['spreadsheet_id'], data['range_B'])
    sold_days = [int(val) for val in sold_days]

    days_gone = len(get_values(connect(CREDENTIALS_FILE), data['spreadsheet_id'], data['range_A']))
    remaining_days = data['days_number'] - days_gone

    sold_avarege = (sum(sold_days) + data['fora']) / data['ROOMS_NUMBER'] / days_gone  # Средний чек прошлых дней
    shortage = (data['needed_avarege_cost'] - sold_avarege) * days_gone                # Недостача
    next_days_cost = data['needed_avarege_cost'] + shortage / remaining_days           # Средний чек след-их дней

    print('\nЗа {} дней средний чек: {:.2f},\nНедостача: {:.2f},'.format(
        days_gone,
        sold_avarege,
        shortage,
    ))
    print('Средний чек за номер на следующие дни: {:.2f}'.format(next_days_cost))
    print('Минимальна сумма прихода на следующие дни: {:.2f}\n'. format(next_days_cost * data['ROOMS_NUMBER']))

if __name__ == "__main__":
    main()
