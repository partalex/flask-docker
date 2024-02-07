import json

from flask import Flask, Response, request
from flask_jwt_extended import JWTManager, get_jwt_identity
from sqlalchemy import and_

from configuration import Configuration
from decoraterRole import roleCheck
from models import database, Order, OrderStatus, Status

app = Flask(__name__)
app.config.from_object(Configuration)
jwt = JWTManager(app)


@app.route("/orders_to_deliver", methods=["GET"])
@roleCheck("courier")
def orders_to_deliver():
    user = get_jwt_identity()
    # orders = Order.query.filter(Order.email == user).all()

    statusCreatedId = Status.query.filter(Status.name == "CREATED").first().id
    ordersCreated = OrderStatus.query.filter(OrderStatus.statusID == statusCreatedId).all()

    allOrders = {"orders": []}
    for order in ordersCreated:
        orderData = {
            "id": order.orderID,
            "email": Order.query.filter(Order.id == order.orderID).first().email,
        }
        allOrders["orders"].append(orderData)
    return Response(json.dumps(allOrders), status=200)


@app.route("/pick_up_order", methods=["POST"])
@roleCheck("courier")
def pick_up_order():
    orderId = request.json.get("id")
    if orderId is None:
        return Response(json.dumps({'message': 'Missing order id.'}), status=400)
    try:
        orderId = int(orderId)
    except ValueError:
        return Response(json.dumps({'message': 'Invalid order id.'}), status=400)
    finally:
        pass

    if orderId < 0:
        return Response(json.dumps({'message': 'Invalid order id.'}), status=400)

    orderToPickup = Order.query.filter(Order.id == orderId).first()
    if orderToPickup is None:
        return Response(json.dumps({'message': 'Invalid order id.'}), status=400)

    address = request.json.get("address")
    if Exception is None:
        return Response(json.dumps({'message': 'Missing address.'}), status=400)

    orderStatus = OrderStatus.query.filter(OrderStatus.orderID == orderId).first()

    statusCreatedId = Status.query.filter(Status.name == "CREATED").first().id
    if orderStatus.statusID != statusCreatedId:
        return Response(json.dumps({'message': 'Invalid order id.'}), status=400)

    statusPending = Status.query.filter(Status.name == "PENDING").first()
    orderStatus.statusID = statusPending.id

    database.session.commit()
    return Response(status=200)


if __name__ == "__main__":
    database.init_app(app)
    app.run(debug=True, host="0.0.0.0", port=5003)
