from extensions.db import db


class UserModel(db.Model):

    # The name of the database table.
    __tablename__ = "users"

    # Database columns.
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    reset_code = db.Column(db.String(6), nullable=True)
    reset_code_expiry = db.Column(db.DateTime, nullable=True)

    # Relationships
    friends = db.relationship(
        "FriendshipModel",
        foreign_keys="[FriendshipModel.user_id]",
        back_populates="user",
        cascade="all, delete-orphan",
        lazy="dynamic",
    )
    friend_of = db.relationship(
        "FriendshipModel",
        foreign_keys="[FriendshipModel.friend_id]",
        back_populates="friend",
        cascade="all, delete-orphan",
        lazy="dynamic",
    )


class FriendshipModel(db.Model):
    __tablename__ = "friendships"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,  # Add an index for better query performance
    )
    friend_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    status = db.Column(db.String(20), nullable=False, default="pending")
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(
        db.DateTime, server_default=db.func.now(), onupdate=db.func.now()
    )

    # Relationships
    user = db.relationship(
        "UserModel", foreign_keys=[user_id], back_populates="friends"
    )
    friend = db.relationship(
        "UserModel", foreign_keys=[friend_id], back_populates="friend_of"
    )
