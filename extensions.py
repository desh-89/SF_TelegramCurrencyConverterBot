import json
import requests
from config import exchanges

class APIException(Exception):
    pass


class Convertor:
    @staticmethod
    def get_price(base, sym, amount):
        try:
            base_key = exchanges[base.lower()]
        except KeyError:
            raise APIException(f"Валюта {base} не найдена!")

        try:
            sym_key = exchanges[sym.lower()]
        except KeyError:
            raise APIException(f"Валюта {sym} не найдена!")

        if base_key == sym_key:
            raise APIException(f'Невозможно перевести одинаковые валюты {base}!')
        
        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'Не удалось обработать количество {amount}!')
        
        access_key = '0fffbd1167776523be75'
        r = requests.get(f"https://free.currconv.com/api/v7/convert?q={base_key}_{sym_key}&compact=ultra&apiKey={access_key}")
        resp = json.loads(r.content)
        new_price = resp[f'{base_key}_{sym_key}'] * amount
        return round(new_price, 2)