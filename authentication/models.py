from flask_sqlalchemy import SQLAlchemy

database = SQLAlchemy()


class UserRole(database.Model):
    __tablename__ = "userrole"

    id = database.Column(database.Integer, primary_key=True)

    # Relation
    userId = database.Column(database.Integer, database.ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    roleId = database.Column(database.Integer, database.ForeignKey("roles.id", ondelete="CASCADE"), nullable=False)

    def __repr__(self):
        return "UserRole: id:{}, userId:{}, roleId:{}]".format(self.id, self.userId, self.roleId)


class User(database.Model):
    __tablename__ = "users"
    id = database.Column(database.Integer, primary_key=True)
    forename = database.Column(database.String(256), nullable=False)
    surname = database.Column(database.String(256), nullable=False)
    email = database.Column(database.String(256), unique=True, nullable=False)
    password = database.Column(database.String(256), nullable=False)

    # Relation
    roles = database.relationship("Role", secondary=UserRole.__table__, cascade="all, delete", back_populates="users")

    def __repr__(self):
        return "User : id:{}, forename:{}, surname:{}, email:{}, password:{}, isCustomer:{}, roles:[{}]]". \
            format(self.id, self.forename, self.surname, self.email, self.password, self.isCustomer, self.roles)


class Role(database.Model):
    __tablename__ = "roles"

    id = database.Column(database.Integer, primary_key=True)
    name = database.Column(database.String(256), unique=True, nullable=False)

    # Relation
    users = database.relationship("User", secondary=UserRole.__table__, cascade="all, delete", back_populates="roles")

    def __repr__(self):
        return "Role: id:{}, name:{}".format(self.id, self.name)
