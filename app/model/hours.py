from app import db

class Hours(db.Model):
    __tablename__ = 'Hours'
    id= db.Column(db.Integer,primary_key=True)
    restid = db.Column(db.Integer)
    Day = db.Column(db.String(32))
    StartTime = db.Column(db.String(32))
    StartTime = db.Column(db.String(32))
    FinishTime = db.Column(db.String(32))

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'StartTime': self.StartTime,
            'FinishTime': self.FinishTime,
            'Day':self.Day
        }