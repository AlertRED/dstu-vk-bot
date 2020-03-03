from app.models.models_DB import *


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


class Meta(Base):
    __tablename__ = 'meta'

    id = db.Column(db.Integer, primary_key=True)
    name_param = db.Column(db.String)
    integer = db.Column(db.Integer, nullable=False, default=0)
    boolean = db.Column(db.Boolean, nullable=False, default=False)

    @staticmethod
    def create(name_param):
        param = Meta.get_first(name_param)
        if not param:
            param = Meta(name_param)
            session.add(param)
            session.commit()
        return param

    @staticmethod
    def get_first(name_param):
        return session.query(Meta).filter_by(name_param=name_param).first()

    def change(self, boolean=None, integer=None):
        if boolean is not None:
            self.boolean = boolean
        if integer is not None:
            self.integer = integer
        session.commit()