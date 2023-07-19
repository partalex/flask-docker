from flask import Flask
from configuration import Configuration
from flask_migrate import Migrate, init, migrate, upgrade
from models import database, Status
from sqlalchemy_utils import database_exists, create_database

app = Flask(__name__)
app.config.from_object(Configuration)

migrateObject = Migrate(app, database)

if not database_exists(app.config["SQLALCHEMY_DATABASE_URI"]):
    create_database(app.config["SQLALCHEMY_DATABASE_URI"])

database.init_app(app)

with app.app_context() as context:
    init()
    migrate(message="Production migration shop.")
    upgrade()
    database.session.commit()
    createdCreated = Status(name="CREATED")
    statusPending = Status(name="PENDING")
    statusComplete = Status(name="COMPLETE")
    database.session.add(createdCreated)
    database.session.add(statusPending)
    database.session.add(statusComplete)
    database.session.commit()
