from rater import db, ma
from flask import Flask


class Currency(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    arabic_code = db.Column(db.String(50), nullable=False)
    alpha2_code = db.Column(db.String(50), nullable=False)
    alpha3_code = db.Column(db.String(50), nullable=False)
    country = db.Column(db.String(50), nullable=True)
    live_price = db.Column(db.Integer, nullable=False)
    change = db.Column(db.String)
    min_price = db.Column(db.Integer)
    max_price = db.Column(db.Integer)
    updated_at = db.Column(db.Integer)

    def __repr__(self):
        return '<Currency %r>' % self.alpha_3


class CurrencySchema(ma.Schema):
    class Meta:
        ordered = True
        fields = ("id", "arabic_code", "alpha2_code", "alpha3_code", "country",
                  "live_price", "change", "min_price", "max_price", "updated_at")


currency_schema = CurrencySchema()
currencies_schema = CurrencySchema(many=True)
