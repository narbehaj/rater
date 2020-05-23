from flask import Blueprint, request, render_template
from rater._helpers import fetch_currency

bp = Blueprint('bp', __name__, url_prefix='/')


@bp.route('/currency', methods=['GET'])
def currency():
    if request.method == 'GET':
        currency = fetch_currency()

        return render_template('/currency/index.html', currency=currency)
