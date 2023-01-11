from . import db


class Favorite(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    city_name = db.Column(db.String(30), unique=True)

    def __repr__(self):
        return f"{self.city_name}"
