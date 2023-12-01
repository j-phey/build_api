from main import ma
from marshmallow import fields

class CommentSchema(ma.Schema):
    class Meta:
        ordered = True
        # Fields to expose. Card is not included as comments will be shown always attached to a Card.
        # id, message and user are the only fields in the schema.
        fields = ("id", "message", "user")
    # user is nested same way as the cards, only showing its email.
    user =  fields.Nested("UserSchema", only=("email",))  
      
comment_schema = CommentSchema()

comments_schema = CommentSchema(many=True)