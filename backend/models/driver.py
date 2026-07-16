from database.db import db


class Driver(db.Model):

    __tablename__ = "drivers"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey(
            "users.id",
            ondelete="CASCADE"
        ),
        nullable=False,
        unique=True
    )

    vehicle_type = db.Column(
        db.String(50),
        nullable=False
    )

    vehicle_number = db.Column(
        db.String(25),
        nullable=False,
        unique=True
    )

    phone = db.Column(
        db.String(15),
        nullable=False
    )

    available = db.Column(
        db.Boolean,
        default=True
    )

    current_latitude = db.Column(
        db.Float,
        default=0.0
    )

    current_longitude = db.Column(
        db.Float,
        default=0.0
    )

    deliveries = db.relationship(
        "Delivery",
        backref="driver",
        lazy=True,
        cascade="all, delete"
    )

    def to_dict(self):

        return {

            "id": self.id,

            "user_id": self.user_id,

            "vehicle_type": self.vehicle_type,

            "vehicle_number": self.vehicle_number,

            "phone": self.phone,

            "available": self.available,

            "latitude": self.current_latitude,

            "longitude": self.current_longitude

        }