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
                        
from django.db.models import Avg,Count,Case,When,IntegerField,Q


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


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
    
    # def get_queryset(self):
    #     query = Product.objects.prefetch_related('size','tag','images').select_related('category','description').annotate(avg_rate=Avg('rates__rate'))
    #     return query
        
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


    # serializer_class = CommentSerializer
    pagination_class = CustomPagination
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_serializer_class(self):
        if self.action in ['create','update','partial_update']:
            return SimpleCommentSerializer
        else:
            return CommentSerializer

    # def get_queryset(self):
    #     print('pk****: ',self.kwargs)
    #     print('user',self.request.user)
    #     return Comment.objects.filter(product=self.kwargs['pk'],parent__isnull=True)
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
  