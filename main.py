import datetime as dt
from string import Template


class Record:
    def __init__(self, amount, comment, date=''):
        self.amount = amount
        self.date = (
            dt.datetime.now().date() if not date
            else dt.datetime.strptime(date, '%d.%m.%Y').date())
        self.comment = comment


class Calculator:
    def __init__(self, limit):
        self.limit = limit
        self.records = []

    def add_record(self, record):
        self.records.append(record)

    def get_today_stats(self):
        today_stats = 0
        today = dt.datetime.now().date()
        for record in self.records:
            today_stats += record.amount if record.date == today else 0
        return today_stats

    def get_week_stats(self):
        week_stats = 0
        today = dt.datetime.now().date()
        for record in self.records:
            diff = (today - record.date).days
            week_stats += record.amount if 0 <= diff < 7 else 0
        return week_stats


class CaloriesCalculator(Calculator):
    EAT_MSG = 'Сегодня можно съесть что-нибудь' \
                   ' ещё, но с общей калорийностью не более $amount кКал'
    NO_EAT_MSG = 'Хватит есть!'

    def get_calories_remained(self):  # Получает остаток калорий на сегодня
        x = self.limit - self.get_today_stats()
        if x > 0:
            return Template(self.EAT_MSG).substitute(amount=x)
        return self.NO_EAT_MSG


class CashCalculator(Calculator):
    USD_RATE = float(60)  # Курс доллар США.
    EURO_RATE = float(70)  # Курс Евро.
    HAS_CASH = 'На сегодня осталось $cash $type'
    NO_CASH = 'Денег нет, держись'
    HAS_DEBT = 'Денег нет, держись: твой долг -$cash $type'

    def get_today_cash_remained(self, currency,
                                usd_rate=USD_RATE, euro_rate=EURO_RATE):
        cash_remained = self.limit - self.get_today_stats()
        cash_convert = {
            'usd': (usd_rate, 'USD'),
            'eur': (euro_rate, 'Euro'),
            'rub': (1.00, 'руб'),
        }
        cash_rate, currency_type = cash_convert[currency]
        cash_remained /= cash_rate

        if cash_remained > 0:
            return Template(self.HAS_CASH).substitute(cash=round(cash_remained, 2), type=currency_type)
        elif cash_remained == 0:
            return self.NO_CASH
        elif cash_remained < 0:
            return Template(self.HAS_DEBT).substitute(cash=round(cash_remained, 2), type=currency_type)

