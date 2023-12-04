from main import ma
from marshmallow import fields # needed for nested fields in request

#create the Card Schema with Marshmallow, it will provide the serialization needed for converting the data into JSON
class CardSchema(ma.Schema):
    class Meta:
        # show the columns in the right order instead of alphabetically
        ordered = True
        # Fields to expose
        fields = ("id", "title", "description", "date", "status", "priority", "user", "comments")
    user =  fields.Nested("UserSchema", only=("email",)) # Don't display everything - only the email
    # The final step is to modify the card schema so we include a list of comments
    comments = fields.List(fields.Nested("CommentSchema"))

#single card schema, when one card needs to be retrieved
card_schema = CardSchema()
#multiple card schema, when many cards need to be retrieved
cards_schema = CardSchema(many=True)