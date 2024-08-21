from rest_framework import serializers
from .models import Category,Tag,Description,Size,Product,ProductImage,Rating,Comment
from django.conf import settings


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
    images = ProductImageSerializer(read_only=True,many=True)

    class Meta(SimpleProductSerializer.Meta):
        fields = ['id','name','category','images','price','stock','rate','description','tags','sizes','updated']



class ProductSerialzier(serializers.ModelSerializer):
    images = serializers.ListField(child=serializers.ImageField(),write_only=True)
    # category = serializers.StringRelatedField()
    size = serializers.StringRelatedField(many=True,read_only=True,source='sizes')
    tag = serializers.StringRelatedField(many=True,read_only=True,source='tags')
    class Meta:
        model = Product
        fields = ['id','name','category','images','price','stock','description','tag','size','tags','sizes']
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
    

    

class CommentSerializer(serializers.ModelSerializer):
    replis = serializers.SerializerMethodField(read_only=True)
   
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

