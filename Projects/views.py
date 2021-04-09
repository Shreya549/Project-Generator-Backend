from django.shortcuts import render
from rest_framework import viewsets, permissions, generics
from rest_framework.response import Response
from rest_framework import status
import json
from rest_framework.parsers import MultiPartParser, JSONParser
from rest_framework.decorators import parser_classes

from .models import MyProject
from .serializers import MyProjectSerializer

from Accounts.models import User, Student

# Create your views here.
@parser_classes((MultiPartParser, JSONParser))
class ProjectViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = MyProjectSerializer

    def get_queryset(self):
        profile = MyProject.objects.filter(owner = self.request.user)
        return profile

    def perform_create(self, serializer):
        author = json.dumps(self.request.data["author"], indent = 4)
        serializer.save(owner = self.request.user, author = author)

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        instance.delete()

class ViewProjectViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = MyProjectSerializer

    def get_queryset(self):
        regno = self.request.GET.get('regno')
        user = Student.objects.get(uid=regno)
        return MyProject.objects.filter(owner = user)
        



