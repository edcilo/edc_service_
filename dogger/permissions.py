import jwt
from rest_framework.permissions import BasePermission
from app.environ import env

class IsAuthorized(BasePermission):
    message = 'Access Forbidden'

    def has_permission(self, request, view):
        auth_token = request.headers['Authorization']
        token = auth_token.replace('Bearer ', '')
        key = env('APP_JWT_KEY')
        print(token)

        try:
            request.data['jwt-decode-data'] = jwt.decode(token, key, algorithms="HS256")
            return True
        except (jwt.InvalidSignatureError, jwt.DecodeError, jwt.ExpiredSignatureError):
            return False
