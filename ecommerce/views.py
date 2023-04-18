from jsonschema import ValidationError
import requests
from rest_framework.response import Response
from rest_framework.views import APIView
from ecommerce.customauth import CustomAuthentication
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from main import models
from django.http import JsonResponse,HttpResponse


def Welcome(request):
    return HttpResponse("Hello Sai Nikhil Welcome To Ecommerce Application")



