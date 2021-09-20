from django.contrib import admin
from .models import User
from baskets.models import Basket
from baskets.admin import BasketAdmin

# Register your models here.
# admin.site.register(User)


# @admin.register(User)
# class UserAdmin(admin.TabularInline):
# 	model = Basket
# 	inlines = (BasketAdmin, )
