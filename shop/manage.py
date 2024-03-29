from flask import Flask
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from models import database
from sqlalchemy_utils import database_exists, create_database
from configuration import Configuration

app = Flask(__name__)
app.config.from_object(Configuration)

migrate = Migrate(app, database)

manager = Manager(app)
manager.add_command("db", MigrateCommand)

if __name__ == '__main__':
    database.init_app(app)
    if not database_exists(Configuration.SQLALCHEMY_DATABASE_URI):
        create_database(Configuration.SQLALCHEMY_DATABASE_URI)
    manager.run()
