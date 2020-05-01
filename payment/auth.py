import jwt
from rest_framework import authentication
from rest_framework import exceptions
from eon_payment.settings import DECODE_KEY


class CustomJWTAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        token = request.headers.get('authorization', None)
        if not token:
            raise exceptions.NotAuthenticated

        token = token.split()
        token_length = len(token)
        if token_length > 2 or token_length < 2 or token[0] != 'Bearer':
            raise exceptions.AuthenticationFailed
        try:
            payload = jwt.decode(token[1], DECODE_KEY, algorithms=['HS256'])
        except:
            raise exceptions.ValidationError({'message': 'Signature Validation Failed'})

        return payload['user_id'], None
