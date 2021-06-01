from django.contrib import admin
from .models import User, Faculty, Student, Contact

# Register your models here.
admin.site.register(User)
admin.site.register(Faculty)
admin.site.register(Student)
admin.site.register(Contact)
