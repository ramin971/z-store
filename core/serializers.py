from rest_framework import serializers
from .models import Category,Tag,Description,Size,Product,ProductImage,Rating,Comment

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


class ProductSerialzier(serializers.ModelSerializer):
    image = serializers.SerializerMethodField(read_only=True)
    rate = serializers.SerializerMethodField(read_only=True)
    category = serializers.StringRelatedField()
    available_sizes = serializers.StringRelatedField(many=True,read_only=True,source='sizes')
    class Meta:
        model = Product
        fields = ['id','name','category','image','price','stock','rate','description','tags','available_sizes','sizes','updated']
        read_only_fields = ['id','rate','image','updated']
        extra_kwargs={'description':{'write_only':True},'tags':{'write_only':True},'sizes':{'write_only':True}}


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