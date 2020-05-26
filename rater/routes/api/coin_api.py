from flask import Blueprint, request, jsonify
from rater.models.coin import Coin, coin_schema, coins_schema

bp_coin_api = Blueprint('bp_coin_api', __name__, url_prefix='/rates/api')


@bp_coin_api.route('/coin', methods=['GET'])
def api_coin():
    if request.method == 'GET':
        data = []

        coins = Coin.query.all()
        dump = coins_schema.dump(coins)

        for item in dump:
            data.append({
                "title": item['title'],
                "prices": [{
                    "live": item['price'],
                    "change": item['change'],
                    "min": item['min'],
                    "max": item['max']
                }],
                "time": item['updated_at']
            })

        return jsonify(message="success", status=200, data=data)
    return jsonify(message="Unsupported Method")
