from rest_framework import viewsets,mixins
from rest_framework.exceptions import MethodNotAllowed
from .models import Category,Tag,Description,Size
from .serializers import CategorySerializer,TagSerializer\
                        ,DescriptionSerializer,SizeSerializer

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

# class DescriptionViewSet(viewsets.ModelViewSet):
    ##  Block list method ------------
    # def list(self, request, *args, **kwargs):
    #     raise MethodNotAllowed("GET")

# Block list method --------------
class DescriptionViewSet(mixins.CreateModelMixin,
                        mixins.RetrieveModelMixin, 
                        mixins.UpdateModelMixin,
                        mixins.DestroyModelMixin,
                        viewsets.GenericViewSet):
    queryset = Description.objects.all()
    serializer_class = DescriptionSerializer


class SizeViewSet(viewsets.ModelViewSet):
    
    queryset = Size.objects.all()
    serializer_class = SizeSerializer

    