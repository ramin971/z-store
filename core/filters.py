from django_filters.rest_framework import RangeFilter,CharFilter,FilterSet,OrderingFilter,BooleanFilter,NumericRangeFilter
from .models import Product


class ProductFilter(FilterSet):
    
    stock = BooleanFilter(field_name='stock',method='filter_stock')
    # size = CharFilter(label='size',method='custom_size')
    # price = RangeFilter(method='custom_price',label='price_range')

    class Meta:
        model = Product
        fields = {
            'category_id':['exact'],
            'price':['gt','lt'],
            'sizes__id':['exact'], 
            'tags__id':['exact'],

        }

    def filter_stock(self,queryset,name,value):
        # print('#value',value,'#name',name)
        if value:
            lookup = '__'.join([name, 'gt'])
            return queryset.filter(**{lookup: 0})
        return queryset
        # if value:
        #     return queryset.filter(stock__gt=0)
        # return queryset