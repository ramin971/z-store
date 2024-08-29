from rest_framework import viewsets,mixins,generics,status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly,IsAuthenticated
from rest_framework.exceptions import ParseError
from rest_framework.filters import SearchFilter,OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from .paginations import CustomPagination
from .filters import ProductFilter
from .models import Category,Tag,Description,Size,Product\
                    ,ProductImage,Rating,Comment,Reaction
from .serializers import CategorySerializer,TagSerializer\
                        ,DescriptionSerializer,SizeSerializer,ProductSerialzier\
                        ,RatingSerializer,CommentSerializer,SimpleCommentSerializer\
                            ,SimpleProductSerializer,DetailProductSerializer\
                                ,ProductImageSerializer,ReactionSerializer\
                                ,SimpleCategorySerializer
                        
from django.db.models import Avg,Count,Case,When,IntegerField,Q,Max
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class DescriptionViewSet(mixins.CreateModelMixin,
                        mixins.RetrieveModelMixin, 
                        mixins.UpdateModelMixin,
                        mixins.DestroyModelMixin,
                        viewsets.GenericViewSet):
    queryset = Description.objects.all()
    serializer_class = DescriptionSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class SizeViewSet(viewsets.ModelViewSet):
    queryset = Size.objects.all()
    serializer_class = SizeSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.prefetch_related('sizes','tags','images').select_related('category','description').annotate(avg_rate=Avg('rates__rate'))
    pagination_class = CustomPagination
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend,SearchFilter,OrderingFilter]
    filterset_class = ProductFilter
    search_fields = ['name']
    
    ordering_fields = ['created','price','avg_rate']

    def get_serializer_class(self):
        if self.action in ['create','update','partial_update']:
            return ProductSerialzier
        elif self.action == 'list':
            return SimpleProductSerializer
        else:
            return DetailProductSerializer
        
    
    @method_decorator(cache_page(3600*24))
    def list(self, request, *args, **kwargs):
        max_price=self.queryset.aggregate(max_price=Max('price'))['max_price']
        category = Category.objects.only('name','id')
        category_serializer = SimpleCategorySerializer(category,many=True)
        category_items = category_serializer.data
        size = Size.objects.all()
        size_serializer = SizeSerializer(size,many=True)
        size_items = size_serializer.data
        tag = Tag.objects.all()
        tag_serializer = TagSerializer(tag,many=True)
        tag_items = tag_serializer.data
        # items = self.queryset.values('category_id','category__name').distinct()
        filters = [
        {
            "name": "category__id",
            "type": "list",
            "faName": "دسته بندی",
            "items": category_items
        },
        {
            "name": "stock",
            "type": "radio",
            "faName": "فقط کالاهای موجود",
            "items": [
                { "name": "exist", "faName": "موجود", "value": "true" },
                { "name": "notExist", "faName": "ناموجود", "value": "false" },
                ],
        },
        {
            "name": "sizes__id",
            "type": "select",
            "faName": "سایز",
            "items": size_items
        },
        {
            "name": "tags__id",
            "type": "select",
            "faName": "تگ",
            "items": tag_items
        },
        {
            "name": "price",
            "type": "range",
            "faName": "محدوده قیمت",
            "items": [
                { "name": "price__gt", "faName": "حداقل", "value": 0 },
                { "name": "price__lt", "faName": "حداکثر", "value": max_price },
                ],
        },
        ]
        sorts=[
        {
            "name": "new",
            "faName": "جدید ترین",
            "value": "-created",
        },
        {
            "name": "cheap",
            "faName": "ارزان ترین",
            "value": "price",
        },
        {
            "name": "expensive",
            "faName": "گران ترین",
            "value": "-price",
        },
        {
            "name": "popular",
            "faName": "پربازدید ترین",
            "value": "-avg_rate",
        },
        ]
        response = super().list(request, *args, **kwargs)
        response.data['filters'] = filters
        response.data['sorts'] = sorts
        return response
        
class ProductImageViewset(viewsets.ModelViewSet):
    queryset = ProductImage.objects.all()
    serializer_class = ProductImageSerializer

    def get_serializer_context(self):
        return {'request':self.request}
    


class RatingProduct(mixins.CreateModelMixin,
                    viewsets.GenericViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    permission_classes = [IsAuthenticated]


    def get_serializer_context(self):
        return {'user':self.request.user}
    
class CommentViewSet(viewsets.ModelViewSet):
    # mixins.CreateModelMixin,
                    # mixins.RetrieveModelMixin, 
                    # mixins.UpdateModelMixin,
                    # mixins.DestroyModelMixin,
                    # viewsets.GenericViewSet):
    queryset = Comment.objects.select_related('user')\
        .annotate(likes=Count('reactions',filter=Q(reactions__reaction_type='L')),
                  dislikes=Count('reactions',filter=Q(reactions__reaction_type='D'))).order_by('-id')
    # SAME........
    # queryset = Comment.objects.all().select_related('user')\
    #     .annotate(likes=Count(Case(When(reactions__reaction_type='L', then=1),output_field=IntegerField(),)),\
    #                 dislikes=Count(Case(When(reactions__reaction_type='D', then=1),output_field=IntegerField(),)))


    pagination_class = CustomPagination
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_serializer_class(self):
        if self.action in ['create','update','partial_update']:
            return SimpleCommentSerializer
        else:
            return CommentSerializer

    def get_serializer_context(self):
        return {'user':self.request.user}
    


class ReactionViewSet(viewsets.ModelViewSet):
    queryset = Reaction.objects.select_related('comment__user','comment__product','user').all()
    serializer_class = ReactionSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    

    def create(self, request, *args, **kwargs):
        comment_id = request.data.get('comment')
        reaction_type = request.data.get('reaction_type')
        try:
            existing_reaction = Reaction.objects.get(comment_id=comment_id,user=request.user)
            if existing_reaction.reaction_type == reaction_type:
                # print('same........')
                raise ParseError(detail='you have already reacted with this type.')
            else:
                # print('change........')
                existing_reaction.reaction_type = reaction_type
                existing_reaction.save()
                serializer = ReactionSerializer(existing_reaction)
                return Response(serializer.data)
        except Reaction.DoesNotExist:
            # print('except........')
            return super().create(request, *args, **kwargs)
        
    def get_serializer_context(self):
        return {'user':self.request.user}
  