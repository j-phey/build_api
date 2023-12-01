from main import ma
from marshmallow.validate import Length
from marshmallow import fields
from models.users import User

#create the Card Schema with Marshmallow, it will provide the serialization needed for converting the data into JSON
class UserSchema(ma.Schema):
    class Meta:
        # Added 'cards' to the list of users' fields
        fields = ['id', 'email', 'password', 'admin', 'cards']
        # these will not show up when we invoke dump to retrieve data:
        load_only = ['password', 'admin']
    #set the password's length to a minimum of 6 characters
    password = ma.String(validate=Length(min=6))
    # Set cards as a field that will store a list. To avoid an infinite loop of calls between user and cards, we exclude user from the card schema.
    cards = fields.List(fields.Nested("CardSchema", exclude=("user",)))

user_schema = UserSchema()
users_schema = UserSchema(many=True)