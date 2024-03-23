from django.contrib import admin
from .models import UserModel,FriendsModel
# Register your models here.

admin.site.register(UserModel)
admin.site.register(FriendsModel)
