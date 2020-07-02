import os
import json
from flask import request, abort
from functools import wraps
from jose import jwt
from urllib.request import urlopen


AUTH0_DOMAIN = os.environ['AUTH0_DOMAIN']
ALGORITHMS = os.environ['ALGORITHMS']
API_AUDIENCE = os.environ['API_AUDIENCE']


class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


def get_token_auth_header():
    auth = request.headers.get('Authorization', None)
    if not auth:
        abort(401, description='Authorization header is expected')
    parts = auth.split()
    if parts[0].lower() != 'bearer':
        abort(401, description='Authorization header must start with "Bearer"')
    elif len(parts) == 1:
        abort(401, description='Token not found.')
    elif len(parts) > 2:
        abort(401, description='Authorization header must be bearer token')
    token = parts[1]
    return token


def check_permissions(permission, payload):
    if 'permissions' not in payload:
        abort(400, description='permissions does not exist in token payload')
    if permission not in payload['permissions']:
        abort(403)
    return True


def verify_decode_jwt(token):
    jsonurl = urlopen(f'https://{AUTH0_DOMAIN}/.well-known/jwks.json')
    jwks = json.loads(jsonurl.read())
    unverified_header = jwt.get_unverified_header(token)
    rsa_key = {}
    if 'kid' not in unverified_header:
        abort(401, description='Authorization malformed')
    for key in jwks['keys']:
        if key['kid'] == unverified_header['kid']:
            rsa_key = {
                'kty': key['kty'],
                'kid': key['kid'],
                'use': key['use'],
                'n': key['n'],
                'e': key['e']
            }
    if rsa_key:
        try:
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=ALGORITHMS,
                audience=API_AUDIENCE,
                issuer='https://' + AUTH0_DOMAIN + '/'
            )
            return payload
        except jwt.ExpiredSignatureError:
            abort(401, description='Token expired')
        except jwt.JWTClaimsError:
            abort(
                401,
                description=(
                    'Incorrect claims. Please, check the audience and issuer'))
        except Exception:
            abort(400, description='Unable to parse authentication token')
    abort(400, description='Unable to find the appropriate key')


def requires_auth(permission=''):
    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            token = get_token_auth_header()
            try:
                payload = verify_decode_jwt(token)
            except:
                abort(401)
            check_permissions(permission, payload)
            return f(payload, *args, **kwargs)

        return wrapper
    return requires_auth_decorator
