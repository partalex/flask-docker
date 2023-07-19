from flask import Flask
from configuration import Configuration
from flask_migrate import Migrate, init, migrate, upgrade
from models import database, Role, User, UserRole
from sqlalchemy_utils import database_exists, create_database

app = Flask(__name__)
app.config.from_object(Configuration)

migrateObject = Migrate(app, database)

database.init_app(app)
if not database_exists(app.config["SQLALCHEMY_DATABASE_URI"]):
    create_database(app.config["SQLALCHEMY_DATABASE_URI"])


with app.app_context() as context:
    init()
    migrate(message="Production migration")
    upgrade()

    ownerRole = Role(name="owner")
    courierRole = Role(name="courier")
    customerRole = Role(name="customer")

    database.session.add(ownerRole)
    database.session.add(courierRole)
    database.session.add(customerRole)
    database.session.commit()

    owner = User(
        email="onlymoney@gmail.com", password="evenmoremoney", forename="Scrooge", surname="McDuck"
    )

    database.session.add(owner)
    database.session.commit()

    user_role = UserRole(userId=owner.id, roleId=ownerRole.id)

    database.session.add(user_role)
    database.session.commit()
