from django.contrib import admin
from django.forms import models

from . models import Order,Payment,OrderProduct


class OrderProductInline(admin.TabularInline):
    model = OrderProduct
    readonly_fields = ('payment','user','product','quantity','product_price','ordered',)
    extra = 0

class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_number','full_name','email','phone','city','tax','status','is_ordered','order_total','created_at',]
    list_filter = ['status','is_ordered',]
    search_fields = ['order_number','first_name','last_name','phone','email',]
    list_per_page= 20
    inlines = [OrderProductInline]

# Register your models here.
admin.site.register(Payment)
admin.site.register(Order,OrderAdmin)
admin.site.register(OrderProduct)