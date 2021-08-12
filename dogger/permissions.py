import jwt
from django.utils import timezone
from rest_framework.permissions import BasePermission
from app.environ import env

class IsAuthorized(BasePermission):
    message = 'Access Forbidden'

    def has_permission(self, request, view):
        try:
            auth_token = request.headers['Authorization']
            token = auth_token.replace('Bearer ', '')
            key = env('APP_JWT_KEY')
            payload = jwt.decode(token, key, algorithms="HS256")
            request.data['jwt-payload'] = payload
            return timezone.now().timestamp() <= payload['exp']
        except (jwt.InvalidSignatureError, jwt.DecodeError, jwt.ExpiredSignatureError, KeyError):
            return False


class IsOwner(BasePermission):
    message = 'Access Forbidden'

    def has_permission(self, request, view):
        try:
            user = request.data['jwt-payload']
            roles = user['roles']
            return 'user' in roles
        except KeyError:
            return False
