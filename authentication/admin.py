from django.contrib import admin
from django.contrib.auth.models import User

from authentication.models import UserProfile

# Register your models here.
admin.site.register(UserProfile)