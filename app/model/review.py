from app import db
from .user import User
class Review(db.Model):
    __tablename__ = 'Review'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32),db.ForeignKey(User.username))
    title= db.Column(db.String(64))
    rest_id=db.Column(db.Integer)
    overall_rate=db.Column(db.Integer)
    discription=db.Column(db.String(512))
    deleted=db.Column(db.String,default=0)
    image_filename = db.Column(db.String)
    image_url = db.Column(db.String)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'id':self.id,
            'overall_rate': self.overall_rate,
            'discription': self.discription,
            'username': self.username,
            'imgurl': self.image_url,
            'imgname': self.image_filename,
            'title': self.title

        }
