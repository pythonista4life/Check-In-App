from flask_jwt_extended import JWTManager
from flask import jsonify

# Initialize JWT manager
jwt = JWTManager()

# Set up an in-memory blacklist (you can replace this with a more persistent solution like Redis)
BLACKLISTED_TOKENS = set()

def init_jwt(app):
    jwt.init_app(app)

    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return jsonify({"message": "The token has expired.", "error": "token_expired"}), 401

    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return jsonify({"message": "Signature verification failed.", "error": "invalid_token"}), 401

    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return jsonify({
            "description": "Request does not contain an access token.",
            "error": "authorization_required",
        }), 401

    # Check if a token is in the blacklist
    @jwt.token_in_blocklist_loader
    def check_if_token_in_blacklist(jwt_header, jwt_payload):
        jti = jwt_payload["jti"]  # Get the token's unique identifier (JTI)
        return jti in BLACKLISTED_TOKENS  # If it's in the blacklist, return True
    
    # If a token is blacklisted return an error.
    @jwt.revoked_token_loader
    def revoked_token_callback(jwt_header, jwt_payload):
        return jsonify({"description": "The token has been revoked.", "error": "token_revoked"}), 401