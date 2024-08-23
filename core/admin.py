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
# class SizeInline(admin.TabularInline):
#     model = models.Product.sizes.through
#     extra = 1


@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    autocomplete_fields = ['category']
    filter_horizontal = ['sizes','tags']
    list_select_related = ['category','category__parent']
    list_display = ['id','name','rate','category','price','stock','size','tag','update']
    prepopulated_fields = {'slug':('name',)}
    ordering = ['-updated']
    list_per_page = 10
    search_fields = ['name','category__istartswith']
    list_filter = ['category','updated']
    inlines = [ProductImageInline]

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(rate=Avg('rates__rate'))


    def size(self,instance):
        # return ','.join([str(i.value) for i in instance.sizes.all()])
        # return [size.value for size in instance.sizes.all()]
        return list(instance.sizes.all().values_list('value',flat=True))

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
    list_display = ['value']
    search_fields = ['value']

@admin.register(models.Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['value']
    search_fields = ['value']

@admin.register(models.Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['id','product']
    list_select_related = ['product','user']



admin.site.register(models.Description)
admin.site.register(models.Rating)
admin.site.register(models.Reaction)


# admin.site.register(models.Cart)
# admin.site.register(models.Coupon)
# admin.site.register(models.OrderItem)
# admin.site.register(models.ReceiverInfo)