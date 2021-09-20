from carts.models import Cart, CartItem
from django.contrib import admin

# Register your models here.

class CartItemAdmin(admin.ModelAdmin):
    list_display = ('product','cart','quantity','is_active',)
    list_filter = ('product','user','quantity',)
    
class CartAdmin(admin.ModelAdmin):
    list_display = ('cart_id','date_added')
    list_filter = ('date_added',)   
    
     

admin.site.register(Cart,CartAdmin)
admin.site.register(CartItem ,CartItemAdmin)
