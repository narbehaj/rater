import requests
import re

from flask import Blueprint, request, jsonify
from bs4 import BeautifulSoup


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

                arabic_code = field[0].text.strip()
                alpha2_code = str(field[0].find('span').attrs['class'][1].replace('flag-', '')).upper()
                alpha3_code = 'usd' if row['data-market-row'] == 'price_dollar_rl' \
                    else row['data-market-row'].replace('price_', '')
                live_price = field[1].text.strip()
                change = field[2].text.strip()
                min_price = field[3].text.strip()
                max_price = field[4].text.strip()

                if 'high' in field[2].find('span').attrs['class']:
                    sign = '+ '
                elif 'low' in field[2].find('span').attrs['class']:
                    sign = '- '
                else:
                    sign = ''

                currency.append({
                    "arabic_title": arabic_code,
                    "alpha2_code": alpha2_code,
                    "alpha3_code": alpha3_code,
                    "price": live_price,
                    "change": str(sign) + change,
                    "min_price": min_price,
                    "max_price": max_price
                })

    return currency
