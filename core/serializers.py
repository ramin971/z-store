from rest_framework import serializers
from .models import Category,Tag,Description,Size,Product,ProductImage,Rating,Comment
from django.conf import settings


class CategorySerializer(serializers.ModelSerializer):
    parent = serializers.StringRelatedField()
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
        fields = ['id','product','image']


class ProductSerialzier(serializers.ModelSerializer):
    # TEST
    # images = ProductImageSerializer(many=True,write_only=True)
    images = serializers.ListField(child=serializers.ImageField(),write_only=True)
    # images = serializers.ImageField()


    image = serializers.SerializerMethodField(read_only=True)
    rate = serializers.SerializerMethodField(read_only=True)
    category = serializers.StringRelatedField()
    available_sizes = serializers.StringRelatedField(many=True,read_only=True,source='sizes')
    class Meta:
        model = Product
        fields = ['id','name','category','image','images','price','stock','rate','description','tags','available_sizes','sizes','updated']
        read_only_fields = ['id','rate','image','updated']
        extra_kwargs={'description':{'write_only':True},'tags':{'write_only':True},'sizes':{'write_only':True}}

    # TEST
    def create(self, validated_data):
        images_data = validated_data.pop('images')
        # product = Product.objects.create(validated_data)
        product = super().create(validated_data)
        print('$$$$$$$$$product:',product)
        for image in images_data:
            print('add image')
            ProductImage.objects.create(product=product,image=image)

        return product

    def get_image(self,obj):
        request = self.context.get('request')
        try:
            image = request.build_absolute_uri(obj.images.first().image.url)
            # images= [request.build_absolute_uri(i.image.url) for i in obj.images.all()]
        except:
            image = None
        return image

    def get_rate(self,instance):
        return instance.avg_rate
    




class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ['id','product','user','rate']
        read_only_fields=['id','user']

    def create(self, validated_data):
        user = self.context.get('user')
        validated_data['user'] = user
        return super().create(validated_data)
    

# class ProductImageSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = ProductImage
#         fields = ['id','product','image']
    

class CommentSerializer(serializers.ModelSerializer):
    replis = serializers.SerializerMethodField(read_only=True)
    # replis = serializers.ListField(child=,source='')
    # replis = ReplySerializer(many=True,read_only=True)


    class Meta:
        model = Comment
        fields = ['id','user','text','product','parent','replis']
        read_only_fields= ['id','user']

    def create(self, validated_data):
        user = self.context.get('user')
        validated_data['user'] = user
        return super().create(validated_data)
    
    def validate_parent(self,value):
        parent = value
        max_level = settings.MAX_NESTED_LEVEL_COMMENT
        count_level = 0
        while parent is not None:
            if max_level <= count_level:
                raise serializers.ValidationError('max_nested_level does not support it')
            count_level = count_level + 1
            parent = parent.parent
            print(f'##############parent:{parent},,level:{count_level}')
        return value
    

    def get_replis(self,instance):
        replis = instance.replis
        serializer = CommentSerializer(replis,many=True)
        return serializer.data

