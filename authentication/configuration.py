import os
from datetime import timedelta

databaseURL = "localhost:3307"


# databaseURL = os.environ["DATABASE_URL"]

class Configuration:
    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://root:root@{databaseURL}/authenticationDatabase"
    JWT_SECRET_KEY = "JWT_SECRET_DEV_KEY"
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)
    # JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=365)
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=60)
    # JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=365)

    SQLALCHEMY_TRACK_MODIFICATIONS = False
