from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.conf import settings
from django.db.models import Q
from rest_framework.response import Response
from rest_framework import generics, status, views, permissions
from django.contrib.auth.hashers import make_password,check_password
from drf_yasg.utils import swagger_auto_schema

import jwt
from ..serializers.userSerializers import *
from ..utils import get_tokens
from ..models.users import CustomUser
import re

def UserValidation(email,username,password,password2,mode):
    string = "~!@#$%^&*()_+-*/<>,.[]\/"
    testSym = False
    if mode == 0:
        if CustomUser.objects.filter(email=email).exists():
            return 1001

        if CustomUser.objects.filter(username=username).exists():
            return 1002

    if password != password2:
        return 1003
    
    if len(password) < 8:
        return 1004

    for i in string:
        if i in password:
            testSym = True
            break
            
    #testSym = re.search(r"\W",password)
    testNum = re.search(r'\d',password)
    my_re = re.compile(r'[A-Za-z]',re.S)
    testAl = re.findall(my_re,password)

    if testSym and testNum and testAl:
        return 200
    else:
        return 1004

"""
POST: Register
"""
class UserRegisterView(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = UserRegisterSerializer

    @swagger_auto_schema(operation_summary="Register New User")
    def post(self, request):
        #try:
            email = request.data.get('email', '')
            username = request.data.get('username', '')
            password = request.data.get('password', '')
            password2 = request.data.get('password2', '')

            code = UserValidation(email,username,password,password2,0)

            if code == 1001:
                return Response({"message": "Email is taken.","code":code}, status=status.HTTP_400_BAD_REQUEST)
            elif code == 1002:
                return Response({"message": "Username is taken.","code":code}, status=status.HTTP_400_BAD_REQUEST)
            elif code == 1003:
                return Response({"message": "Password not match.","code":code}, status=status.HTTP_400_BAD_REQUEST)
            elif code == 1004:
                return Response({"message": "Password too simple.","code":code}, status=status.HTTP_400_BAD_REQUEST)

            serializer = self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            #newUser = CustomUser.objects.get(email=serializer.data['email'])
            #newToken = get_tokens(newUser)['access']

            #send_smtp(newUser, request, newToken, "Activate Account", "register_email.txt", True)
            data = serializer.data
            data['message'] = "Register Account Successfully"
            return Response(data, status=status.HTTP_201_CREATED)
        #except:
         #   return Response({"message": "Register Account Failed"}, status=status.HTTP_400_BAD_REQUEST)

"""
POST: Login
"""
class LoginView(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = LoginSerializer

    @swagger_auto_schema(operation_summary="User Login")
    def post(self, request):

        username = request.data['username']
        data = {}
        data['password'] = request.data['password']

        filter = Q(email=username) | Q(username=username)
        user = CustomUser.objects.filter(filter)
        if not user.exists():
            return Response({"message": "Invalid credentials, try again"},  status= status.HTTP_400_BAD_REQUEST)
        
        user = user[0]
        data['username'] = user.username

        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)


        data = serializer.data
        data['id'] = user.id
        data['realname'] = user.realname
        data['thumbnail'] = user.thumbnail or None
        data['gender'] = user.gender or None
        data['is_staff'] = user.is_staff
        data['dob'] = user.dob or None
        data['message'] = "Login Successfully"
        return Response(data,  status= status.HTTP_200_OK)

"""
POST: Logout
"""
class LogoutView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = LogoutSerializer

    @swagger_auto_schema(operation_summary="User Logout")
    def post(self, request):
        try:
            # apparently no need to delete access token on logout, it should time out quickly enough anyway.
            # https://medium.com/devgorilla/how-to-log-out-when-using-jwt-a8c7823e8a6
            serializer = self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)
            return Response({"message": "Logout Successfully"}, status=status.HTTP_204_NO_CONTENT)
        except:
            return Response({"message": "Logout Failed"}, status=status.HTTP_400_BAD_REQUEST)

"""
PUT: Reset Password (for authenticated user only)
"""
class ResetPasswordbyOldpasswordView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ResetPasswordByPasswordSerializer

    @swagger_auto_schema(operation_summary="Reset Password Through Old Password")
    def put(self, request):
        try:
            oldpassword = request.data['oldpassword']
            username = request.user.username
            user = CustomUser.objects.get(username=username)
            result = user.check_password(oldpassword)
            if result:
                code = UserValidation("","",request.data['newpassword'],request.data['newpassword2'],0)

                if code == 1001:
                    return Response({"message": "Email is taken.","code":code}, status=status.HTTP_400_BAD_REQUEST)
                elif code == 1002:
                    return Response({"message": "Username is taken.","code":code}, status=status.HTTP_400_BAD_REQUEST)
                elif code == 1003:
                    return Response({"message": "Password not match.","code":code}, status=status.HTTP_400_BAD_REQUEST)
                elif code == 1004:
                    return Response({"message": "Password too simple.","code":code}, status=status.HTTP_400_BAD_REQUEST)

                serializer = self.get_serializer(data=request.data, user=self.request.user)
                if serializer.is_valid(raise_exception=True):
                    serializer.updatePassword()
                    # When update success, should terminate the token, so it cannot be used again
                    return Response({"message": "Password Reset Successfully"}, status=status.HTTP_200_OK)
            else:
                return Response({"message": "Old Password Is Incorrect"}, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response({"message": "Password Reset Failed"}, status=status.HTTP_400_BAD_REQUEST)