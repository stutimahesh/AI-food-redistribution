from database.db import db


class Donation(db.Model):

    __tablename__ = "donations"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    donor_id = db.Column(
        db.Integer,
        db.ForeignKey("donors.id", ondelete="CASCADE"),
        nullable=False
    )

    food_name = db.Column(
        db.String(100),
        nullable=False
    )

    food_type = db.Column(
        db.String(50),
        nullable=False
    )

    quantity = db.Column(
        db.Integer,
        nullable=False
    )

    cooked_time = db.Column(
        db.DateTime,
        nullable=False
    )

    expiry_time = db.Column(
        db.DateTime,
        nullable=False
    )

    pickup_address = db.Column(
        db.Text,
        nullable=False
    )

    latitude = db.Column(
        db.Float,
        nullable=False
    )

    longitude = db.Column(
        db.Float,
        nullable=False
    )

    status = db.Column(
        db.String(30),
        default="Pending"
    )

    created_at = db.Column(
        db.DateTime,
        server_default=db.func.now()
    )

    recommendations = db.relationship(
        "Recommendation",
        backref="donation",
        cascade="all, delete",
        lazy=True
    )

    deliveries = db.relationship(
        "Delivery",
        backref="donation",
        cascade="all, delete",
        lazy=True
    )

    def to_dict(self):

        return {

            "id": self.id,

            "donor_id": self.donor_id,

            "food_name": self.food_name,

            "food_type": self.food_type,

            "quantity": self.quantity,

            "cooked_time": self.cooked_time,

            "expiry_time": self.expiry_time,

            "pickup_address": self.pickup_address,

            "latitude": self.latitude,

            "longitude": self.longitude,

            "status": self.status,

            "created_at": self.created_at

        }