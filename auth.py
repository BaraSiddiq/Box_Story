import json
from functools import wraps
from jose import jwt
from urllib.request import urlopen
from flask import request, jsonify, abort
import os
AUTH0_DOMAIN = os.environ['AUTH_DOMAIN']
ALGORITHMS = ['RS256']
API_AUDIENCE = 'story'


## AuthError Exception

class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


def get_token_auth_header():
    # raise Exception('Not Implemented')
    auth = request.headers.get("Authorization", None)
    if auth is None:
        msg = 'Wrong formed header - Authorization header is missing.'
        abort(401, msg)

    items = auth.split(" ")
    if items[0].lower() != 'bearer':
        msg = 'Wrong formed header - Bearer key is missing.'
        abort(400, msg)

    elif len(items) != 2:
        msg = 'Wrong formed header.'
        abort(400, msg)

    token = items[1]
    return token


def check_permissions(permission, payload: list):
    print(permission, ' : ', payload['permissions'])
    if permission in payload['permissions']:
        print('found!!!')
        for p in payload['permissions']:
            if permission.lower() == p:
                print(p)
    else:
        msg = 'This user cannot perform this task.'
        abort(401, msg)
    return 'permission'


def verify_decode_jwt(token):
    jsonurl = urlopen(f'https://{AUTH0_DOMAIN}/.well-known/jwks.json')
    jwks = json.loads(jsonurl.read())
    unverified_header = jwt.get_unverified_header(token)
    rsa_key = {}
    if 'kid' not in unverified_header:
        msg = '(code: invalid_header, description: Authorization malformed.)'
        abort(401, msg)


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
            msg = '(code: token_expired, description: Token expired.)'
            abort(401, msg)

        except jwt.JWTClaimsError:
            msg = '(code: invalid_claims, description: Incorrect claims. Please, check the audience and issuer.)'
            abort(401, msg)

        except Exception:
            msg = '(code: invalid_header, description: Unable to parse authentication token.)'
            abort(400, msg)

    msg = '(code: invalid_header, description: Unable to find the appropriate key.)'
    abort(400, msg)


def requires_auth(permission=''):
    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            token = get_token_auth_header()
            payload = verify_decode_jwt(token)
            check_permissions(permission, payload)
            return f(payload, *args, **kwargs)

        return wrapper

    return requires_auth_decorator