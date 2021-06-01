from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils.translation import ugettext_lazy as _

from datetime import timedelta
from datetime import datetime as dtime
from django.conf import settings
from uuid import uuid4

import jwt
import time
import uuid

# Create your models here.
class UserManager(BaseUserManager):
    def create_user(
            self, email, uid, name, password=None,
            commit=True):
        """
        Creates and saves a User with the given email, first name, last name
        and password.
        """
        if not email:
            raise ValueError(_('Users must have an email address'))
        if not name:
            raise ValueError(_('Users must have a name'))
        if not uid:
            raise ValueError(_('Users must have an Id'))

        user = self.model(
            email=self.normalize_email(email),
            name=name,
            uid=uid
        )

        user.set_password(password)
        if commit:
            user.save(using=self._db)
        return user

    def create_superuser(self, email, uid, name, password):
        """
        Creates and saves a superuser with the given email, first name,
        last name and password.
        """
        user = self.create_user(
            email,
            password=password,
            name=name,
            uid=uid,
            commit=False,
        )
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

    def get_by_natural_key(self, uid):
        return self.get(uid=uid)

class FacultyManager(BaseUserManager):

    def create_faculty(self, name, email, uid, password=None):
        if email is None:
            raise TypeError('Users must have an email address.')
        faculty = Faculty(name=name, uid=uid,
                          email=self.normalize_email(email),
                          )
        faculty.set_password(password)
        faculty.is_active = True
        faculty.save()
        return faculty

class StudentManager(BaseUserManager):

    def create_student(self, uid, name, email, password=None):
        if email is None:
            raise TypeError('Users must have an email address.')
        student = Student(name=name,uid=uid,
                        email=self.normalize_email(email))
        student.set_password(password)
        student.is_active = True
        student.save()
        return student

class User(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    uid = models.CharField(max_length = 10, unique = True, db_index = True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_(
            'Designates whether the user can log into this admin site.'
        ),
    )

    USERNAME_FIELD = 'uid'
    REQUIRED_FIELDS = ['name', 'email']

    objects = UserManager()

    @property
    def token(self):
        dt = dtime.now() + timedelta(days=2)
        token = jwt.encode({
            'id': self.id,
            'exp': int(time.mktime(dt.timetuple()))
        }, settings.SECRET_KEY, algorithm='HS512')
        return token.decode('utf-8')

    def natural_key(self):
        return (self.name)

    def __str__(self):
        return self.email

class Faculty(User, PermissionsMixin):

    USERNAME_FIELD = 'uid'
    REQUIRED_FIELDS = ['name', 'email']

    objects = FacultyManager()

    def __str__(self):
        return self.name

class Student(User, PermissionsMixin):

    USERNAME_FIELD = 'uid'
    REQUIRED_FIELDS = ['name', 'email']

    objects = StudentManager()

    def __str__(self):
        return self.name

class Contact(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, primary_key=True)
    name = models.CharField(max_length = 100)
    email = models.EmailField()
    subject = models.CharField(max_length = 200)
    message = models.TextField()

class OTPStore(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, primary_key = True)
    email = models.EmailField()
    otp = models.CharField(max_length = 8)
    timestamp = models.DateTimeField()