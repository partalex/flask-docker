from flask import Flask
from configuration import Configuration
from flask_migrate import Migrate, init, migrate, upgrade
from models import database, Status
from sqlalchemy_utils import database_exists, create_database, drop_database

app = Flask(__name__)
app.config.from_object(Configuration)

migrateObject = Migrate(app, database)

finished = False

while not finished:
    try:
        if not database_exists(app.config["SQLALCHEMY_DATABASE_URI"]):
            create_database(app.config["SQLALCHEMY_DATABASE_URI"])

        database.init_app(app)

        with app.app_context() as context:
            init()
            migrate(message="Production migration shop.")
            upgrade()
            database.session.commit()
            status1 = Status(name="Correct")
            status2 = Status(name="Waiting")
            database.session.add(status1)
            database.session.add(status2)
            database.session.commit()
            finished = True
    except Exception as error:
        print(error)
