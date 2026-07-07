from database.db import db


class Recommendation(db.Model):

    __tablename__ = "recommendations"

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

    ngo_id = db.Column(
        db.Integer,
        db.ForeignKey(
            "ngos.id",
            ondelete="CASCADE"
        ),
        nullable=False
    )

    score = db.Column(
        db.Float,
        nullable=False
    )

    acceptance_probability = db.Column(
        db.Float,
        default=0.0
    )

    distance = db.Column(
        db.Float,
        default=0.0
    )

    eta = db.Column(
        db.Integer,
        default=0
    )

    created_at = db.Column(
        db.DateTime,
        server_default=db.func.now()
    )

    def to_dict(self):

        return {

            "id": self.id,

            "donation_id": self.donation_id,

            "ngo_id": self.ngo_id,

            "score": self.score,

            "acceptance_probability":
            self.acceptance_probability,

            "distance": self.distance,

            "eta": self.eta,

            "created_at": self.created_at

        }