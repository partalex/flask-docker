import datetime
import json

from flask import Flask, request, Response, jsonify
from flask_jwt_extended import JWTManager, get_jwt_identity
from models import Product, Category, ProductCategory, Order, OrderStatus, ProductOrder, database, Status
from sqlalchemy import and_

from decoraterRole import roleCheck
from configuration import Configuration

# from pprint import pprint

app = Flask(__name__)
app.config.from_object(Configuration)
jwt = JWTManager(app)


@app.route("/search", methods=["GET"])
@roleCheck(role="customer")
def search():
    name = request.args.get("name")
    category = request.args.get("category")

    products = []
    categories = []
    if name and category:
        products = Product.query.join(ProductCategory).join(Category).filter(
            and_(Category.name.like(f"%{category}%"), Product.name.like(f"%{name}%")))
    elif name and category is None:
        products = Product.query.filter(Product.name.like(f"%{name}%"))
    elif name is None and category:
        products = Product.query.join(ProductCategory).join(Category).filter(Category.name.like(f"%{category}%"))
    else:
        products = Product.query.all()

    searchProducts = []
    for product in products:
        productCategories = []
        for productCat in product.categories:
            productCategories.append(productCat.name)
            if productCat.name not in categories:
                categories.append(productCat.name)
        searchProducts.append({
            "categories": productCategories,
            "id": product.id,
            "name": product.name,
            "price": product.price
        })
    return Response(json.dumps({"categories": categories, "products": searchProducts}), status=200)


@app.route("/order", methods=["POST"])
@roleCheck(role="customer")
def order():
    requests = request.json.get("requests", "")

    if len(requests) == 0:
        return Response(json.dumps({"message": "Field requests is missing."}), status=400)

    cnt = 0
    for r in requests:
        id = r.get("id", "")
        if id == "":
            return Response(json.dumps({"message": f"Product id is missing for request number {cnt}."}), status=400)
        number = r.get("quantity", "")
        if number == "":
            return Response(json.dumps({"message": f"Product quantity is missing for request number {cnt}."}),
                            status=400)
        try:
            id = int(id)
        except ValueError:
            return Response(json.dumps({"message": f"Invalid product id for request number {cnt}."}), status=400)
        if id < 0:
            return Response(json.dumps({"message": f"Invalid product id for request number {cnt}."}), status=400)
        try:
            number = int(number)
        except ValueError:
            return Response(json.dumps({"message": f"Invalid product quantity for request number {cnt}."}), status=400)
        if number <= 0:
            return Response(json.dumps({"message": f"Invalid product quantity for request number {cnt}."}), status=400)

        product = Product.query.filter(Product.id == id).first()
        if product is None:
            return Response(json.dumps({"message": f"Invalid product for request number {cnt}."}), status=400)
        cnt += 1

    order = Order(price=0, time=datetime.datetime.now().isoformat(), email=get_jwt_identity())
    database.session.add(order)
    # database.session.commit()
    database.session.flush()
    database.session.refresh(order)
    statusCreatedId = Status.query.filter(Status.name == "CREATED").first().id
    orderStatus = OrderStatus(orderID=order.id, statusID=statusCreatedId)
    database.session.add(orderStatus)
    # database.session.commit()
    database.session.flush()
    database.session.refresh(orderStatus)

    for r in requests:
        product = Product.query.filter(Product.id == r['id']).first()
        order.price += float(product.price) * float(r['quantity'])
        productOrder = ProductOrder(productID=r["id"], orderID=order.id, price=product.price, quantity=r['quantity'])

        database.session.add(productOrder)
        database.session.flush()
        database.session.refresh(productOrder)
        # database.session.commit()

    database.session.commit()

    return Response(json.dumps({"id": order.id}), status=200)


@app.route("/status", methods=["GET"])
@roleCheck(role="customer")
def status():
    user = get_jwt_identity()
    orders = Order.query.filter(Order.email == user).all()

    ordersResult = []
    for order in orders:
        productsResult = []
        for product in order.products:
            categoriesResult = []
            for category in product.categories:
                categoriesResult.append(category.name)
            productOrder = ProductOrder.query.join(Order).filter(
                and_(Order.id == order.id, ProductOrder.productID == product.id)).first()
            productsResult.append({
                "categories": categoriesResult,
                "name": product.name,
                "price": productOrder.price,
                "quantity": productOrder.quantity
            })
        orderStatus = OrderStatus.query.filter(OrderStatus.orderID == order.id).first()
        ordersResult.append({
            "products": productsResult,
            "price": order.price,
            "status": Status.query.filter(Status.id == orderStatus.statusID).first().name,
            "timestamp": str(order.time)
        })
    return jsonify(orders=ordersResult)


@app.route("/delivered", methods=["POST"])
@roleCheck(role="customer")
def delivered():
    orderId = request.json.get("id")
    if orderId is None:
        return Response(json.dumps({'message': 'Missing order id.'}), status=400)
    try:
        orderId = int(orderId)
        if orderId < 0:
            raise ValueError
        if Order.query.filter(Order.id == orderId).first() is None:
            raise ValueError
    except ValueError:
        return Response(json.dumps({'message': 'Invalid order id.'}), status=400)
    finally:
        pass

    keys = request.json.get("keys")
    passphrase = request.json.get("passphrase")

    orderStatus = OrderStatus.query.filter(OrderStatus.orderID == orderId).first()
    statusPendingId = Status.query.filter(Status.name == "PENDING").first().id

    if orderStatus.statusID != statusPendingId:
        return Response(json.dumps({'message': 'Invalid order id.'}), status=400)

    statusComplete = Status.query.filter(Status.name == "COMPLETE").first()
    orderStatus.statusID = statusComplete.id
    database.session.commit()

    return Response(status=200)


if __name__ == "__main__":
    database.init_app(app)
    app.run(debug=True, host="0.0.0.0", port=5004)
