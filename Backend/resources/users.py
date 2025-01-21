import random
import os
from extensions.extensions import limiter
from dotenv import load_dotenv
from flask import jsonify
from flask_jwt_extended import jwt_required, get_jwt
from extensions.jwt_config import BLACKLISTED_TOKENS
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from datetime import datetime, timedelta
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    get_jwt_identity,
)
from werkzeug.security import generate_password_hash, check_password_hash
from models import UserModel
from schemas.schemas import (
    RegisterResponseSchema,
    RegisterArgsSchema,
    LoginArgsSchema,
    LoginResponseSchema,
    UserSchema,
    PasswordResetRequestSchema,
    ResetCodeRequestSchema,
    PasswordResetResponseSchema,
)
from extensions.db import db

from flask_mail import Mail, Message

load_dotenv("secrets.env")
mail = Mail()
blp = Blueprint("users", __name__, description="Operations on users.")


# Register a user.
@blp.route("/register")
class Register(MethodView):

    @blp.arguments(RegisterArgsSchema)
    @blp.response(201, RegisterResponseSchema)
    def post(self, user_data):
        """
        Create a new user account with hashed password.
        """
        # Check if the email is already registered
        if UserModel.query.filter_by(email=user_data["email"]).first():
            abort(400, message="A user with this email already exists.")

        elif UserModel.query.filter_by(username=user_data["username"]).first():
            abort(400, message="A user with this username already exists.")

        # Hash the password
        hashed_password = generate_password_hash(user_data["password"])

        # Create the user
        new_user = UserModel(
            email=user_data["email"],
            username=user_data["username"],
            password=hashed_password,
        )
        db.session.add(new_user)
        db.session.commit()

        return {
            "message": f"Account for {new_user.username} has been created successfully."
        }


# Login a user.
@blp.route("/login")
class Login(MethodView):

    @blp.arguments(LoginArgsSchema)  # Validate login arguments
    @blp.response(200, LoginResponseSchema)  # Return response with success message
    def post(self, login_data):
        """
        Log in a user by verifying the email and password.
        """
        # Retrieve user from the database using the provided email
        user = UserModel.query.filter_by(email=login_data["email"]).first()

        if not user:
            abort(400, message="Invalid email.")

        # Verify the provided password with the stored hashed password
        if not check_password_hash(user.password, login_data["password"]):
            abort(400, message="Invalid password.")

        # Create access token if login is successful
        access_token = create_access_token(identity=str(user.id), fresh=True)

        # Create Refresh Token
        refresh_token = create_refresh_token(identity=str(user.id))

        # Return JWT Token and a success message if login is successful
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "message": f"Successfully logged in as {user.username}.",
        }


@blp.route("/refresh")
class TokenRefresh(MethodView):
    @jwt_required(refresh=True)
    def post(self):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False)
        # If you blacklist the refresh token you will need to login once again.
        # jti = get_jwt()["jti"]
        # BLACKLISTED_TOKENS.add(jti)
        return {"access_token": new_token}, 200


# Get or delete a user.
@blp.route("/user/<int:user_id>")
class User(MethodView):

    @blp.response(200, UserSchema)
    def get(self, user_id):
        """
        Get a user.
        """
        user = UserModel.query.get_or_404(user_id)
        return user

    def delete(self, user_id):
        """
        Delete a user.
        """
        user = UserModel.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()
        return jsonify({"message": "User deleted successfully."}), 200


# Send Email Function
def send_email(recipient, body):
    msg = Message(
        "Password Reset Code",
        sender=os.getenv("SECRET_KEY"),
        recipients=[recipient],
        body=body,
    )
    mail.send(msg)


# Reset password request.
@blp.route("/reset-password/request")
class RequestPasswordReset(MethodView):

    @limiter.limit("3 per minute")
    @blp.arguments(PasswordResetRequestSchema)
    @blp.response(200, PasswordResetResponseSchema)
    def post(self, data):
        """
        Send a request to reset your password by a 4 digit code sent to your email.
        """
        user = UserModel.query.filter_by(email=data["email"]).first()

        if not user:
            abort(404, message="User with this email does not exist.")

        reset_code = f"{random.randint(1000, 9999)}"  # Generate a 4-digit code
        expiry = datetime.now() + timedelta(minutes=15)  # Code valid for 15 minutes

        user.reset_code = reset_code
        user.reset_code_expiry = expiry
        db.session.commit()

        # Send reset code via email
        send_email(user.email, f"Your reset code is: {reset_code}")
        return {"message": "Password reset code sent to your email."}


# Reset password.
@blp.route("/reset-password/reset")
class ResetPassword(MethodView):

    @blp.arguments(ResetCodeRequestSchema)
    def post(self, data):
        """
        Hash and update a new password.
        """
        user = UserModel.query.filter_by(email=data["email"]).first()

        if not user or user.reset_code != data["reset_code"]:
            abort(400, message="Invalid or expired reset code.")

        if user.reset_code_expiry < datetime.now():
            abort(400, message="Reset code has expired.")

        # Hash the new password and update it
        user.password = generate_password_hash(data["new_password"])
        user.reset_code = None
        user.reset_code_expiry = None
        db.session.commit()

        return jsonify({"message": "Password has been reset successfully."}), 200


# Logout a user.
@blp.route("/logout")
class Logout(MethodView):

    @jwt_required()
    def post(self):
        """
        Log out a user by blacklisting their token.
        """
        jti = get_jwt()["jti"]
        BLACKLISTED_TOKENS.add(jti)

        return jsonify({"message": "Successfully logged out."}), 200
