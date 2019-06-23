from sqlalchemy.orm import Session
from app.models.models import Place, TypePlace, Day_of_week, Post, Phone_place, Manager, Schedule, Grant, Condition, \
    Payment


class grantDAO:

    def __init__(self, db: Session):
        self.db = db

    def create_or_update_grant(self, name:str , need_statement: bool, conditions: list, payments: list):

        grant = self.db.query(Grant).filter_by(name=name).first()
        if grant:
            grant.need_statement = need_statement
        else:
            grant = Grant(name=name, need_statement=need_statement)
            self.db.add(grant)
        self.db.commit()

        for description in conditions:
            condition = Condition(description=description, grant=grant)
            self.db.add(condition)
        self.db.commit()

        for i in payments:
            payment = Payment(foreigner=i.get('foreigner'),
                              conditions=i.get('conditions'),
                              form_of_study=i.get('form_of_study'),
                              money=i.get('money'),
                              grant=grant)
            self.db.add(payment)
        self.db.commit()

