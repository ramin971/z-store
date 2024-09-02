from typing import Any
from django.contrib import admin
from django.db.models import Avg,F
from django.utils import timezone
from . import models
import jdatetime

@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']
    list_select_related = ['parent']
    list_display = ['name','path']
    prepopulated_fields = {'slug':('name',)}

    def path(self,instance):
        parent=instance.parent
        path = [instance.name]
        if parent:
            while parent:
                path.append(parent.name)
                parent = parent.parent
        return ' > '.join(path[::-1])



class ProductImageInline(admin.TabularInline):
    model = models.ProductImage
    extra = 1

# use filter horizontal instead ----------------
# class TagInline(admin.TabularInline):
#     model = models.Product.tags.through
#     extra = 1
    
# use filter horizontal instead ----------------
class SizeInline(admin.TabularInline):
    model = models.Size
    extra = 1


@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    autocomplete_fields = ['category']
    filter_horizontal = ['tags']
    list_select_related = ['category','category__parent']
    list_display = ['id','name','rate','category','price','size','tag','update']
    prepopulated_fields = {'slug':('name',)}
    ordering = ['-updated']
    list_per_page = 10
    search_fields = ['name','category__istartswith']
    list_filter = ['category','updated']
    inlines = [ProductImageInline,SizeInline]

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(rate=Avg('rates__rate'))


    def size(self,instance):
        # return ','.join([str(i.value) for i in instance.sizes.all()])
        # return [size.value for size in instance.sizes.all()]
        # return (a,b) for a , b in list(instance.sizes.all().values_list('value',flat=True))
        return list(f'{v}->{s}' for v,s in instance.sizes.values_list('value','stock'))


    def tag(self,instance):
        # return ",".join([p.value for p in instance.sizes.all()])
        # return [tag.value for tag in instance.tags.all()]
        return list(instance.tags.all().values_list('value',flat=True))
    
    def rate(self,instance):
        return f'{instance.rate}'
    
    def update(self,instance):
        updated=instance.updated
        local_time = timezone.localtime(updated) # change local timezone in setting to convert time
        converted_date = jdatetime.datetime.fromgregorian(datetime=local_time) # don't convert time. the solution is above the line.
        return converted_date.strftime("%Y-%m-%d %H:%M:%S")
    
@admin.register(models.ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ['product','image']
    list_select_related = ['product']

@admin.register(models.Size)
class SizeAdmin(admin.ModelAdmin):
    list_display = ['product','value','stock']
    search_fields = ['value']

@admin.register(models.Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['value']
    search_fields = ['value']

@admin.register(models.Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['id','product']
    list_select_related = ['product','user']


@admin.register(models.OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['user','product','quantity','cart']

class OrderItemInline(admin.TabularInline):
    autocomplete_fields = ['product']
    model = models.OrderItem
    extra = 1
    readonly_fields = ['user']
    

@admin.register(models.Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['id','user','customer','payment','get_total_price','status','ordered_date']
    ordering = ['payment','status','-ordered_date']
    search_fields = ['customer','id']
    readonly_fields = ['id','user','customer','payment','get_total_price','coupon','ordered_date']
    list_filter = ['payment','status','ordered_date']
    radio_fields = {'status':admin.HORIZONTAL}
    list_editable = ['status']
    list_select_related = ['customer','coupon']
    inlines = [OrderItemInline]
    list_per_page = 10
    

@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['full_name','user','mobile','address','national_code','postal_code']
    readonly_fields = ['full_name','user','national_code','postal_code','mobile','address']

admin.site.register(models.Description)
admin.site.register(models.Rating)
admin.site.register(models.Reaction)
admin.site.register(models.Coupon)


# admin.site.register(models.Cart)
# admin.site.register(models.OrderItem)
# admin.site.register(models.ReceiverInfo)