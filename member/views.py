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
from django.db import IntegrityError
import pytz

#Create your views here.
class Register(APIView):
    authentication_classes = ()
    permission_classes = (AllowAny,)
    def post(self, request, format=None):
        """
        Register user
        ---
        request_serializer: member.serializers.MemberRegisterSerializer
        response_serializer: member.serializers.MemberSerializer
        """

        serializedMember = MemberRegisterSerializer(data=request.data)
        if serializedMember.is_valid():
            if request.data['password'] != request.data['password2']:
                return Response({"password":["The field password and password2 does not match"]}, status=status.HTTP_400_BAD_REQUEST)

            member = Member.objects.create_user(
                email    = serializedMember.initial_data['username'],
                username = serializedMember.initial_data['username'],
                password = serializedMember.initial_data['password'],
                is_vendor= serializedMember.initial_data['is_vendor'],
                phone    = serializedMember.initial_data['phone'],
                country_code = serializedMember.initial_data['country_code'],
                last_login = datetime.now()

                )

            hooio_url = "https://secure.hoiio.com/open/sms/send?dest=%2B6596541924&sender_name=PIKA&msg=PIKACHU+please+response!&access_token=b7GlIeggXZQOYCJJ&app_id=j4wwJjlFrcYb9gsB"
            
            token, created = Token.objects.get_or_create(user=member)
            if not created:
                token.created = datetime.utcnow().replace(tzinfo=pytz.utc)
                token.save()

            serializedMember = MemberSerializer(member)

            return Response({'token':token.key, 'user':serializedMember.data, 'message':'Register successful'}, status=status.HTTP_201_CREATED)

        return Response(serializedMember.errors, status=status.HTTP_400_BAD_REQUEST)


class Login(ObtainAuthToken):
    # to add expiring auth token
    authentication_classes = ()
    permission_classes = (AllowAny,)
    
    def post(self, request):
        # """
        # Login user, returns token and user data
        # ---
        # request_serializer: rest_framework.authtoken.serializers.AuthTokenSerializer    
        # response_serializer: member.serializers.MemberSerializer
        # """
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']

        serializedMember = MemberSerializer(user)
        token, created = Token.objects.get_or_create(user=user)
        if not created:
            token.created = datetime.utcnow().replace(tzinfo=pytz.utc)
            token.save()

        return Response({'token': token.key,'message':'Login Successful','user':serializedMember.data})

class Verification(APIView):
    def get(self, request):
        pass

    def post(self, request):
        pass


class MemberDetail(APIView):
    def get(self, request):
        # """
        # Get all details for this member
        # ---
        # serializer: member.serializers.MemberSerializer
        # """
        serializedMember = MemberSerializer(request.user)
        return Response({'user':serializedMember.data})

    def put(self, request):
        # """
        # Modify details for currently logged in member, fields that is not included in the JSON will be left unchanged
        # ---
        # serializer: member.serializers.MemberSerializer
        # """

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


class MemberCategoryDetail(APIView):
    def post(self, request, mc_id):
        try:
            MemberCategory.objects.create(category_id=mc_id, member=request.user)
        except ValueError:
            return Response({'error':'No such category'})
        except IntegrityError:
            return Response({'error':'Category already been associated with member'})
        
        return Response({'message':'Category has been added to the member'})

    def delete(self, request, mc_id):
        try:
            mc = MemberCategory.objects.get(id=mc_id, member=request.user)
        except:
            raise Http404

        mc.delete()
        return Response({'message':'Category has been deleted from member'},status=status.HTTP_204_NO_CONTENT)