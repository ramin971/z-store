from rest_framework import viewsets,mixins,generics,status
from rest_framework.response import Response
from rest_framework.exceptions import ParseError
from .models import Category,Tag,Description,Size,Product\
                    ,ProductImage,Rating,Comment,Reaction
from .serializers import CategorySerializer,TagSerializer\
                        ,DescriptionSerializer,SizeSerializer,ProductSerialzier\
                        ,RatingSerializer,CommentSerializer,SimpleProductSerializer\
                        ,DetailProductSerializer,ProductImageSerializer,ReactionSerializer\
                        
from django.db.models import Avg,Count,Case,When,IntegerField
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
        
class ProductImageViewset(viewsets.ModelViewSet):
    queryset = ProductImage.objects.all()
    serializer_class = ProductImageSerializer

    def get_serializer_context(self):
        return {'request':self.request}
    


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
    queryset = Comment.objects.all().select_related('user')\
        .annotate(likes=Count(Case(When(reactions__reaction_type='L', then=1),output_field=IntegerField(),)),\
                    dislikes=Count(Case(When(reactions__reaction_type='D', then=1),output_field=IntegerField(),)))


    serializer_class = CommentSerializer

    # def get_queryset(self):
    #     print('pk****: ',self.kwargs)
    #     print('user',self.request.user)
    #     return Comment.objects.filter(product=self.kwargs['pk'],parent__isnull=True)
    def get_serializer_context(self):
        return {'user':self.request.user}
    


class ReactionViewSet(viewsets.ModelViewSet):
    queryset = Reaction.objects.select_related('comment__user','comment__product','user').all()
    serializer_class = ReactionSerializer
    # permission_classes = [IsAuthenticated]
    

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
  