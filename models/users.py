from main import db

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(), nullable=False, unique=True)
    password = db.Column(db.String(), nullable=False)
    admin = db.Column(db.Boolean(), default=False)
    # Establish the relationship with card model
    cards = db.relationship(
        "Card",
        back_populates="user",
        cascade="all, delete"
    )