from django.contrib import admin
from .models.users import CustomUser
# Register your models here.

class UserAdminConfig(admin.ModelAdmin):
    list_display = ('id', 'username', 'email', 'realname')