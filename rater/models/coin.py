from rater import db, ma


class Coin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    change = db.Column(db.String)
    min = db.Column(db.Integer)
    max = db.Column(db.Integer)
    updated_at = db.Column(db.Integer)

    def __repr__(self):
        return '<Coin %r>' % self.title


class CoinSchema(ma.Schema):
    class Meta:
        ordered = True
        fields = ("id", "title", "price", "change", "min", "max", "updated_at")


coin_schema = CoinSchema()
coins_schema = CoinSchema(many=True)
