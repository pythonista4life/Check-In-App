from flask.views import MethodView
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_smorest import Blueprint, abort
from models import UserModel, FriendshipModel
from schemas.schemas import (
    SearchFriendResponseSchema,
    AddFriendResponseSchema,
    GetFriendsResponseSchema,
    DeleteFriendResponseSchema,
    AcceptRejectFriendResponseSchema,
    GetSentPendingFriendsResponseSchema,
    GetReceivedPendingFriendsResponseSchema,
)
from extensions.db import db

blp = Blueprint("friends", __name__, description="Operations for managing friendships.")


@blp.route("/search-friend/<friend_username>")
class SearchFriend(MethodView):

    @jwt_required()
    @blp.response(200, SearchFriendResponseSchema)
    def get(self, friend_username):
        """
        Return user if found in database.
        """
        user = UserModel.query.filter_by(username=friend_username).first()

        if not user:
            abort(404, message="User not found.")

        return {"user": user.username}


@blp.route("/add-friend/<friend_username>")
class AddFriend(MethodView):

    @jwt_required()
    @blp.response(201, AddFriendResponseSchema)
    def post(self, friend_username):
        """
        Send a friend request to another user.
        """
        # Assume current_user is fetched from session or token
        current_user_id = get_jwt_identity()

        # Check if the friend exists by their username
        friend = UserModel.query.filter_by(username=friend_username).first()

        if not friend:
            abort(404, message="User not found.")

        # Check if the friendship already exists
        existing_friendship = FriendshipModel.query.filter_by(
            user_id=current_user_id, friend_id=friend.id
        ).first()
        if existing_friendship:
            abort(
                400, message="Friend request already sent or user is already a friend."
            )

        # Create the friendship request using IDs (user_id and friend_id)
        new_friendship = FriendshipModel(
            user_id=current_user_id, friend_id=friend.id, status="pending"
        )
        db.session.add(new_friendship)
        db.session.commit()

        return {"message": "Friend request sent successfully."}


@blp.route("/accept-friend/<friend_username>")
class AcceptFriendRequest(MethodView):

    @jwt_required()
    @blp.response(200, AcceptRejectFriendResponseSchema)
    def put(self, friend_username):
        """
        Accept a friend request from another user.
        """
        # Get the current user's ID from the JWT
        current_user_id = get_jwt_identity()

        # Find the friend by username
        friend = UserModel.query.filter_by(username=friend_username).first()

        if not friend:
            abort(404, message="User not found.")

        # Check if a pending friend request exists
        friendship = FriendshipModel.query.filter_by(
            user_id=friend.id,  # Friend initiated the request
            friend_id=current_user_id,  # Current user is the recipient
            status="pending",
        ).first()

        if not friendship:
            abort(404, message="No pending friend request found from this user.")

        # Update the status to 'accepted'
        friendship.status = "accepted"
        db.session.commit()

        return {"message": "Friend request accepted successfully."}


@blp.route("/reject-friend/<friend_username>")
class RejectFriendRequest(MethodView):

    @jwt_required()
    @blp.response(200, AcceptRejectFriendResponseSchema)
    def put(self, friend_username):
        """
        Reject a friend request from another user.
        """
        # Get the current user's ID from the JWT
        current_user_id = get_jwt_identity()

        # Find the friend by username
        friend = UserModel.query.filter_by(username=friend_username).first()

        if not friend:
            abort(404, message="User not found.")

        # Check if a pending friend request exists
        friendship = FriendshipModel.query.filter_by(
            user_id=friend.id,  # Friend initiated the request
            friend_id=current_user_id,  # Current user is the recipient
            status="pending",
        ).first()

        if not friendship:
            abort(404, message="No pending friend request found from this user.")

        # Update the status to 'rejected'
        friendship.status = "rejected"
        db.session.commit()

        return {"message": "Friend request rejected successfully."}


@blp.route("/friends")
class GetFriends(MethodView):

    @jwt_required()
    @blp.response(200, GetFriendsResponseSchema)
    def get(self):
        """
        Retrieve the list of the user's friends.
        """
        # Placeholder for the current logged-in user's ID
        current_user_id = get_jwt_identity()

        friendships = FriendshipModel.query.filter_by(
            user_id=current_user_id, status="accepted"
        ).all()
        friends = [
            {"id": f.friend_id, "username": f.friend.username} for f in friendships
        ]

        return {"friendships": friends}


@blp.route("/sent-pending-friends")
class GetSentPendingFriends(MethodView):

    @jwt_required()
    @blp.response(200, GetSentPendingFriendsResponseSchema)
    def get(self):
        """
        Retrieve the list of the user's friends.
        """
        # Placeholder for the current logged-in user's ID
        current_user_id = get_jwt_identity()

        pending_friendships = FriendshipModel.query.filter_by(
            user_id=current_user_id, status="pending"
        ).all()
        pending_friends = [
            {"id": f.friend_id, "username": f.friend.username}
            for f in pending_friendships
        ]

        return {"pending_friends": pending_friends}


@blp.route("/received-pending-friends")
class GetReceivedPendingFriends(MethodView):

    @jwt_required()
    @blp.response(200, GetReceivedPendingFriendsResponseSchema)
    def get(self):
        """
        Retrieve the list of pending friend requests for the current user.
        """
        # Get the current logged-in user's ID
        current_user_id = get_jwt_identity()

        # Find friend requests the user has received (where friend_id = current_user_id)
        received_requests = FriendshipModel.query.filter_by(
            friend_id=current_user_id, status="pending"
        ).all()
        received_friends = [
            {"id": f.user_id, "username": f.user.username} for f in received_requests
        ]

        return {
            "received_requests": received_friends,
        }


@blp.route("/delete-friend/<friend_username>")
class DeleteFriend(MethodView):

    @jwt_required()
    @blp.response(200, DeleteFriendResponseSchema)
    def delete(self, friend_username):
        """
        Delete a friendship between the current user and another user.
        """
        current_user_id = get_jwt_identity()  # Get the ID of the logged-in user

        # Find the friend by username
        friend = UserModel.query.filter_by(username=friend_username).first()
        if not friend:
            abort(404, message="Friend not found.")

        # Check if a friendship exists
        friendship = FriendshipModel.query.filter(
            (
                (FriendshipModel.user_id == current_user_id)
                & (FriendshipModel.friend_id == friend.id)
            )
            | (
                (FriendshipModel.user_id == friend.id)
                & (FriendshipModel.friend_id == current_user_id)
            )
        ).first()

        if not friendship:
            abort(404, message="Friendship not found.")

        # Delete the friendship
        db.session.delete(friendship)
        db.session.commit()

        return {"message": "Friendship deleted successfully."}
