import requests
import re
import pycountry

from flask import Blueprint, request, jsonify
from bs4 import BeautifulSoup
from rater.models.currency import Currency, currency_schema, currencies_schema
from unidecode import unidecode
from . import create_app, db


def fetch_data():
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

                arabic_code = field[0].text.strip()
                alpha2_code = str(field[0].find('span').attrs['class'][1].replace('flag-', '')).upper()
                alpha3_code = 'USD' if row['data-market-row'] == 'price_dollar_rl' \
                    else row['data-market-row'].replace('price_', '').upper()
                country = pycountry.countries.get(alpha_2=alpha2_code)
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
                    "titles": [{
                        "alpha2": alpha2_code,
                        "alpha3": alpha3_code,
                        "arabic": arabic_code
                    }],
                    "country": country.name if country else '-',
                    "prices": [{
                        "current": live_price,
                        "change": str(sign) + change,
                        "min": min_price,
                        "max": max_price
                    }],
                    "time": unidecode(updated_at) if re.search(':', updated_at) else "-"
                })

    return currency


def save_to_database():
    data = fetch_data()

    if data:
        db.session.query(Currency).delete()

        for item in data:
            rate = Currency(arabic_code=item['titles'][0]['arabic'],
                            alpha2_code=item['titles'][0]['alpha2'],
                            alpha3_code=item['titles'][0]['alpha3'],
                            country=item['country'],
                            live_price=item['prices'][0]['current'],
                            change=item['prices'][0]['change'],
                            min_price=item['prices'][0]['min'],
                            max_price=item['prices'][0]['max'],
                            updated_at=item['time']
                            )
            db.session.add(rate)
            db.session.commit()

        return jsonify(message="success", status=200, currency=data), 200


def get_currencies(limit=None):
    if limit:
        currencies = Currency.query.limit(limit).all()
    else:
        currencies = Currency.query.all()

    data = currencies_schema.dump(currencies)

    return data
