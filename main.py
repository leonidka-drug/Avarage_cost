from config import (
    needed_avarege_cost, income, days_number,
    CREDENTIALS_FILE, spreadsheet_id, range_)
from connect_to_sheets import connect_and_get_values


def main():
    sold_days = connect_and_get_values(CREDENTIALS_FILE, spreadsheet_id, range_)

    days_gone = len(sold_days)
    remaining_days = days_number - days_gone

    # Средний чек прошлых дней
    sold_avarege = sum(sold_days) / 11 / days_gone
    # Недостача
    shortage = (needed_avarege_cost - sold_avarege) * days_gone       
    # Средний чек следующих дней
    next_days_cost = needed_avarege_cost + shortage / remaining_days  

    print('\nЗа {} дней средний чек: {:.2f},\nНедостача: {:.2f},'.format(
        days_gone,
        sold_avarege,
        shortage,
    ))
    print('Средний чек за номер на следующие дни: {:.2f}'.format(next_days_cost))
    print('Минимальна сумма прихода на следующие дни: {:.2f}\n'. format(next_days_cost * 11))


if __name__ == "__main__":
    main()
