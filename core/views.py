from rest_framework import viewsets,mixins,generics
from rest_framework.exceptions import MethodNotAllowed
from .models import Category,Tag,Description,Size,Product\
                    ,ProductImage,Rating,Comment
from .serializers import CategorySerializer,TagSerializer\
                        ,DescriptionSerializer,SizeSerializer,ProductSerialzier\
                        ,RatingSerializer,CommentSerializer,SimpleProductSerializer\
                        ,DetailProductSerializer,ProductImageSerializer
from django.db.models import Avg
from rest_framework.permissions import IsAuthenticated

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    # permission_classes = [IsAuthenticated]


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

    
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all().select_related('category','description').prefetch_related('sizes','tags','images').annotate(avg_rate=Avg('rates__rate'))
  
    def get_serializer_class(self):
        if self.action in ['create','update','partial_update']:
            return ProductSerialzier
        elif self.action == 'list':
            return SimpleProductSerializer
        else:
            return DetailProductSerializer
        


class RatingProduct(mixins.CreateModelMixin,
                    viewsets.GenericViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer

    def get_serializer_context(self):
        return {'user':self.request.user}
    
class CommentViewSet(viewsets.ModelViewSet):
    # mixins.CreateModelMixin,
                    # mixins.RetrieveModelMixin, 
                    # mixins.UpdateModelMixin,
                    # mixins.DestroyModelMixin,
                    # viewsets.GenericViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    # def get_queryset(self):
    #     print('pk****: ',self.kwargs)
    #     print('user',self.request.user)
    #     return Comment.objects.filter(product=self.kwargs['pk'],parent__isnull=True)
    def get_serializer_context(self):
        return {'user':self.request.user}
    
class ProductImageViewset(viewsets.ModelViewSet):
    queryset = ProductImage.objects.all()
    serializer_class = ProductImageSerializer

    def get_serializer_context(self):
        return {'request':self.request}