from rest_framework import serializers
from .models import Category,Tag,Description,Size

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
