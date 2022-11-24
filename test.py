from main import CashCalculator, Record


# создадим калькулятор денег с дневным лимитом 1000
cash_calculator = CashCalculator(1000)

# дата в параметрах не указана,
# так что по умолчанию к записи должна автоматически добавиться сегодняшняя дата
cash_calculator.add_record(Record(amount=145, comment="кофе"))
# и к этой записи тоже дата должна добавиться автоматически
cash_calculator.add_record(Record(amount=300, comment="Серёге за обед"))
# а тут пользователь указал дату, сохраняем её
cash_calculator.add_record(Record(amount=2800, comment="бар в Танин др", date="23.11.2022"))
# запись за прошлую неделю
cash_calculator.add_record(Record(amount=200, comment="Ивану за обед", date="14.11.2022"))
print([x.comment for x in cash_calculator.records])

res_rub = cash_calculator.get_today_cash_remained("rub")
res_usd = cash_calculator.get_today_cash_remained("usd")
print(res_rub)
print(res_usd)

today_stats = cash_calculator.get_today_stats()
print(f'За сегодня: {today_stats}')

week_stats = cash_calculator.get_week_stats()
print(f'За неделю: {week_stats}')

assert res_rub == 'На сегодня осталось 555.0 руб'
assert res_usd == 'На сегодня осталось 9.25 USD'
assert week_stats == 3245
assert today_stats == 445
print("OK!")