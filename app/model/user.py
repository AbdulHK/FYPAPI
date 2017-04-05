from app import app,db,auth
from passlib.apps import custom_app_context as pwd_context
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)
class User(db.Model):
    __tablename__ = 'Users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), index=True)
    password_hash = db.Column(db.String(512))
    address = db.Column(db.String(32))
    firstname = db.Column(db.String(32))
    lastname = db.Column(db.String(32))
    deleted = db.Column(db.Integer, default=0)
    pre1 = db.Column(db.String(32))
    pre2 = db.Column(db.String(32))
    pre3 = db.Column(db.String(32))
    image_filename = db.Column(db.String)
    image_url = db.Column(db.String)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'id': self.id,
            'username': self.username,
            'address': self.address,
            'firstname': self.firstname,
            'lastname': self.lastname,
            'imgurl': self.image_url,
            'imgname': self.image_filename,
            'preferance1': self.pre1,
            'preferance2': self.pre2,
            'preferance3': self.pre3

        }
    @property
    def serializepref(self):
        """Return object data in easily serializeable format"""
        return {

        }

    @property
    def serlizeimg(self):
        """Return object data in easily serializeable format"""
        return {

        }


    def hash_password(self, password):
        self.password_hash = pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)

    def generate_auth_token(self, expiration=86400):
        s = Serializer(app.config['SECRET_KEY'], expires_in=expiration)
        return s.dumps({'id': self.id})

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None  # valid token, but expired
        except BadSignature:
            return None  # invalid token
        user = User.query.get(data['id'])
        return user
