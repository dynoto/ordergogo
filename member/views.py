# from django.http import Http404
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.serializers import AuthTokenSerializer
from member.models import Member, MemberCategory, MemberVerification
from member.serializers import MemberSerializer, MemberRegisterSerializer, MemberCategorySerializer, MemberPhotoSerializer, MemberVerificationSerializer
from datetime import datetime
from random import randrange
from django.http import Http404
from django.db import IntegrityError
# from ordergogo.settings import HOOIO_SENDER, HOOIO_ACCESS_TOKEN, HOOIO_APP_ID
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

            #SEND VERIFICATION CODE TO THE USER
            vrf = MemberVerification.objects.create(member=member)
            vrf.send_code(vrf.code, member.country_code, member.phone)

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
        """
        Login user, returns token and user data
        ---
        request_serializer: rest_framework.authtoken.serializers.AuthTokenSerializer    
        response_serializer: member.serializers.MemberSerializer
        """
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']

        serializedMember = MemberSerializer(user)
        token, created = Token.objects.get_or_create(user=user)
        if not created:
            token.created = datetime.utcnow().replace(tzinfo=pytz.utc)
            token.save()

        return Response({'token': token.key,'message':'Login Successful','user':serializedMember.data})

class Verify(APIView):
    def get_object(self, member):
        try:
            return MemberVerification.objects.get(member=member, verified=False)
        except:
            raise Http404

    def get(self, request):
        """
        Resend verification code to the registered mobile number, allow only every 5 minutes after the SMS has been successfully sent
        ---
        omit_serializer: true
        """

        vrf = self.get_object(request.user)
        grace_period = datetime.now(pytz.utc) - vrf.updated_at
        if grace_period.seconds < 300:
            return Response({'message':'You have just request for verification code, please wait for 5 minutes before trying again'})


        vrf.code = randrange(100000,999999)
        response = vrf.send_code(request.user.country_code, request.user.phone, vrf.code)
        if response.status_code == "200":
            vrf.save()
            return Response({'message':'Verification code has been resend, please check your mobile phone for SMS'})
        else:
            return Response({'message':'Something wrong when sending verification code to your number, please check if the phone number is correct and exist'})



    def post(self, request):
        """
        Verify phone number
        ---
        request_serializer: member.serializers.MemberVerificationSerializer
        """
        vrf = self.get_object(request.user)

        serializedVerification = MemberVerificationSerializer(request.data)
        if serializedVerification.is_valid():
            if vrf.code == serializedVerification.initial_data['code']:
                request.user.verified = True
                request.user.save()
                vrf.verified = True
                vrf.save()
                return Response({'message':'Your account has been successfully verified!'})
        else:
            return Response(serializedVerification.errors, status=status.HTTP_400_BAD_REQUEST)


class MemberDetail(APIView):
    def get(self, request):
        """
        Get all details for this member
        ---
        serializer: member.serializers.MemberSerializer
        """
        serializedMember = MemberSerializer(request.user)
        return Response({'user':serializedMember.data})

    def put(self, request):
        """
        Modify details for currently logged in member, fields that is not included in the JSON will be left unchanged
        ---
        serializer: member.serializers.MemberSerializer
        """

        serializedMember = MemberSerializer(request.user ,data=request.data, partial=True)
        if serializedMember.is_valid():
            serializedMember.save()
            return Response({'user':serializedMember.data})
        return Response(serializedMember.errors, status=status.HTTP_400_BAD_REQUEST)


class MemberPhotoList(APIView):
    def post(self, request):
        """
        This API is used solely to upload member photos.
        ---
        serializer: member.serializers.MemberPhotoSerializer
        """
        serializedMember = MemberSerializer(request.user ,data=request.data, exclude=('first_name','last_name','username','email','phone','categories'))
        if serializedMember.is_valid():
            serializedMember.save()
            return Response({'user':serializedMember.data}, status=status.HTTP_200_CREATED)
        return Response(serializedMember.errors, status=status.HTTP_400_BAD_REQUEST)


class MemberCategoryList(APIView):
    def get(self, request):
        """
        This API is used to list out all the categories associated with this member
        ---
        serializer: member.serializers.MemberCategorySerializer
        """
        categories = MemberCategory.objects.filter(member=request.user)
        serializedMemberCategory = MemberCategorySerializer(categories, many=True)

        return Response({'categories':serializedMemberCategory.data})


class MemberCategoryDetail(APIView):
    def post(self, request, mc_id):
        """
        This API is used to register the user with the category, verified is false by default until verified by the admin.
        just need to post with the serializer and thats all.
        ---
        omit_serializer: true
        """
        try:
            MemberCategory.objects.create(category_id=mc_id, member=request.user)
        except ValueError:
            return Response({'error':'No such category'})
        except IntegrityError:
            return Response({'error':'Category already been associated with member'})
        
        return Response({'message':'Category has been added to the member'})

    def delete(self, request, mc_id):
        """
        This API is used to delete the category associated with the member.
        just need to post with the serializer and thats all.
        ---
        omit_serializer: true
        """
        try:
            mc = MemberCategory.objects.get(id=mc_id, member=request.user)
        except:
            raise Http404

        mc.delete()
        return Response({'message':'Category has been deleted from member'},status=status.HTTP_204_NO_CONTENT)