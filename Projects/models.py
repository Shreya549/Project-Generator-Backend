from django.db import models
from uuid import uuid4
import os, uuid

from django.core.serializers.json import DjangoJSONEncoder
from django.contrib.postgres.fields.jsonb import JSONField

from Accounts.models import (
    User,
    Student
)

def path_and_rename(instance, filename):
    upload_to = 'staticfiles/files'
    ext = filename.split('.')[-1]
    # get filename
    if instance.pk:
        filename = '{}.{}'.format(instance.pk, ext)
    else:
        # set filename as random string
        filename = '{}.{}'.format(uuid4().hex, ext)
    # return the whole path to the file
    return os.path.join(upload_to, filename)

# Create your models here.
class MyProject(models.Model):
    uuid = models.UUIDField(default = uuid.uuid4, primary_key = True)
    owner = models.ForeignKey(Student,  on_delete=models.CASCADE, related_name='student_project')
    title = models.CharField(max_length=100, null=True, blank=True)
    start_date = models.DateField(null = True, blank = True)
    end_date = models.DateField(null=True, blank=True)
    file = models.FileField(upload_to=path_and_rename, null = True)
    link = models.URLField(max_length=500, blank=True, null=True)
    author = models.TextField(null = True)
    # author = JSONField(encoder = DjangoJSONEncoder, null = True)

    faculty = models.CharField(max_length=200)
    course_code = models.CharField(max_length=10)
    course_name = models.CharField(max_length=100)
    duration = models.CharField(max_length=200)
    description = models.TextField()


