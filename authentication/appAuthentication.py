import re
from operator import and_

from flask import Flask, request, Response, jsonify
from flask_jwt_extended import JWTManager
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt, get_jwt_identity

from configuration import Configuration
from models import User, UserRole, database, Role
from decoraterRole import roleCheck

app = Flask(__name__)
app.config.from_object(Configuration)


@app.route("/register_customer", methods=["POST"])
def register_customer():
    email = request.json.get("email", "")
    password = request.json.get("password", "")
    forename = request.json.get("forename", "")
    surname = request.json.get("surname", "")

    emailEmpty = len(email) == 0
    passwordEmpty = len(password) == 0
    forenameEmpty = len(forename) == 0
    surnameEmpty = len(surname) == 0

    emptyField = ""

    # check for empty field
    if passwordEmpty:
        emptyField = "password"
    if emailEmpty:
        emptyField = "email"
    if surnameEmpty:
        emptyField = "surname"
    if forenameEmpty:
        emptyField = "forename"
    if len(emptyField) != 0:
        return jsonify(message=f"Field {emptyField} is missing."), 400

    # email valid check
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    if not re.fullmatch(regex, email):
        return jsonify(message="Invalid email."), 400

    # password check
    # if len(password) < 8 or not any(char.isdigit() for char in password) or password.islower() or password.isupper():
    if len(password) < 8:
        return jsonify(message="Invalid password."), 400

    # email existing check
    emailExist = User.query.filter(User.email == email).first()
    if emailExist:
        return jsonify(message="Email already exists."), 400

    user = User(forename=forename, surname=surname, email=email, password=password)
    database.session.add(user)
    database.session.commit()

    role = Role.query.filter(Role.name == "customer").first()
    if role is None:
        role = Role(name="courier")
        database.session.add(role)
        database.session.commit()
    userRole = UserRole(userId=user.id, roleId=role.id)

    database.session.add(userRole)
    database.session.commit()

    return Response(status=200)


@app.route("/register_courier", methods=["POST"])
def register_courier():
    email = request.json.get("email", "")
    password = request.json.get("password", "")
    forename = request.json.get("forename", "")
    surname = request.json.get("surname", "")
    # buyer = request.json.get("isCustomer", "")

    emailEmpty = len(email) == 0
    passwordEmpty = len(password) == 0
    forenameEmpty = len(forename) == 0
    surnameEmpty = len(surname) == 0

    emptyField = ""

    # check for empty field
    if passwordEmpty:
        emptyField = "password"
    if emailEmpty:
        emptyField = "email"
    if surnameEmpty:
        emptyField = "surname"
    if forenameEmpty:
        emptyField = "forename"
    if len(emptyField) != 0:
        return jsonify(message=f"Field {emptyField} is missing."), 400

    # email valid check
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    if not re.fullmatch(regex, email):
        return jsonify(message="Invalid email."), 400

    # password check
    if len(password) < 8:
        return jsonify(message="Invalid password."), 400

    # email existing check
    emailExist = User.query.filter(User.email == email).first()
    if emailExist:
        return jsonify(message="Email already exists."), 400

    user = User(forename=forename, surname=surname, email=email, password=password)
    database.session.add(user)
    database.session.commit()

    role = Role.query.filter(Role.name == "courier").first()
    if role is None:
        role = Role(name="courier")
        database.session.add(role)
        database.session.commit()
    userRole = UserRole(userId=user.id, roleId=role.id)

    database.session.add(userRole)
    database.session.commit()

    return Response(status=200)


jwt = JWTManager(app)


@app.route("/login", methods=["POST"])
def login():
    email = request.json.get("email", "")
    password = request.json.get("password", "")

    emailEmpty = len(email) == 0
    passwordEmpty = len(password) == 0
    emptyField = ""

    if passwordEmpty:
        emptyField = "password"
    if emailEmpty:
        emptyField = "email"
    if len(emptyField) != 0:
        return jsonify(message=f"Field {emptyField} is missing."), 400

    # email valid check
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    if not re.fullmatch(regex, email):
        return jsonify(message="Invalid email."), 400

    # password correct check
    result = User.query.filter(and_(User.email == email, User.password == password)).first()
    if not result:
        return jsonify(message="Invalid credentials."), 400

    additionalInf = {"forename": result.forename,
                     "surname": result.surname,
                     "roles": [str(role.name) for role in result.roles]
                     }

    accessToken = create_access_token(identity=email, additional_claims=additionalInf)
    refreshToken = create_refresh_token(identity=email, additional_claims=additionalInf)
    return jsonify(accessToken=accessToken, refreshToken=refreshToken)


@app.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    identity = get_jwt_identity()
    payload = get_jwt()

    additionalClaims = {
        "forename": payload["forename"],
        "password": payload["password"],
        "roles": payload["roles"]
    }

    accessToken = create_access_token(identity=identity, additional_claims=additionalClaims)
    return jsonify(accessToken=accessToken), 200


@app.route("/delete", methods=["POST"])
@roleCheck("owner,courier,customer")
def delete():
    email = get_jwt_identity()

    userToDelete = User.query.filter(User.email == email).first()
    if userToDelete:
        User.query.filter(User.email == email).delete()
        database.session.commit()
        return Response(status=200)
    return jsonify({"message": "Unknown user."}), 400


@app.route("/", methods=["GET"])
def index():
    return "<h1>Authentication</h1>"


if __name__ == "__main__":
    database.init_app(app)
    app.run(debug=True, host="0.0.0.0", port=5002)
