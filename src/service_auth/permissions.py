from rest_framework import permissions
from django.conf import settings

from .remote_model import RemoteModel

# to give access to different user


class IsAuthenticated(permissions.BasePermission):
    """
    Allows access only to authenticated users. It takes
    the token from headers and send it to auth service to
    verify. If verified it creates session for that user inorder
    to reduce the number of requests for verifying token. If not
    in session then create new session.If no token provided return False.
    """ 

    def has_permission(self, request, view):
        try:
            token = request.headers['Authorization']
        except KeyError as e:
            return False
        if request.session.has_key("user") and request.session["user"] == token:
            return True
        verify = bool(RemoteModel(request,'auth','api/auth/token/verify',token).verify_token(token))
        if verify:
            request.session["user"] = token
            return True
        else:
            return False
