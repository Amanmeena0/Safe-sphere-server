import jwt
from jwt import PyJWKClient
import os
from flask import request, jsonify
from functools import wraps

# The Clerk JWKS URL is typically derived from your Clerk Frontend API URL.
# You should set CLERK_JWKS_URL in your .env file.
# Example: https://polite-cat-12.clerk.accounts.dev/.well-known/jwks.json

def get_jwks_client():
    jwks_url = os.getenv('CLERK_JWKS_URL')
    if not jwks_url:
        # Fallback or informative error if not set
        raise ValueError("CLERK_JWKS_URL environment variable is not set in .env")
    return PyJWKClient(jwks_url)

def verify_token(f):
    """
    Decorator to verify Clerk JWTs. 
    It fetches public keys from Clerk's JWKS endpoint to verify the signature (RS256).
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        # Check Authorization header
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization'].split()
            if len(auth_header) == 2 and auth_header[0] == 'Bearer':
                token = auth_header[1]

        if not token:
            return jsonify({'message': 'Authentication token is missing!'}), 401

        try:
            # Dynamically fetch the signing key from Clerk's JWKS
            jwks_client = get_jwks_client()
            signing_key = jwks_client.get_signing_key_from_jwt(token)
            
            # Verify the token
            payload = jwt.decode(
                token,
                signing_key.key,
                algorithms=["RS256"]
            )
            
            # Attach Clerk's user ID (sub) and full payload to the request object
            # This ensures subsequent code uses a verified identity.
            request.user_id = payload.get("sub")
            request.user_payload = payload
            
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token has expired!'}), 401
        except jwt.InvalidTokenError as e:
            return jsonify({'message': f'Invalid token: {str(e)}'}), 401
        except Exception as e:
            # Handles connection issues to JWKS or other unexpected errors
            return jsonify({'message': f'Authentication error: {str(e)}'}), 401

        return f(*args, **kwargs)

    return decorated
