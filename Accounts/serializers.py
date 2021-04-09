from rest_framework import serializers
from .models import User, Faculty, Student, OTPStore
from django.contrib.auth import authenticate, password_validation

from rest_framework.response import Response

class FacultyRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True
    )
    token = serializers.CharField(max_length=255, read_only=True)

    class Meta:
        model = Faculty
        fields = ['email','name','token','password', 'uid']
        auto_created = True

    def create(self, validated_data):
        return Faculty.objects.create_faculty(**validated_data)

class StudentRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True
    )
    token = serializers.CharField(max_length=255, read_only=True)

    class Meta:
        model = Student
        fields = ['email','name','token','password', 'uid']
        auto_created = True

    def create(self, validated_data):
        return Student.objects.create_student(**validated_data)

class UserLoginSerializer(serializers.Serializer):
    uid = serializers.CharField(max_length=15)
    password = serializers.CharField(max_length=128, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)
    ac_type = serializers.CharField(max_length = 50, read_only=True)

    def validate(self, data):
        # The `validate` method is where we make sure that the current
        # instance of `LoginSerializer` has "valid". In the case of logging a
        # user in, this means validating that they've provided an email
        # and password and that this combination matches one of the users in
        # our database.
        uid = data.get('uid', None)
        password = data.get('password', None)

        # The `authenticate` method is provided by Django and handles checking
        # for a user that matches this email/password combination. Notice how
        # we pass `email` as the `username` value since in our User
        # model we set `USERNAME_FIELD` as `email`.
        user = authenticate(username=uid, password=password)

        # If no user was found matching this email/password combination then
        # `authenticate` will return `None`. Raise an exception in this case.
        if user is None:
            raise serializers.ValidationError(
                'A user with this Faculty Id and password is not found.'
            )
            
        userObj = None
        ac_type = ''
        try:
            userObj = Faculty.objects.get(uid=user.uid)
            ac_type = 'Faculty'

        except Faculty.DoesNotExist:
            userObj = None

        try:
            if userObj is None:
                userObj = Student.objects.get(uid=user.uid)
                ac_type = 'Student'

        except Student.DoesNotExist:
            raise serializers.ValidationError(
                'User with given Registration Number and Password does not exists'
            )

        # Django provides a flag on our `User` model called `is_active`. The
        # purpose of this flag is to tell us whether the user has been banned
        # or deactivated. This will almost never be the case, but
        # it is worth checking. Raise an exception in this case.
        if not user.is_active:
            raise serializers.ValidationError(
                'This user has been deactivated.'
            )

        # The `validate` method should return a dictionary of validated data.
        # This is the data that is passed to the `create` and `update` methods
        # that we will see later on.
        return {
            'uid': user.uid,
            'token': user.token,
            'ac_type' : ac_type
        }

class OTPStoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = OTPStore
        fields = '__all__'
        read_only_fields = '__all__'

class ChangePasswordSerializer(serializers.Serializer):
    model = User

    """
    Serializer for password change endpoint.
    """
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
