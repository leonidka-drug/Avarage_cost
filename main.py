from config import CREDENTIALS_FILE, GH_data
from connect_to_sheets import connect, get_values


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
