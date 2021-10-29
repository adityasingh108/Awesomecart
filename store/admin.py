from django.contrib import admin
from . models import Product, Variation,ReviewRating,ProductGallery
from django.utils.html import format_html

import admin_thumbnails


@admin_thumbnails.thumbnail('image')
class ProductGalleryInline(admin.TabularInline):
    model = ProductGallery
    extra = 1

class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name','price','stock','category','modified_date','is_available')
    prepopulated_fields = {'slug':('product_name',)}
    inlines= [ProductGalleryInline]
    list_filter= ('stock','category','is_available',)
    
    
class VariationAdmin(admin.ModelAdmin):
    list_display    = ('product','variation_category','variation_value','is_active')
    list_editable   = ('is_active', )  
    list_filter     =  ('product','variation_category','variation_value',)
 
@admin_thumbnails.thumbnail('image')    
class ProductGalleryAdmin(admin.ModelAdmin):
    def thumbnail(self,object):
        return format_html('<img src= "{}" width="10%" style="border-radius:50%;">' .format(object.image.url))
    thumbnail.short_description = 'Product Image'
    list_display= ('product','thumbnail',)
    list_filter = ('product',)    

class AdminReviewRating(admin.ModelAdmin):
    list_display = ['product','rating','subject','user',]
admin.site.register(Product ,ProductAdmin)
admin.site.register(Variation ,VariationAdmin)
admin.site.register(ReviewRating,AdminReviewRating)
admin.site.register(ProductGallery,ProductGalleryAdmin)
