import json
from flask import request,jsonify
from functools import wraps
from jose import jwt
from urllib.request import urlopen
import os



AUTH0_DOMAIN = os.getenv('AUTH0_DOMAIN')
ALGORITHMS = ['RS256']
API_AUDIENCE = os.getenv('API_AUDIENCE')

class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code

def get_token_auth_header():
    """Obtains the Access Token from the Authorization Header"""
    auth = request.headers.get('Authorization', None)
    
    if not auth:
        return jsonify({
            'success': False,
            'code': 'authorization_header_missing',
            'description': 'Authorization header is expected.'
        }), 401

    parts = auth.split()
    
    if parts[0].lower() != 'bearer':
        return jsonify({
            'success': False,
            'code': 'invalid_header',
            'description': 'Authorization header must start with "Bearer".'
        }), 401

    if len(parts) == 1:
        return jsonify({
            'success': False,
            'code': 'invalid_header',
            'description': 'Token not found.'
        }), 401

    if len(parts) > 2:
        return jsonify({
            'success': False,
            'code': 'invalid_header',
            'description': 'Authorization header must be bearer token.'
        }), 401

    return parts[1]  # ✅ Return only the token string

def check_permissions(permission, payload):
    """Checks if the required permission exists in the JWT payload"""
    if 'permissions' not in payload:
        return jsonify({
            'success': False,
            'code': 'invalid_claims',
            'description': 'Permissions not included in JWT.'
        }), 400

    if permission not in payload['permissions']:
        return jsonify({
            'success': False,
            'code': 'unauthorized',
            'description': 'Permission not found.'
        }), 403

    return True  # ✅ Proper return instead of `raise True`

def verify_decode_jwt(token):
    """Verifies and decodes the JWT using Auth0's JWKS"""
    try:
        # GET THE PUBLIC KEY FROM AUTH0
        jsonurl = urlopen(f'https://{AUTH0_DOMAIN}/.well-known/jwks.json')
        jwks = json.loads(jsonurl.read())

        # GET THE DATA IN THE HEADER
        try:
            unverified_header = jwt.get_unverified_header(token)
        except jwt.JWTError:
            return jsonify({
                'success': False,
                'code': 'invalid_header',
                'description': 'Unable to parse token header.'
            }), 401

        # CHOOSE OUR KEY
        rsa_key = {}
        if 'kid' not in unverified_header:
            return jsonify({
                'success': False,
                'code': 'invalid_header',
                'description': 'Authorization malformed.'
            }), 401

        for key in jwks['keys']:
            if key['kid'] == unverified_header['kid']:
                rsa_key = {
                    'kty': key['kty'],
                    'kid': key['kid'],
                    'n': key['n'],
                    'e': key['e']
                }

        # VERIFY THE TOKEN
        if rsa_key:
            try:
                payload = jwt.decode(
                    token,
                    rsa_key,
                    algorithms=ALGORITHMS,
                    audience=API_AUDIENCE,
                    issuer=f'https://{AUTH0_DOMAIN}/'
                )
                return payload
            except jwt.ExpiredSignatureError:
                return jsonify({
                    'success': False,
                    'code': 'token_expired',
                    'description': 'Token expired.'
                }), 401
            except jwt.JWTClaimsError:
                return jsonify({
                    'success': False,
                    'code': 'invalid_claims',
                    'description': 'Incorrect claims. Please check audience and issuer.'
                }), 401
            except Exception:
                return jsonify({
                    'success': False,
                    'code': 'invalid_token',
                    'description': 'Invalid token.'
                }), 401

    except Exception as e:
        return jsonify({
            'success': False,
            'code': 'invalid_header',
            'description': f'Unable to parse authentication token. Error: {str(e)}'
        }), 401

def requires_auth(permission=''):
    """Authorization decorator method"""
    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            token = get_token_auth_header()
            response = verify_decode_jwt(token)
            
            # If `verify_decode_jwt` returned a JSON error response, return it instead of crashing
            if isinstance(response, tuple):
                return response
            
            # Now, check permissions
            if 'permissions' not in response:
                return jsonify({
                    "success": False,
                    "code": "invalid_claims",
                    "description": "Permissions not included in JWT."
                }), 400
            
            if permission and permission not in response['permissions']:
                return jsonify({
                    "success": False,
                    "code": "unauthorized",
                    "description": "Permission not found."
                }), 403
            
            return f(response, *args, **kwargs)
        return wrapper
    return requires_auth_decorator