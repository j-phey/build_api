from flask import Blueprint, jsonify, request, abort
from main import db
from models.cards import Card
from models.users import User
from schemas.card_schema import card_schema, cards_schema
from datetime import date
from flask_jwt_extended import jwt_required, get_jwt_identity

cards = Blueprint('cards', __name__, url_prefix="/cards")

# The GET all cards route endpoint
@cards.route("/", methods=["GET"])
def get_cards():
    # get all the cards from the database table
    stmt = db.select(Card)
    cards_list = db.session.scalars(stmt)
    # Convert the cards from the database into a JSON format and store them in result
    result = cards_schema.dump(cards_list)
    # return the data in JSON format
    return jsonify(result)

# The GET a single card route endpoint - /cards/<id>
@cards.route("/<int:id>/", methods=["GET"])
def get_card(id):
    stmt = db.select(Card).filter_by(id=id)
    card = db.session.scalar(stmt)
    #return an error if the card doesn't exist
    if not card:
        return abort(400, description= "Card does not exist")
    # Convert the cards from the database into a JSON format and store them in result
    result = card_schema.dump(card)
    # return the data in JSON format
    return jsonify(result)


# The create card POST route endpoint
@cards.route("/", methods=["POST"])
@jwt_required()
def create_card():
    # #Create a new card
    card_fields = card_schema.load(request.json)

    new_card = Card()
    new_card.title = card_fields["title"]
    new_card.description = card_fields["description"]
    new_card.status = card_fields["status"]
    new_card.priority = card_fields["priority"]
    # not taken from the request, generated by the server
    new_card.date = date.today()
    # add to the database and commit
    db.session.add(new_card)
    db.session.commit()
    #return the card in the response
    return jsonify(card_schema.dump(new_card))

# The PUT route endpoint for updating a card
# The update card needs to authenticate the admin user, 
# find the card by id first (same as the delete_card method), 
# and if the card exists it will be updated with the information included in the request.

@cards.route("/<int:id>/", methods=["PUT"])
@jwt_required()
def update_card(id):
    # #Create a new card
    card_fields = card_schema.load(request.json)

    #get the user id invoking get_jwt_identity
    user_id = get_jwt_identity()
    #Find it in the db
    stmt = db.select(User).filter_by(id=user_id)
    user = db.session.scalar(stmt)
    #Make sure it is in the database
    if not user:
        return abort(401, description="Invalid user")
    # Stop the request if the user is not an admin
    if not user.admin:
        return abort(401, description="Unauthorised user")
    # find the card
    stmt = db.select(Card).filter_by(id=id)
    card = db.session.scalar(stmt)
    #return an error if the card doesn't exist
    if not card:
        return abort(400, description= "Card does not exist")
    #update the car details with the given values
    card.title = card_fields["title"]
    card.description = card_fields["description"]
    card.status = card_fields["status"]
    card.priority = card_fields["priority"]
    # not taken from the request, generated by the server
    card.date = date.today()
    # add to the database and commit
    db.session.commit()
    #return the card in the response
    return jsonify(card_schema.dump(card))

# Finally, we round out our CRUD resource with a DELETE card method 
@cards.route("/<int:id>/", methods=["DELETE"])
@jwt_required()
def delete_card(id):
    # #get the user id invoking get_jwt_identity
    user_id = get_jwt_identity()
    # #Find the user in the db
    stmt = db.select(User).filter_by(id=user_id)
    user = db.session.scalar(stmt)
    # #Make sure it is in the database
    if not user:
        return abort(401, description="Invalid user")
    # # Stop the request if the user is not an admin
    if not user.admin:
        return abort(401, description="Unauthorised user")
    # find the card
    stmt = db.select(Card).filter_by(id=id)
    card = db.session.scalar(stmt)
    #return an error if the card doesn't exist
    if not card:
        return abort(400, description= "Card doesn't exist")
    #Delete the card from the database and commit
    db.session.delete(card)
    db.session.commit()
    #return the card in the response
    return jsonify(card_schema.dump(card))

# Search / Filter card 

@cards.route("/search", methods=["GET"])
def search_cards():
    # create an empty list in case the query string is not valid
    cards_list = []

    if request.args.get('priority'):
        stmt = db.select(Card).filter_by(priority= request.args.get('priority'))
        cards_list = db.session.scalars(stmt)
    elif request.args.get('status'):
        stmt = db.select(Card).filter_by(status= request.args.get('status'))
        cards_list = db.session.scalars(stmt)

    result = cards_schema.dump(cards_list)
    # return the data in JSON format
    return jsonify(result)