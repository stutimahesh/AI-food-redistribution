from database.db import db


class Delivery(db.Model):

    __tablename__ = "deliveries"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    donation_id = db.Column(
        db.Integer,
        db.ForeignKey(
            "donations.id",
            ondelete="CASCADE"
        ),
        nullable=False
    )

    driver_id = db.Column(
        db.Integer,
        db.ForeignKey(
            "drivers.id",
            ondelete="CASCADE"
        ),
        nullable=False
    )

    ngo_id = db.Column(
        db.Integer,
        db.ForeignKey(
            "ngos.id",
            ondelete="CASCADE"
        ),
        nullable=False
    )

    pickup_time = db.Column(
        db.DateTime
    )

    delivered_time = db.Column(
        db.DateTime
    )

    delivery_status = db.Column(

        db.String(30),

        default="Assigned"
    )

    estimated_distance = db.Column(
        db.Float,
        default=0.0
    )

    estimated_eta = db.Column(
        db.Integer,
        default=0
    )

    actual_distance = db.Column(
        db.Float,
        default=0.0
    )

    actual_duration = db.Column(
        db.Integer,
        default=0
    )

    route_polyline = db.Column(
        db.Text
    )

    created_at = db.Column(
        db.DateTime,
        server_default=db.func.now()
    )

    def to_dict(self):

        return {

            "id": self.id,

            "donation_id": self.donation_id,

            "driver_id": self.driver_id,

            "ngo_id": self.ngo_id,

            "pickup_time": self.pickup_time,

            "delivered_time": self.delivered_time,

            "delivery_status": self.delivery_status,

            "estimated_distance": self.estimated_distance,

            "estimated_eta": self.estimated_eta,

            "actual_distance": self.actual_distance,

            "actual_duration": self.actual_duration,

            "route_polyline": self.route_polyline,

            "created_at": self.created_at

        }