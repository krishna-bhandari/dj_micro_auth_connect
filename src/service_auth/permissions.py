from rest_framework import permissions,status
from django.conf import settings

from .remote_model import RemoteModel
import jwt
# to give access to different user
import json
from rest_framework.exceptions import APIException

class TokenValidation:
    def verify_token(request):
        try:
            token = request.headers['Authorization']
        except KeyError as e:
            return False
        if request.session.has_key("user") and request.session["user"] == token:
            return True
        verify = RemoteModel(request, 'auth', 'verify_token', token).verify_token(token)
        perm = (verify.text)
        if verify.status_code == 200:
            request.session["user"] = token
            request.session["user_type"] = perm
            return True
        else:
            raise InvalidToken()


    def get_user_permission(request,user_type,perm):
        try:
            token = request.headers['Authorization']
            if request.session.has_key("user") and request.session["user"] == token:
                try:
                    verify = RemoteModel(request, 'user_perm', 'check_perm', token).get_permission(user_type,perm)
                    if verify.status_code == 200:
                        return True
                    else:
                        return False
                except Exception as e:
                    print(e)
                    return False
            else:
                return False
        except KeyError as e:
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
        checking whether normal user has permission to view facebook settings or not
        """
       
        user = request.session['user_type'].strip('"')
        permission = 'facebook_settings'
        user_perm = bool(TokenValidation.get_user_permission(request,user,permission))
        if user_perm:
            return True
        else:   
            # return False
            raise Forbidden()


class SetEscalation(permissions.BasePermission):

    def has_permission(self, request, view):
        """
        checking whether normal user has permission to view facebook settings or not
        """
       
        user = request.session['user_type'].strip('"')
        permission = 'set_escalation'
        user_perm = bool(TokenValidation.get_user_permission(request,user,permission))
        if user_perm:
            return True
        else:   
            # return False
            raise Forbidden() 


class UserManagement(permissions.BasePermission):

    def has_permission(self, request, view):
        """
        checking whether normal user has permission to view facebook settings or not
        """
       
        user = request.session['user_type'].strip('"')
        permission = 'user_management'
        user_perm = bool(TokenValidation.get_user_permission(request,user,permission))
        if user_perm:
            return True
        else:   
            # return False
            raise Forbidden()     

class ViewUserUsageData(permissions.BasePermission):

    def has_permission(self, request, view):
        """
        checking whether normal user has permission to view facebook settings or not
        """
       
        user = request.session['user_type'].strip('"')
        permission = 'view_user_usage_data'
        user_perm = bool(TokenValidation.get_user_permission(request,user,permission))
        if user_perm:
            return True
        else:   
            # return False
            raise Forbidden()   


class InvalidToken(APIException):
    """
        responds 400 for invalid or expired tokens
    """
    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = 'Token is invalid or expired'
    default_code = 'token_not_valid'


class Forbidden(APIException):
    """
        responds 400 for invalid or expired tokens
    """
    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = 'user has no permission to access this data'
    default_code = 'permission_not_allowed'