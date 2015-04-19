# from django.http import Http404
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.serializers import AuthTokenSerializer
# from member.models import Member
from member.serializers import MemberSerializer
from datetime import datetime
import pytz

# Create your views here.
# class Register(APIView):
#     permission_classes = (AllowAny,)
#     def post(self, request, format=None):
#         serializedMember = MemberSerializer(data=request.data)
#         if serializedMember.is_valid():
#             serializedMember.save()
#             return Response(serializedMember.data, status=status.HTTP_201_CREATED)
#         return Response(serializedMember.errors, status=status.HTTP_400_BAD_REQUEST)

class Login(ObtainAuthToken):
    # to add expiring auth token
    def post(self, request):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']

        serializedMember = MemberSerializer(user)
        token, created = Token.objects.get_or_create(user=user)
        if not created:
            token.created = datetime.utcnow().replace(tzinfo=pytz.utc)
            token.save()

        return Response({'token': token.key,'message':'Login Successful','user':serializedMember.data})

class Profile(APIView):
    def get(self, request):
        serializedMember = MemberSerializer(request.user)
        return Response(serializedMember.data)
