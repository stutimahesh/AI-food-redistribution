from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)

from database.db import db


class User(db.Model):

    __tablename__ = "users"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    full_name = db.Column(
        db.String(100),
        nullable=False
    )

    email = db.Column(
        db.String(100),
        unique=True,
        nullable=False
    )

    password = db.Column(
        db.String(255),
        nullable=False
    )

    phone = db.Column(
        db.String(15)
    )

    role = db.Column(
        db.String(20),
        nullable=False
    )

    created_at = db.Column(
        db.DateTime,
        server_default=db.func.now()
    )

    # ------------------------

    def set_password(self, password):
        self.password = generate_password_hash(password)

    # ------------------------

    def check_password(self, password):
        return check_password_hash(
            self.password,
            password
        )

    # ------------------------

    def to_dict(self):

        return {

            "id": self.id,

            "full_name": self.full_name,

            "email": self.email,

            "phone": self.phone,

            "role": self.role,

            "created_at": self.created_at
        }