from django.shortcuts import render

# Create your views here.
from django.conf import settings
import jwt, requests, uuid
from .models import (
    User,
    Faculty,
    Student,
    OTPStore,
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

        try:
            serializer.is_valid()
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except:
            return Response({"error" : "Employee Id already exists"}, status = 403)  

class StudentRegistration(APIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = StudentRegistrationSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        try:
            serializer.is_valid()
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except:
            return Response({"error" : "Registration already exists"}, status = 403)  

class UserLogin(APIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = UserLoginSerializer

    def post(self, request):

        serializer = self.serializer_class(data=request.data)

        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)



