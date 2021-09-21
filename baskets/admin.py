from django.contrib import admin

# Register your models here.
from baskets.models import Basket



@admin.register(Basket)
class BasketAdmin(admin.ModelAdmin):

	fields = ('user', 'product', ('price', 'quantity'), 'category', 'created_timestamp', 'update_timestamp')
	readonly_fields = ('created_timestamp', 'update_timestamp')
	# ordering = ('name', 'price')
	# search_fields = ('name', 'description')