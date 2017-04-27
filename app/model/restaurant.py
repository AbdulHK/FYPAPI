from app import app, db,auth
from flask import jsonify, request, abort
from werkzeug.utils import secure_filename

class Restaurant(db.Model):
    __tablename__ ='Restaurant'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    address1 =db.Column(db.String(128))
    address2 = db.Column(db.String(32))
    phone =db.Column(db.Integer)
    lat = db.Column(db.Float(precision='12,10'),index=True)
    lng = db.Column(db.Float(precision='12,10'),index=True)
    cost = db.Column(db.Integer)
    menu_type = db.Column(db.String(64))
    rate =db.Column(db.Float(precision='3,2'))
    offer=db.Column(db.String(128))
    deleted =db.Column(db.Integer,default=0)
    has_delivery = db.Column(db.String(1),default=0)
    has_parking = db.Column(db.String(1),default=0)
    has_wifi = db.Column(db.String(1),default=0)
    has_reservation = db.Column(db.String(1),default=0)
    has_cards = db.Column(db.String(1),default=0)
    has_bar = db.Column(db.String(1),default=0)
    has_terrace = db.Column(db.String(1),default=0)
    image_filename = db.Column(db.String)
    image_url = db.Column(db.String)



    @property
    def serialize(self):
       """Return object data in easily serializeable format"""
       return {
           'id'  : self.id,
           'name': self.name,
           'address1'  : self.address1,
           'address2': self.address2,
           'phone'  : self.phone,
           'lat': self.lat,
           'lng'  : self.lng,
           'cost': self.cost,
           'menu_type'  : self.menu_type,
           'rate': self.rate,
           'imgurl': self.image_url,
           'imgname': self.image_filename,
           'offer' : self.offer,
           'has_delivery': self.has_delivery,
           'has_bar':self.has_bar,
           'has_cards': self.has_cards,
           'has_terrace': self.has_terrace,
           'has_wifi': self.has_wifi,
           'has_parking': self.has_parking,
           'has_reservation': self.has_reservation
       }
