from flask import Blueprint, request, jsonify
from rater.models.currency import Currency, currency_schema, currencies_schema

bp_api = Blueprint('bp_api', __name__, url_prefix='/api')


@bp_api.route('/currency', methods=['GET'])
def api_currency():
    if request.method == 'GET':
        data = []

        currencies = Currency.query.all()
        dump = currencies_schema.dump(currencies)

        for item in dump:
            data.append({
                "titles": [{
                    "alpha2": item['alpha2_code'],
                    "alpha3": item['alpha3_code'],
                    "arabic": item['arabic_code']
                }],
                "country": item['country'],
                "prices": [{
                    "current": item['live_price'],
                    "change": item['change'],
                    "min": item['min_price'],
                    "max": item['max_price']
                }],
                "time": item['updated_at']
            })

        return jsonify(message="success", status=200, data=data)
    return jsonify(message="Unsupported Method")


@bp_api.route('/currency/<string:code>')
def api_currency_by(code):
    if request.method == 'GET':
        data = []

        currency = Currency.query.filter_by(alpha3_code=code.upper()).first()
        dump = currency_schema.dump(currency)

        data.append({
            "titles": [{
                "alpha2": dump['alpha2_code'],
                "alpha3": dump['alpha3_code'],
                "arabic": dump['arabic_code']
            }],
            "country": dump['country'],
            "prices": [{
                "change": dump['change'],
                "min": dump['min_price'],
                "max": dump['max_price']
            }],
            "time": dump['updated_at']
        })

        return jsonify(message="Success", status=200, data=data)

    return jsonify(message="Unsupported Method")
