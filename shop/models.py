from flask_sqlalchemy import SQLAlchemy

database = SQLAlchemy()


class ProductCategory(database.Model):
    __tablename__ = "productcategory"
    id = database.Column(database.Integer, primary_key=True)
    productID = database.Column(database.Integer, database.ForeignKey("products.id", ondelete="CASCADE"),
                                nullable=False)
    categoryID = database.Column(database.Integer, database.ForeignKey("categories.id", ondelete="CASCADE"),
                                 nullable=False)

    def __repr__(self):
        return "(PRODUCTCATEGORY {}, {}, {})".format(self.id, self.productID, self.categoryID)


class ProductOrder(database.Model):
    __tablename__ = "productorder"
    id = database.Column(database.Integer, primary_key=True)
    orderID = database.Column(database.Integer, database.ForeignKey("orders.id", ondelete="CASCADE"), nullable=False)
    productID = database.Column(database.Integer, database.ForeignKey("products.id", ondelete="CASCADE"),
                                nullable=False)
    price = database.Column(database.Float, nullable=False)
    quantity = database.Column(database.Integer, nullable=False)

    def __repr__(self):
        return "(PRODUCTORDER {}, {}, {}, {}, {}, {})".format(self.id, self.orderID, self.productID, self.price,
                                                              self.received, self.requested)


class Category(database.Model):
    __tablename__ = "categories"
    id = database.Column(database.Integer, primary_key=True)
    name = database.Column(database.String(256), nullable=False, unique=True)
    products = database.relationship("Product", secondary=ProductCategory.__tablename__, back_populates="categories")

    def __repr__(self):
        return "(CATEGORY {}, {})".format(self.id, self.name)


class Product(database.Model):
    __tablename__ = "products"
    id = database.Column(database.Integer, primary_key=True)
    name = database.Column(database.String(256), nullable=False)
    price = database.Column(database.Float, nullable=False)
    categories = database.relationship("Category", secondary=ProductCategory.__tablename__, back_populates="products")
    orders = database.relationship("Order", secondary=ProductOrder.__tablename__, back_populates="products")

    def __repr__(self):
        return "(PRODUCT {}, {}, {}, {})".format(self.id, self.name, self.price, self.number)


class OrderStatus(database.Model):
    __tablename__ = "orderstatus"
    id = database.Column(database.Integer, primary_key=True)
    orderID = database.Column(database.Integer,
                              database.ForeignKey("orders.id", onupdate="CASCADE", ondelete="CASCADE"), nullable=False)
    statusID = database.Column(database.Integer,
                               database.ForeignKey("status.id", onupdate="CASCADE", ondelete="CASCADE"), nullable=False)

    def __repr__(self):
        return "(ORDERSTATUS {}, {}, {})".format(self.id, self.orderID, self.statusID)


class Status(database.Model):
    __tablename__ = "status"
    id = database.Column(database.Integer, primary_key=True)
    name = database.Column(database.String(256), nullable=False, unique=True)
    orders = database.relationship("Order", secondary=OrderStatus.__tablename__, back_populates="status")

    def __repr__(self):
        return "(STATUS {}, {})".format(self.id, self.name)


class Order(database.Model):
    __tablename__ = "orders"
    id = database.Column(database.Integer, primary_key=True)
    price = database.Column(database.Float, nullable=False)
    time = database.Column(database.TIMESTAMP, nullable=False)
    email = database.Column(database.String(256), nullable=False)
    status = database.relationship("Status", secondary=OrderStatus.__tablename__, back_populates="orders")
    products = database.relationship("Product", secondary=ProductOrder.__tablename__, back_populates="orders")

    def __repr__(self):
        return "(ORDER {}, {}, {}, {})".format(self.id, self.price, self.time, self.email)
