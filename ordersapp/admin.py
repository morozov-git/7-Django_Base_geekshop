from django.contrib import admin

# Register your models here.
from django.contrib import admin

# Register your models here.
from ordersapp.models import Order



# @admin.register(Basket)
class OrderAdmin(admin.TabularInline):
	model = Order
	fields = ('Order',  'created_timestamp', 'update_timestamp')
	readonly_fields = ('created_timestamp', 'update_timestamp')
	extra = 0