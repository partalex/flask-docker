from configuration import Configuration
from sqlalchemy_utils import database_exists
from models import database, UserRole, User, Role
from flask import Flask


def generateRelation(database):
    rola1 = Role(name="owner")
    rola2 = Role(name="kupac")
    rola3 = Role(name="magacioner")
    admin = User(email="owner@owner.com", password="1", forename="owner", surname="owner")
    relation = UserRole(userID=1, roleID=1)
    database.session.add(rola1)
    database.session.add(rola2)
    database.session.add(rola3)
    database.session.add(admin)
    database.session.commit()
    database.session.add(relation)
    database.session.commit()


application = Flask(__name__)
application.config.from_object(Configuration)

while True:
    if not database_exists(Configuration.SQLALCHEMY_DATABASE_URI):
        print("Database does not exists!")
        break
    else:
        database.init_app(application)
        with application.app_context() as contex:
            generateRelation(database)
            print("Role and Admin added.")
    break
