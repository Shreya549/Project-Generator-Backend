from rest_framework import serializers
from .models import MyProject

class MyProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyProject
        fields = '__all__'
        read_only_fields = ('owner',)