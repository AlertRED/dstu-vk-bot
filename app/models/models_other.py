from datetime import datetime

from app.models.models import db


class Log(db.Model):
    __tablename__ = 'log'
    id = db.Column(db.Integer, primary_key=True)

    vk_id = db.Column(db.Integer)
    text = db.Column(db.String, nullable=False)
    created_date = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    @staticmethod
    def create(text, vk_id=None):
        log = Log(text=text, vk_id=vk_id)
        db.session.add(log)
        db.session.commit()
        return log