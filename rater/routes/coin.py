from flask import Blueprint, render_template, jsonify, make_response
from rater._helpers import get_coins

bp_coin = Blueprint('bp_coin', __name__, url_prefix='/rates')


@bp_coin.route('/coin', methods=['GET'])
def coin():
    data = get_coins(10)
    return render_template('coin/index.html', coin=data)


@bp_coin.route('/coin/all', methods=['GET'])
def coin_all():
    data = get_coins()
    return render_template('coin/coin-all.html', coin=data)
