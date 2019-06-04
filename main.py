from sqlalchemy.orm import Session

import models
from app import app

db = Session(bind=models.engine)
app = app(db)

if __name__ == '__main__':
    app.run()
