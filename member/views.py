# from django.http import Http404
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.serializers import AuthTokenSerializer
from member.models import Member, MemberCategory
from member.serializers import MemberSerializer, MemberRegisterSerializer, MemberCategorySerializer
from datetime import datetime
from django.http import Http404
import pytz

#Create your views here.
class Register(APIView):
    authentication_classes = ()
    permission_classes = (AllowAny,)
    def post(self, request, format=None):
        serializedMember = MemberRegisterSerializer(data=request.data)
        if serializedMember.is_valid():
            if request.data['password'] != request.data['password2']:
                return Response({"password":["The field password and password2 does not match"]}, status=status.HTTP_400_BAD_REQUEST)

            member = Member.objects.create_user(
                email    = serializedMember.initial_data['email'],
                username = serializedMember.initial_data['username'],
                password = serializedMember.initial_data['password'],
                is_vendor= serializedMember.initial_data['is_vendor'],
                last_login = datetime.now()

                )
            
            serializedMember = MemberSerializer(member)

            return Response({'user':serializedMember.data}, status=status.HTTP_201_CREATED)

        return Response(serializedMember.errors, status=status.HTTP_400_BAD_REQUEST)


class Login(ObtainAuthToken):
    # to add expiring auth token
    authentication_classes = ()
    permission_classes = (AllowAny,)
    
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


class MemberDetail(APIView):
    def get(self, request):
        serializedMember = MemberSerializer(request.user)
        return Response({'user':serializedMember.data})

    def put(self, request):
        serializedMember = MemberSerializer(request.user ,data=request.data, partial=True)
        if serializedMember.is_valid():
            serializedMember.save()
            return Response({'user':serializedMember.data})
        return Response(serializedMember.errors, status=status.HTTP_400_BAD_REQUEST)


class MemberPhotoList(APIView):
    def post(self, request):
        serializedMember = MemberSerializer(request.user ,data=request.data, exclude=('first_name','last_name','username','email','photo','phone','mobile','fax','categories'))
        if serializedMember.is_valid():
            serializedMember.save()
            return Response({'user':serializedMember.data}, status=status.HTTP_200_CREATED)
        return Response(serializedMember.errors, status=status.HTTP_400_BAD_REQUEST)


class MemberCategoryList(APIView):
    def get(self, request):
        categories = MemberCategory.objects.filter(member=request.user)
        serializedMemberCategory = MemberCategorySerializer(categories, many=True)

        return Response({'categories':serializedMemberCategory.data})

    def post(self, request, mc_id):
        mc, created = MemberCategory.objects.get_or_create(category=mc_id, member=request.user)
        serializedMemberCategory = MemberCategorySerializer(mc)
        return Response(serializedMemberCategory.data)

    def delete(self, request, mc_id):
        try:
            mc = MemberCategory.objects.get(id=mc_id, member=request.user)
        except:
            raise Http404

        mc.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)