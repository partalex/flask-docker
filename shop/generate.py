from flask import Flask
from models import database, Status
from sqlalchemy_utils import database_exists
from configuration import Configuration

app = Flask(__name__)
app.config.from_object(Configuration)

while True:
    if not database_exists(Configuration.SQLALCHEMY_DATABASE_URI):
        print("Database does not exists.")
        break
    else:
        database.init_app(app)
        with app.app_context() as contex:
            status1 = Status(name="CREATED")
            status2 = Status(name="PENDING")
            status3 = Status(name="COMPLETED")

            database.session.add(status1)
            database.session.add(status2)
            database.session.add(status3)
            database.session.commit()
            print("Added statutes.")
    break
