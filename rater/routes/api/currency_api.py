from flask import Blueprint, request, jsonify
from rater._helpers import fetch_currency

bp_api = Blueprint('bp_api', __name__, url_prefix='/api')


@bp_api.route('/currency', methods=['GET'])
def api_currency():
    if request.method == 'GET':
        currency = fetch_currency()

        return jsonify(message="success", status=200, data=currency)
    else:
        return jsonify(message="failed", status=400)
