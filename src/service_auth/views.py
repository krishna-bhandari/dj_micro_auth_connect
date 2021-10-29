from django.http.response import HttpResponse, HttpResponseForbidden
from django.shortcuts import render

# Create your views here.
from django.contrib.auth.decorators import login_required
import requests
import urllib.parse
import json
from django.conf import settings 
from rest_framework.decorators import api_view, permission_classes
from rest_framework import generics
from .permissions import IsAuthenticated
from .remote_model import RemoteModel

@api_view(['GET'])
def get_user(request):
    if request.user.is_authenticated:
        user = RemoteModel(request,'authentication','api/auth/user/list').get()
        return HttpResponse(user)
    else:
        return HttpResponse('not login')

class GetUser(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    def get(self,request,*args,**kwargs):
        user = RemoteModel(request,'auth','api/auth/user/list').get()
        return HttpResponse(user)
