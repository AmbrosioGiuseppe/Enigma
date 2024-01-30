from django.contrib import admin
from .models import *

# Register your models here.
class AllSettingAdmin(admin.ModelAdmin):
    model = AllSetting
    list_display = ['id', 'language',]

admin.site.register(AllSetting,AllSettingAdmin)