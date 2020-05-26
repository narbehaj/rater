import requests
import re
import pycountry

from flask import jsonify
from bs4 import BeautifulSoup
from rater.models.currency import Currency, currencies_schema
from rater.models.coin import Coin, coins_schema
from unidecode import unidecode
from . import db


def fetch_currency():
    urls = [
        'https://tgju.org/currency',
        'https://www.tgju.org/currency-minor'
    ]

    currency = []

    for url in urls:
        resp = requests.get(url)
        html = BeautifulSoup(resp.text, 'html.parser')

        tables = html.find_all('table', class_='market-table')

        for table in tables:
            tbody = table.find('tbody')
            rows = tbody.find_all('tr')

            for row in rows:
                field = row.findChildren(['th', 'td'], recursive=False)

                title = field[0].text.strip()
                alpha2 = str(field[0].find('span').attrs['class'][1].replace('flag-', '')).upper()
                alpha3 = 'USD' if row['data-market-row'] == 'price_dollar_rl' \
                    else row['data-market-row'].replace('price_', '').upper()
                country = pycountry.countries.get(alpha_2=alpha2)
                live_price = field[1].text.strip()
                change = field[2].text.strip()
                min_price = field[3].text.strip()
                max_price = field[4].text.strip()
                updated_at = field[5].text.strip()

                if 'high' in field[2].find('span').attrs['class']:
                    sign = '+ '
                elif 'low' in field[2].find('span').attrs['class']:
                    sign = '- '
                else:
                    sign = ''

                currency.append({
                    "title": title,
                    "codes": [{
                        "alpha2": alpha2,
                        "alpha3": alpha3
                    }],
                    "country": country.name if country else '-',
                    "prices": [{
                        "live": live_price,
                        "change": str(sign) + change,
                        "min": min_price,
                        "max": max_price
                    }],
                    "time": unidecode(updated_at) if re.search(':', updated_at) else "-"
                })

    return currency


def fetch_coin():
    urls = [
        'https://www.tgju.org/coin'
    ]

    coin = []

    for url in urls:
        resp = requests.get(url)
        html = BeautifulSoup(resp.text, 'html.parser')

        tables = html.find_all('table', class_='market-table')

        for table in tables:
            tbody = table.find('tbody')
            rows = tbody.find_all('tr')

            for row in rows:
                field = row.findChildren(['th', 'td'], recursive=False)

                title = field[0].text.strip()
                live_price = field[1].text.strip()
                change = field[2].text.strip()
                min_price = field[3].text.strip()
                max_price = field[4].text.strip()
                updated_at = field[5].text.strip()

                if 'high' in field[2].find('span').attrs['class']:
                    sign = '+ '
                elif 'low' in field[2].find('span').attrs['class']:
                    sign = '- '
                else:
                    sign = ''

                coin.append({
                    "title": title,
                    "prices": [{
                        "live": live_price,
                        "change": str(sign) + change,
                        "min": min_price,
                        "max": max_price
                    }],
                    "time": unidecode(updated_at) if re.search(':', updated_at) else "-"
                })

    return coin


def save_to_database():
    data_currency = fetch_currency()
    data_coin = fetch_coin()

    if data_currency and data_coin:
        db.session.query(Currency).delete()
        db.session.query(Coin).delete()

        for currency in data_currency:
            rate_currency = Currency(title=currency['title'],
                                     alpha2=currency['codes'][0]['alpha2'],
                                     alpha3=currency['codes'][0]['alpha3'],
                                     country=currency['country'],
                                     price=currency['prices'][0]['live'],
                                     change=currency['prices'][0]['change'],
                                     min=currency['prices'][0]['min'],
                                     max=currency['prices'][0]['max'],
                                     updated_at=currency['time']
                                     )
            db.session.add(rate_currency)

        for coin in data_coin:
            rate_coin = Coin(
                title=coin['title'],
                price=coin['prices'][0]['live'],
                change=coin['prices'][0]['change'],
                min=coin['prices'][0]['min'],
                max=coin['prices'][0]['max'],
                updated_at=coin['time']
            )
            db.session.add(rate_coin)

        db.session.commit()

        return jsonify(message="success", status=200, currency=data_currency, coin=data_coin), 200


def get_currencies(limit=None):
    if limit:
        currencies = Currency.query.limit(limit).all()
    else:
        currencies = Currency.query.all()

    data = currencies_schema.dump(currencies)

    return data


def get_coins(limit=None):
    if limit:
        coins = Coin.query.limit(limit).all()
    else:
        coins = Coin.query.all()

    data = coins_schema.dump(coins)

    return data
