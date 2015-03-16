# from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.serializers import AuthTokenSerializer
from datetime import datetime
import pytz

# Create your views here.
class Register(APIView):
    def post(self, request, format=None):
        pass                

class Update(APIView):
    def post(self, request, format=None):
        pass

class Login(ObtainAuthToken):
    # to add expiring auth token
    def post(self, request):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        if not created:
            token.created = datetime.utcnow().replace(tzinfo=pytz.utc)
            token.save()

        return Response({'token': token.key})