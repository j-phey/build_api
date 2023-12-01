from main import db

class Card(db.Model):
    # define the table name for the db
    __tablename__= "cards"
    # Set the primary key, we need to define that each attribute is also a column in the db table, remember "db" is the object we created in the previous step.
    id = db.Column(db.Integer,primary_key=True)
    # Add the rest of the attributes. 
    title = db.Column(db.String())
    description = db.Column(db.String())
    date = db.Column(db.Date())
    status = db.Column(db.String())
    priority = db.Column(db.String())
    # Add the user_id column as a foreign key in the Card model
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False) # nullable=False - card can't exist without an author
    # Establish the relationship with users model
    user = db.relationship(
        "User",
        back_populates="cards"
    )
    # Establish the relationship with comments model
    comments = db.relationship(
        "Comment",
        back_populates="card",
        cascade="all, delete"
    )