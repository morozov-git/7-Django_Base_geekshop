from django.contrib import admin
from .models import User
from baskets.models import Basket
from baskets.admin import BasketAdmin
from ordersapp.models import Order
# Register your models here.
# admin.site.register(User)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
	# model = Basket
	# inlines = (BasketAdmin, )
	model = Order
	inlines = (Order, )