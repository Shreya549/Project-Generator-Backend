from django.shortcuts import render

# Create your views here.
from django.conf import settings
import jwt, requests, uuid
from .models import (
    User,
    Faculty,
    Student,
    OTPStore,
    Contact,
)

from rest_framework.views import APIView
from rest_framework.generics import UpdateAPIView
from rest_framework.response import Response
from rest_framework import status, serializers
from rest_framework import viewsets, permissions, generics

from .serializers import (
    FacultyRegistrationSerializer,
    StudentRegistrationSerializer,
    UserLoginSerializer,
    ChangePasswordSerializer,
    ContactSerializer,
)

import uuid, os, base64, environ
from django.utils.crypto import get_random_string
from django.dispatch import receiver
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from datetime import datetime, timezone

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

class FacultyRegistration(APIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = FacultyRegistrationSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class StudentRegistration(APIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = StudentRegistrationSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class ContactUsView(viewsets.ModelViewSet):
    serializer_class = ContactSerializer

    def perform_create(self, serializer):
        serializer.save()

class UserLogin(APIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = UserLoginSerializer

    def post(self, request):

        serializer = self.serializer_class(data=request.data)

        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class ChangePasswordView(UpdateAPIView):
    """
    An endpoint for changing password.
    """
    serializer_class = ChangePasswordSerializer
    model = User
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Password updated successfully'
            }

            return Response(response)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




