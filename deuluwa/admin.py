from django.contrib import admin
from deuluwa.models import User, Userinformation

# Register your models here.

@admin.register(User)
class InitUser(admin.ModelAdmin):
    list_display = ['id','password','admin']
    list_display_links = ['id']
