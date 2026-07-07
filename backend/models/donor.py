from database.db import db


class Donor(db.Model):

    __tablename__ = "donors"

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

    organization_name = db.Column(
        db.String(150),
        nullable=False
    )

    address = db.Column(
        db.Text
    )

    latitude = db.Column(
        db.Float
    )

    longitude = db.Column(
        db.Float
    )

    # Relationship
    donations = db.relationship(
        "Donation",
        backref="donor",
        lazy=True,
        cascade="all, delete"
    )

    def to_dict(self):

        return {

            "id": self.id,

            "user_id": self.user_id,

            "organization_name": self.organization_name,

            "address": self.address,

            "latitude": self.latitude,

            "longitude": self.longitude

        }