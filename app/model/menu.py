from app import db
from .restaurant import Restaurant
class Menu(db.Model):
    __tablename__ = 'Menu'
    id = db.Column(db.Integer, primary_key=True)
    restid = db.Column(db.Integer,db.ForeignKey(Restaurant.id))
    dish = db.Column(db.String(64))
    price = db.Column(db.Integer)
    description = db.Column(db.String(128))

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'dish': self.dish,
            'price': self.price,
            'description': self.description

        }