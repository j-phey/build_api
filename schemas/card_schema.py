from main import ma
from marshmallow import fields, validates # 'fields' needed for nested fields in request. 'validates' for @validates decorator
from marshmallow.validate import Length, OneOf, Regexp, And
from marshmallow.exceptions import ValidationError
from models.cards import Card # Needed so that we can count how many existing cards have 'Ongoing'

# List of allowed values. Declared as tuples. Note the all-caps naming convention for Python constants.
# We call OneOf and pass in the tuple containing the valid values. OneOf will raise a ValidationError if the incoming value is not in the tuple.
VALID_PRIORITIES = ('Urgent', 'High', 'Low', 'Medium')
VALID_STATUSES = ('To Do', 'Done', 'Ongoing', 'Testing', 'Deployed')

# create the Card Schema with Marshmallow, it will provide the serialization needed for converting the data into JSON
class CardSchema(ma.Schema):
    # Regexp - every character is either a letter (upper or lower case), a digit, or a space
    title = fields.String(required=True, validate=And(Length(min=1), Regexp('^[a-zA-Z0-9 ]+$'))) # Title is required, must be a string and not empty. 
    status = fields.String(required=True, validate=OneOf(VALID_STATUSES)) # OneOf above valid statuses
    priority = fields.String(load_default='Medium', validate=OneOf(VALID_PRIORITIES)) # OneOf above valid priorities. Priority can be empty, but default to 'Medium' if so

    # Validates that there is one 'Ongoing' status card only
    # Declare @validates decorator first
    @validates('status') # Pass the name of the field we want to validate
    # Then we define the method itself, which accepts the implicit self parameter (as all methods must), and a value. 
    def validate_status(self, value):
        # Only apply this validator if the attempted status is 'Ongoing'
        if value == 'Ongoing':
            # Get a count of cards that already have the 'Ongoing' status
            count = Card.query.filter_by(status='Ongoing').count()
            if count > 1:
                raise ValidationError('You already have an ongoing card')

    class Meta:
        # show the columns in the right order instead of alphabetically
        ordered = True
        # Fields to expose when we 'jsonify' instances of the schema
        fields = ("id", "title", "description", "date", "status", "priority", "user", "comments")
    user =  fields.Nested("UserSchema", only=("email",)) # Don't display everything - only the email
    # The final step is to modify the card schema so we include a list of comments
    comments = fields.List(fields.Nested("CommentSchema"))


#single card schema, when one card needs to be retrieved
card_schema = CardSchema()
#multiple card schema, when many cards need to be retrieved
cards_schema = CardSchema(many=True)