from datetime import timedelta
import os

databaseUrl = os.environ["DATABASE_URL"]
# databaseUrl = "localhost"


class Configuration:
    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://root:root@{databaseUrl}/storeDb"
    # JWT_SECRET_KEY = "JWT_SECRET_KEY"
    JWT_SECRET_KEY = "JWT_SECRET_DEV_KEY"
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(seconds=3600)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)

    SQLALCHEMY_TRACK_MODIFICATIONS = False

