from flask import Blueprint, render_template, jsonify, make_response
from rater._helpers import get_currencies, get_coins, fetch_currency, save_to_database

bp_main = Blueprint('bp_main', __name__)


@bp_main.route('/rates', methods=['GET'])
def homepage():
    data_currency = get_currencies(10)
    data_coin = get_coins(10)
    return render_template('index.html', currency=data_currency, coin=data_coin)


@bp_main.route('/rates/api', methods=['GET'])
def api():
    return render_template('api/index.html')
