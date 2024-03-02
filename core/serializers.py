from rest_framework import serializers
from . import models

class CategorySerializer(serializers.ModelSerializer):
    parent = serializers.StringRelatedField()
    class Meta:
        model = models.Category
        fields = ['id','name','slug','parent']
