from django.contrib import admin
from django.contrib.admin.decorators import register
from django.contrib.auth.admin import UserAdmin 
from django.contrib.auth.models import User
from .models import User, Profile

admin.site.register(User, UserAdmin)
admin.site.register(Profile)