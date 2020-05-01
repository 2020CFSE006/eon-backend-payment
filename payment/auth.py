import jwt
from rest_framework import authentication
from rest_framework import exceptions
from rest_framework.authentication import get_authorization_header
from eon_payment.settings import DECODE_KEY


class CustomJWTAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        token = get_authorization_header(request)
        if not token:
            raise exceptions.NotAuthenticated

        token = token.split()
        if len(token) > 2 or len(token) < 2:
            raise exceptions.AuthenticationFailed

        if token[0] != 'Bearer':
            raise exceptions.AuthenticationFailed

        token = token.split()[1]

        try:
            payload = jwt.decode(token, DECODE_KEY, algorithms=['HS256'])
        except:
            raise exceptions.ValidationError('Token Validation Failed')

        return payload['user_id'], None
