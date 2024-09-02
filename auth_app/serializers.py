from rest_framework_simplejwt.serializers import TokenRefreshSerializer as BaseTokenRefreshSerializer
from rest_framework_simplejwt.exceptions import InvalidToken
from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer\
                                , UserSerializer as BaseUserSerializer
from core.serializers import CustomerSerializer
from core.models import Customer
from django.db import transaction
from .models import User


# # require for custom-user ---------------
class UserCreateSerializer(BaseUserCreateSerializer):
    customer = CustomerSerializer()
    class Meta:
        model = User
        fields = ['username','password','customer']

    def validate(self, attrs):
        customer=attrs.pop('customer')
        super().validate(attrs)
        attrs['customer'] = customer
        return attrs
  
    @transaction.atomic()
    def create(self, validated_data):
        customer_data = validated_data.pop('customer')
        user = super().create(validated_data)
        customer = Customer.objects.create(user=user,**customer_data)
        return user
    


# require for custom-user ---------------
class UserSerializer(BaseUserSerializer):
    customer = CustomerSerializer(read_only=True)
    class Meta(BaseUserSerializer.Meta):
        fields = ['id','username','customer']


class TokenRefreshSerializer(BaseTokenRefreshSerializer):
    refresh = None
    def validate(self, attrs):
        attrs['refresh'] = self.context['request'].COOKIES.get('refresh_token')
        print('****',self.context['request'].COOKIES)
        if attrs['refresh']:
            return super().validate(attrs)
        raise InvalidToken