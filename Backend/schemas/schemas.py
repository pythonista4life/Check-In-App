from marshmallow import fields, validate, Schema, ValidationError, pre_load


# Make sure the data recieved must include questions.
class QuestionResponseSchema(Schema):
    id = fields.Str(dump_only=True)
    question = fields.Str(required=True)

# Custom Questions Schemas
class CustomQuestionSchema(Schema):
    question = fields.Str(required=True)  # Provided in the request body

class CustomQuestionResponseSchema(Schema):
    id = fields.Str(required=True)  # Returned after creation
    user_id = fields.Str(required=True)
    question = fields.Str(required=True)

class DeleteCustomQuestionResponseSchema(Schema):
    # List of questions, which can be empty
    questions = fields.List(fields.Dict(keys=fields.Str(), values=fields.Str()), required=True)
    
    # Message giving context about the action
    message = fields.Str(required=True)

# Signup Args Schema
class RegisterArgsSchema(Schema):
    id = fields.Int(dump_only=True)
    email = fields.Email(required=True, description="User's email address")
    confirm_email = fields.Email(
        required=True,
        description="Confirmation of the user's email address"
    )
    password = fields.String(
        required=True,
        description="User's password",
        validate=validate.Length(min=8, error="Password must be at least 8 characters long."),
        load_only = True
    )
    username = fields.String(
        required=True,
        description="User's username",
        validate=validate.Length(min=3, error="Username must be at least 3 characters long.")
    )

    @pre_load
    def check_email_match(self, data, **kwargs):
        """
        Custom check to ensure email and confirm_email match.
        """
        if data.get("email") != data.get("confirm_email"):
            raise ValidationError("Email and confirm email must match.", field_name="confirm_email")
        return data
    
# Signup Response Schema
class RegisterResponseSchema(Schema):
    message = fields.String(
        required=True,
        description="Confirmation message indicating account creation success."
    )

# Login Args Schema
class LoginArgsSchema(Schema):
    id = fields.Int(dump_only=True)
    email = fields.Email(required=True, description="User's email address")
    password = fields.String(
        required=True,
        description="User's password",
        validate=validate.Length(min=8, error="Password must be at least 8 characters long."),
        load_only=True
    )

# Login Response Schema
class LoginResponseSchema(Schema):
    access_token = fields.String(
        required=True, 
        description="JWT Token"
    )
    message = fields.String(
        required=True, 
        description="A success message confirming that the user has logged in successfully"
    )

# User Schema
class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True)
    email = fields.Str(required=True)
    # We use load_only=True to specify that we dont want that value returned.
    password = fields.Str(required=True, load_only=True)

# Password Reset Schema
class PasswordResetRequestSchema(Schema):
    email = fields.Email(
        required=True,
        description="The registered email address of the user"
    )

# Password Reset Response Schema
class PasswordResetResponseSchema(Schema):
    message = fields.Str(description="Message after resetting the password")

# Reset Code Response Schema
class ResetCodeRequestSchema(Schema):
    email = fields.Email(
        required=True,
        description="The registered email address of the user"
    )
    reset_code = fields.String(
        required=True,
        description="Verification code for password reset"
    )
    new_password = fields.String(
        required=True,
        description="User's password",
        validate=validate.Length(min=8, error="Password must be at least 8 characters long."),
        load_only = True
    )

# Friendship Schemas

# Search for a friend.
class SearchFriendResponseSchema(Schema):
    user = fields.Nested(UserSchema, required=True, description="Search for a friend.")

# Add a friend.
class AddFriendResponseSchema(Schema):
    message = fields.Str(required=True, description="Add a friend.")

# Accept/Reject A Friend Request.
class AcceptRejectFriendResponseSchema(Schema):
    message = fields.Str(required=True, description="Accept/Reject A Friend Request.")

# A list of friendships.
class GetFriendsResponseSchema(Schema):
    friendships = fields.List(fields.Nested(UserSchema), description="A list of friendships.")

# A list of pending friend requests sent by the user.
class GetSentPendingFriendsResponseSchema(Schema):
    pending_friends = fields.List(fields.Nested(UserSchema), description="A list of pending friend requests sent by the user.")

# A list of pending friend requests received by the user.
class GetReceivedPendingFriendsResponseSchema(Schema):
    received_requests = fields.List(fields.Nested(UserSchema), description="A list of pending friend requests received by the user.")

# Confirmation of deletion.
class DeleteFriendResponseSchema(Schema):
    message = fields.Str(description="Confirmation of deletion.", required=True)