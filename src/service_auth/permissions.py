from rest_framework import permissions
from django.conf import settings

from .remote_model import RemoteModel
import jwt
# to give access to different user


class TokenValidation:
    def verify_token(request):
        try:
            token = request.headers['Authorization']
        except KeyError as e:
            return False
        if request.session.has_key("user") and request.session["user"] == token:
            return True
        verify = bool(RemoteModel(request, 'auth', 'verify_token', token).verify_token(token))
        if verify:
            request.session["user"] = token
            return True
        else:
            return False

    def get_user_permission(request):
        try:
            token = request.headers['Authorization']
        except KeyError as e:
            return False
        if request.session.has_key("user_type"):
            return True

        token = request.headers.get('Authorization')
        token = token[6:]
        if not token:
            return False
        info = jwt.decode(token, key=settings.SECRET_KEY)
        user = info.get('user_type')
        try:
            verify = bool(RemoteModel(request, 'user_perm', 'check_perm', token).get_permission(user))
            if verify:
                print(verify)
                request.session["user_type"] = verify
                return True
            else:
                return False
        except Exception as e:
            print(e)
            return False


class IsAuthenticated(permissions.BasePermission):
    """
    Allows access only to authenticated users. It takes
    the token from headers and send it to auth service to
    verify. If verified it creates session for that user inorder
    to reduce the number of requests for verifying token. If not
    in session then create new session.If no token provided return False.
    """ 

    def has_permission(self, request, view):
        token = TokenValidation.verify_token(request)
        return True if token else False
            


class SetFacebook(permissions.BasePermission):

    def has_permission(self, request, view):
        """
        checking whether normal user has permission to view or not
        """
        user_perm = TokenValidation.get_user_permission(request)
        if user_perm:
            user = request.session['user_type']
            return True if user['facebook_settings'] else False
        else:
            return False