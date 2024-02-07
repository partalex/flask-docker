import json

from flask import Flask, Response, request
from flask_jwt_extended import JWTManager, get_jwt_identity
from sqlalchemy import and_, func, desc, select, alias, join

from configuration import Configuration
from decoraterRole import roleCheck
from models import database, Order, OrderStatus, Status, ProductOrder, ProductCategory, Category, Product

app = Flask(__name__)
app.config.from_object(Configuration)
jwt = JWTManager(app)


@app.route("/money", methods=["GET"])
def getMoney():
    return Response(json.dumps({}))


if __name__ == "__main__":
    database.init_app(app)
    app.run(debug=True, host="0.0.0.0", port=5004)
