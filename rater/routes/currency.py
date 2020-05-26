from flask import Blueprint, render_template, jsonify, make_response, request
from rater._helpers import get_currencies, get_coins, fetch_currency, save_to_database

bp_currency = Blueprint('bp_currency', __name__, url_prefix='/rates')


# @bp_currency.route('/rates', methods=['GET'])
# def currency():
#     data_currency = get_currencies(10)
#     data_coin = get_coins(10)
#     return render_template('index.html', currency=data_currency, coin=data_coin)


@bp_currency.route('/currency/all', methods=['GET'])
def currency_all():
    data = get_currencies()
    return render_template('currency/currency-all.html', currency=data)


@bp_currency.route('/currency/update-database', methods=['POST'])
def update_database():
    data = request.get_json()
    if data['token'] == 'MY_TOKEN':
        if save_to_database():
            return jsonify(message='database has been updated successfully')
