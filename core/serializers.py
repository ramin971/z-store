from rest_framework import serializers
from .models import Category,Tag,Description,Size,Product,ProductImage,Rating,\
                Comment,Reaction,Coupon,Cart,OrderItem,Customer
from django.conf import settings
from auth_app.models import User


class SimpleUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','username']



class SimpleCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id','name']


class CategorySerializer(serializers.ModelSerializer):
    # parent = serializers.StringRelatedField()
    class Meta:
        model = Category
        fields = ['id','name','slug','parent']

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id','value']

class DescriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Description
        fields = ['id','video','text']

class SizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Size
        fields = ['id','value']


# TEST
class ProductImageSerializer(serializers.ModelSerializer):
    # images = serializers.ListField(child=serializers.ImageField(),write_only=True)
    class Meta:
        model = ProductImage
        fields = ['image']

    def to_representation(self, instance):
        request = self.context.get('request')


        return request.build_absolute_uri(instance.image.url)


class SimpleProductSerializer(serializers.ModelSerializer):
    rate = serializers.SerializerMethodField(read_only=True)
    category = serializers.StringRelatedField()
    sizes = serializers.StringRelatedField(many=True,read_only=True)
    tags = serializers.StringRelatedField(many=True,read_only=True)
    images = ProductImageSerializer(read_only=True,many=True)

    class Meta:
        model = Product
        fields = ['id','name','category','images','price','stock','rate','tags','sizes','updated']
        read_only_fields = ['id','rate','updated']


    def get_rate(self,instance):
        return instance.avg_rate
    

class DetailProductSerializer(SimpleProductSerializer):

    class Meta(SimpleProductSerializer.Meta):
        fields = ['id','name','category','images','price','stock','rate','description','tags','sizes','updated']



class ProductSerialzier(serializers.ModelSerializer):
    images = serializers.ListField(child=serializers.ImageField(),write_only=True)
    class Meta:
        model = Product
        fields = ['id','name','category','images','price','stock','description','tags','sizes']
        read_only_fields = ['id','updated']
        extra_kwargs={'description':{'write_only':True},'tags':{'write_only':True},'sizes':{'write_only':True}}

    def save(self, **kwargs):
        validated_data = self.validated_data
        if self.instance:
            # PUT
            if 'images' in validated_data:
                print('delete old images.....')
                self.instance.images.all().delete()
        images_data = validated_data.pop('images')
        instance = super().save(**kwargs)
        for image in images_data:
            print('add image.....')
            ProductImage.objects.create(product=instance,image=image)

        return instance

    # TEST
    # def create(self, validated_data):
    #     images_data = validated_data.pop('images')
    #     # product = Product.objects.create(validated_data)
    #     product = super().create(validated_data)
    #     print('$$$$$$$$$product:',product)
    #     for image in images_data:
    #         print('add image')
    #         ProductImage.objects.create(product=product,image=image)

    #     return product



    # def get_rate(self,instance):
    #     print('***********seriallzier')
        
    #     if hasattr(instance,'avg_rate'):
    #         print('***********seriallzier2')

    #         return instance.avg_rate
    #     print('***********seriallzier3')

        
    #     return None
    




class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ['id','product','user','rate']
        read_only_fields=['id','user']

    def create(self, validated_data):
        user = self.context.get('user')
        validated_data['user'] = user
        return super().create(validated_data)
    


class ReactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reaction
        fields = ['id','user','comment','reaction_type']
        read_only_fields = ['id','user']
        # extra_kwargs={'comment':{'write_only':True}}
        
    def create(self, validated_data):
        user = self.context.get('user')
        validated_data['user'] = user
        return super().create(validated_data)

class SimpleCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id','user','text','product']
        read_only_fields = ['id','user']

    def create(self, validated_data):
        user = self.context.get('user')
        validated_data['user'] = user
        return super().create(validated_data)



class CommentSerializer(serializers.ModelSerializer):
    user = SimpleUserSerializer(read_only=True)
    likes = serializers.SerializerMethodField(read_only=True)
    dislikes = serializers.SerializerMethodField(read_only=True)
    class Meta(SimpleCommentSerializer.Meta):
        model = Comment
        fields = ['id','user','text','product','likes','dislikes']


    def get_likes(self,instance):
        return instance.likes
    def get_dislikes(self,instance):
        return instance.dislikes

# class CommentSerializer(serializers.ModelSerializer):
#     replis = serializers.SerializerMethodField(read_only=True)
#     # replis = SimpleCommentSerializer(many=True,read_only=True)
#     # reactions = ReactionSerializer(many=True,read_only=True)
   
#     class Meta:
#         model = Comment
#         fields = ['id','user','text','product','parent','replis']
#         read_only_fields= ['id','user']

#     def create(self, validated_data):
#         user = self.context.get('user')
#         validated_data['user'] = user
#         return super().create(validated_data)
    
#     def validate_parent(self,value):
#         parent = value
#         max_level = settings.MAX_NESTED_LEVEL_COMMENT
#         count_level = 0
#         while parent is not None:
#             if max_level <= count_level:
#                 raise serializers.ValidationError('max_nested_level does not support it')
#             count_level = count_level + 1
#             parent = parent.parent
#             # print(f'##############parent:{parent},,level:{count_level}')
#         return value
    

#     def get_replis(self,instance):
#         replis = instance.replis
#         serializer = CommentSerializer(replis,many=True)
#         return serializer.data


# cart-----------------------------------------------------------------

class CouponSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coupon
        fields = ['id','code','amount']


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['user','full_name','mobile','address','national_code','postal_code']
        read_only_fields = ['user']


    def create(self, validated_data):
        user = self.context.get('user')
        validated_data['user'] = user
        return super().create(validated_data)
