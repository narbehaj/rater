import os

from flask import Flask
from flask_marshmallow import Marshmallow
from flask_htmlmin import HTMLMIN

ma = Marshmallow()
htmlmin = HTMLMIN()


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_pyfile('config.py', silent=True)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    ma.init_app(app)
    htmlmin.init_app(app)

    from rater.routes import currency
    from rater.routes.api import currency_api

    # template routes
    app.register_blueprint(currency.bp)
    # api routes
    app.register_blueprint(currency_api.bp_api)

    return app
