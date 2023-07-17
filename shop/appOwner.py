import json
import io
import csv

from flask import Flask, Response, request
from flask_jwt_extended import JWTManager
from sqlalchemy import func, and_

from decoraterRole import roleCheck
from configuration import Configuration
from models import database, Product, ProductOrder, Category, ProductCategory, OrderStatus, Status

app = Flask(__name__)
app.config.from_object(Configuration)
jwt = JWTManager(app)


@app.route("/update", methods=["POST"])
@roleCheck("owner")
def update():
    if not request.files.get("file", None):
        return Response(json.dumps({"message": "Field file is missing."}), status=400)
    content = request.files["file"].stream.read().decode("utf-8")
    stream = io.StringIO(content)
    reader = csv.reader(stream)

    products = []
    cnt = 0
    for row in reader:
        if len(row) != 3:
            return Response(json.dumps({"message": f"Incorrect number of values on line {cnt}."}), status=400)
        try:
            categories = row[0].split('|')
        except ValueError:
            return Response(json.dumps({"message": f"Incorrect quantity on line {cnt}."}), status=400)
        try:
            name = row[1]
        except ValueError:
            return Response(json.dumps({"message": f"Incorrect quantity on line {cnt}."}), status=400)
        try:
            price = float(row[2])
            if price < 0:
                raise ValueError
        except ValueError:
            return Response(json.dumps({"message": f"Incorrect price on line {cnt}."}), status=400)

        cnt += 1

        newProduct = Product.query.filter(Product.name == name).first()

        # update product
        if newProduct:
            return Response(json.dumps({"message": f"Product {name} already exists."}), status=400)

            # categoriesExist = [cat.name for cat in product.categories]
            # isDifferent = False
            # for categoryName in categories:
            #     if categoryName in categoriesExist:
            #         continue
            #     isDifferent = True
            #     break
            # # ne obradjuje se!
            # if isDifferent:
            #     continue
            # product.number += 1
        else:
            products.append({
                "categories": categories,
                "name": name,
                "price": price
            })

    for product in products:
        newProduct = Product(name=product['name'], price=product['price'])
        database.session.add(newProduct)
        database.session.commit()

        categoriesId = []
        productCategories = []
        productId = Product.query.filter(Product.name == product['name']).first().id

        for categoryName in product['categories']:
            category = Category.query.filter(Category.name == categoryName).first()
            if category:
                pass
            else:
                category = Category(name=categoryName)
                database.session.add(category)
                database.session.commit()
            categoriesId.append(category.id)

        for categoryId in categoriesId:
            productCategory = ProductCategory(productID=productId, categoryID=categoryId)
            productCategories.append(productCategory)

        database.session.add_all(productCategories)
        database.session.commit()

    return Response(status=200)


@app.route("/product_statistics", methods=["GET"])
@roleCheck("owner")
def product_statistics():
    statistics = []

    productsStatusComplete = database.session.query(
        Product.name,
        Status.name,
        func.sum(ProductOrder.quantity)
    ).filter(
        and_(
            ProductOrder.productID == Product.id,
            ProductOrder.orderID == OrderStatus.orderID,
            Status.id == OrderStatus.statusID,
            Status.name == "COMPLETE"
        )
    ).group_by(
        Product.name,
        Status.name,
    ).all()

    productsNotStatusComplete = database.session.query(
        Product.name,
        Status.name,
        func.sum(ProductOrder.quantity)
    ).filter(
        and_(
            ProductOrder.productID == Product.id,
            ProductOrder.orderID == OrderStatus.orderID,
            Status.id == OrderStatus.statusID,
            Status.name != "COMPLETE"
        )
    ).group_by(
        Product.name,
        Status.name,
    ).all()

    productDict = {}

    for product in productsStatusComplete:
        productDict[product[0]] = {"sold": 0, "waiting": 0}
        productDict[product[0]]["sold"] += product[2]

    for product in productsNotStatusComplete:
        productDict[product[0]]["waiting"] += product[2]

    for product in productDict:
        statistics.append({
            "name": product,
            "sold": int(productDict[product]["sold"]),
            "waiting": int(productDict[product]["waiting"])
        })

    return Response(json.dumps({"statistics": statistics}), status=200)


@app.route("/category_statistics", methods=["GET"])
@roleCheck("owner")
def category_statistics():
    statistics = []

    totalQunatity = func.coalesce(func.sum(ProductOrder.quantity), 0)
    categories = Category.query.outerjoin(ProductCategory, Category.id == ProductCategory.categoryID).outerjoin(
        ProductOrder, ProductCategory.productID == ProductOrder.productID).group_by(Category.id).order_by(
        totalQunatity.desc()).order_by(Category.name).with_entities(Category.name).all()

    for category in categories:
        statistics.append(category[0])
    return Response(json.dumps({"statistics": statistics}), status=200)


@app.route("/modification", methods=["GET"])
@roleCheck("owner")
def modification():
    statistics = []

    productOrders = Category.query.outerjoin(ProductCategory, Category.id == ProductCategory.categoryID).outerjoin(
        ProductOrder, ProductCategory.productID == ProductOrder.productID).group_by(Category.id).with_entities(
        Category.name, func.coalesce(func.sum(ProductOrder.requested) - func.sum(ProductOrder.received), 0)).all()

    for product in productOrders:
        statistics.append({
            "name": product[0],
            "waiting": int(product[1])
        })

    return Response(json.dumps({"statistics": statistics}), status=200)


if __name__ == "__main__":
    database.init_app(app)
    app.run(debug=True, host="0.0.0.0", port=5005)
