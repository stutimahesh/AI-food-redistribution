from database.db import db


class NGO(db.Model):

    __tablename__ = "ngos"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id", ondelete="CASCADE"),
        unique=True,
        nullable=False
    )

    ngo_name = db.Column(
        db.String(150),
        nullable=False
    )

    address = db.Column(
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

    max_capacity = db.Column(
        db.Integer,
        nullable=False
    )

    current_capacity = db.Column(
        db.Integer,
        default=0
    )

    active = db.Column(
        db.Boolean,
        default=True
    )

    recommendations = db.relationship(
        "Recommendation",
        backref="ngo",
        cascade="all, delete",
        lazy=True
    )

    deliveries = db.relationship(
        "Delivery",
        backref="ngo",
        cascade="all, delete",
        lazy=True
    )

    @property
    def remaining_capacity(self):

        return max(
            self.max_capacity - self.current_capacity,
            0
        )

    def to_dict(self):

        return {

            "id": self.id,

            "user_id": self.user_id,

            "ngo_name": self.ngo_name,

            "address": self.address,

            "latitude": self.latitude,

            "longitude": self.longitude,

            "max_capacity": self.max_capacity,

            "current_capacity": self.current_capacity,

            "remaining_capacity": self.remaining_capacity,

            "active": self.active

        }