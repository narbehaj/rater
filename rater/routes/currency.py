from flask import Blueprint, render_template, jsonify, make_response
from rater._helpers import get_currencies, fetch_data, save_to_database

bp = Blueprint('bp', __name__)


@bp.route('/currency', methods=['GET'])
def currency():
    data = get_currencies(10)
    return render_template('currency/index.html', currency=data)


@bp.route('/currency/all', methods=['GET'])
def currency_all():
    data = get_currencies()
    return render_template('currency/currency-all.html', currency=data)


@bp.route('/currency/update-database', methods=['GET'])
def update_database():
    if save_to_database():
        return jsonify(message='database has been updated successfully')
