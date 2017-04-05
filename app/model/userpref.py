from app import db

class UserPref(db.Model):
    __tablename__ = 'UserPref'
    id = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.Integer)
    pre1 = db.Column(db.String(32))
    pre2 = db.Column(db.String(32))
    pre3 = db.Column(db.String(32))

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'pre1': self.pre1,
            'pre2': self.pre2,
            'pre3':self.pre3,
            'userid':self.userid
        }