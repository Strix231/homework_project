import requests
import json
from config import keys


class ConvertException(Exception):
    pass


class CryptoConvertor:
    @staticmethod
    def get_price(quote: str, base: str, amount: str):
        if quote == base:
            raise ConvertException(f'Невозможно перевести одинаковые валюты {base}.')

        try:
            quote_ticket = keys[quote]
        except KeyError:
            raise ConvertException(f'Не удалось обработать валюту {quote}')

        try:
            base_ticker = keys[base]
        except KeyError:
            raise ConvertException(f'Не удалось обработать валюту {base}')

        try:
            amount_value = float(amount)
        except ValueError:
            raise ConvertException(f'Не удалось обработать количество {amount}')

        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={quote_ticket}&tsyms={base_ticker}')
        response = json.loads(r.content)

        if base_ticker not in response:
            raise ConvertException(f'Не удалось получить курс для валюты {base}')

        base_price = response[base_ticker]
        total_base = base_price * amount_value

        return total_base
