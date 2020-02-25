from app.models.orm_models import *


class Log(Base):
    __tablename__ = 'log'
    id = db.Column(db.Integer, primary_key=True)

    vk_id = db.Column(db.Integer)
    text = db.Column(db.String, nullable=False)
    created_date = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    @staticmethod
    def create(text, vk_id=None):
        log = Log(text=text, vk_id=vk_id)
        session.add(log)
        session.commit()
        return log
