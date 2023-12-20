from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from .models import *

# Register your models here.
class UserAdmin(UserAdmin):
    model = User
    list_display = ['id', 'uid', 'username',]
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('telephoneNumber', 'levelUser', 'terms', 'privacy', 'newsletter')}),
    )

admin.site.register(User,UserAdmin)


class EmailVerificationTokenAdmin(admin.ModelAdmin):
    model = EmailVerificationToken
    list_display = ['id', 'user', 'token', 'created_at']

admin.site.register(EmailVerificationToken,EmailVerificationTokenAdmin)