from django_filters.rest_framework import RangeFilter,CharFilter,FilterSet,OrderingFilter,BooleanFilter,NumericRangeFilter
from .models import Product


class ProductFilter(FilterSet):
    stock = BooleanFilter(field_name='stock',method='filter_stock')
    class Meta:
        model = Product
        fields = {
            'category__id':['exact'],
            'price':['gt','lt'],
            'sizes__id':['exact'], 
            'tags__id':['exact'],

        }

    def filter_stock(self,queryset,name,value):
        if value:
            lookup = '__'.join([name, 'gt'])
            return queryset.filter(**{lookup: 0})
        return queryset
        # if value:
        #     return queryset.filter(stock__gt=0)
        # return queryset