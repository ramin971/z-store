from rest_framework import serializers
from .models import Category,Tag,Description,Size,Product,ProductImage,Rating,\
                Comment,Reaction,Coupon,Cart,OrderItem,Customer
from django.conf import settings
from auth_app.models import User
from django.shortcuts import get_object_or_404
from django.urls import reverse
# from django.db.models import Sum

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
        fields = ['id','product','value','stock']


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
    stock = serializers.SerializerMethodField(read_only=True)
    rate = serializers.SerializerMethodField(read_only=True)
    category = serializers.StringRelatedField()
    sizes = SizeSerializer(many=True,read_only=True)
    # sizes = serializers.StringRelatedField(many=True,read_only=True)
    tags = serializers.StringRelatedField(many=True,read_only=True)
    images = ProductImageSerializer(read_only=True,many=True)

    class Meta:
        model = Product
        fields = ['id','name','category','images','price','stock','rate','tags','sizes','updated']
        read_only_fields = ['id','rate','updated']


    def get_rate(self,instance):
        return instance.avg_rate
    
    def get_stock(self,instance):
        return instance.stock

class DetailProductSerializer(SimpleProductSerializer):

    class Meta(SimpleProductSerializer.Meta):
        fields = ['id','name','category','images','price','rate','description','tags','sizes','updated']



class ProductSerialzier(serializers.ModelSerializer):
    images = serializers.ListField(child=serializers.ImageField(),write_only=True)
    class Meta:
        model = Product
        fields = ['id','name','category','images','price','description','tags','sizes']
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

    def validate(self, attrs):
        user = self.context.get('user')
        attrs['user'] = user
        return super().validate(attrs)

    # def create(self, validated_data):
    #     user = self.context.get('user')
    #     validated_data['user'] = user
    #     return super().create(validated_data)
    


class ReactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reaction
        fields = ['id','user','comment','reaction_type']
        read_only_fields = ['id','user']
        # extra_kwargs={'comment':{'write_only':True}}

    def validate(self, attrs):
        user = self.context.get('user')
        attrs['user'] = user
        return super().validate(attrs)
        
    # def create(self, validated_data):
    #     user = self.context.get('user')
    #     validated_data['user'] = user
    #     return super().create(validated_data)

class SimpleCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id','user','text','product']
        read_only_fields = ['id','user']

    def validate(self, attrs):
        user = self.context.get('user')
        attrs['user'] = user
        return super().validate(attrs)

    # def create(self, validated_data):
    #     user = self.context.get('user')
    #     validated_data['user'] = user
    #     return super().create(validated_data)



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

# unset user for cart new customer when dont interest to default user customer 
    # def validate(self, attrs):
    #     user = self.context.get('user')
    #     attrs['user'] = user
    #     return super().validate(attrs)
    
    # def create(self, validated_data):
    #     user = self.context.get('user')
    #     validated_data['user'] = user
    #     return super().create(validated_data)

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['id','user','product','size','quantity','cart','get_total_product_price']
        read_only_fields = ['id','user','cart','get_total_product_price']

    def validate(self, attrs):
        user = self.context.get('user')
        attrs['user'] = user
        cart,created = Cart.objects.get_or_create(user=user,payment=False)
        # print('$$$$$$$$$$$$$$created cart?',created)
        attrs['cart']=cart
        return super().validate(attrs)

    def create(self, validated_data):
        try:
            order_item = OrderItem.objects.get(cart=validated_data['cart'],product=validated_data['product'],size=validated_data['size'])
            order_item.quantity += validated_data['quantity']
            order_item.save()
            # print('1')
            # print('########not created')
            return order_item
        except OrderItem.DoesNotExist:
            # print('2')
            return super().create(validated_data)

class OrderItemDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['id','user','product','size','quantity','cart','get_total_product_price']
        read_only_fields = ['id','user','product','cart','get_total_product_price']

    def validate(self, attrs):
        user = self.context.get('user')
        attrs['user'] = user
        cart,created = Cart.objects.get_or_create(user=user,payment=False)
        # print('$$$$$$$$$$$$$$created cart?',created)
        attrs['cart']=cart
        return super().validate(attrs)


class CartProductSerializer(SimpleProductSerializer):
    # size = serializers.CharField
    class Meta(SimpleProductSerializer.Meta):
        fields = ['id','name','images','price']
   
class SimpleOrderItemSerializer(serializers.ModelSerializer):
    product = CartProductSerializer(read_only=True)
    class Meta:
        model = OrderItem
        fields = ['id','user','product','size','quantity','get_total_product_price']
        read_only_fields = ['id','user','get_total_product_price']
    
    

class CartSerializer(serializers.ModelSerializer):
    order_items= SimpleOrderItemSerializer(many=True,read_only=True)
    coupon_code = serializers.CharField(max_length=25,write_only=True,allow_blank=True)

    class Meta:
        model = Cart
        fields =['id','ordered_date','payment','user','customer','coupon_code','order_items','coupon','get_total_price','status']
        read_only_fields = ['id','ordered_date','user','payment','status','coupon','get_total_price']

    def validate(self, attrs):
        user = self.context.get('user')
        attrs['user'] = user
        if 'customer' not in attrs or attrs['customer'] is None:
            customer = user.customer
            attrs['customer'] = customer
        return super().validate(attrs)
    
    def update(self, instance, validated_data):
        if 'coupon_code' in validated_data:
            coupon_code = validated_data.pop('coupon_code')
            coupon = get_object_or_404(Coupon,code=coupon_code)
            instance.coupon = coupon
        return super().update(instance, validated_data)

class CartDetailSerializer(CartSerializer):
    # coupon_code = serializers.CharField(max_length=25,write_only=True,allow_blank=True)
    customer = CustomerSerializer(read_only=True)
    redirect_url = serializers.SerializerMethodField(read_only=True)
    class Meta(CartSerializer.Meta):
        fields = ['id','ordered_date','payment','user','customer','order_items','coupon','get_total_price','status','redirect_url']
        read_only_fields = ['id','ordered_date','user','payment','coupon','status','get_total_price']

    def get_redirect_url(self,instance):
        if instance.payment:
            return 'has been paid'
        redirect_url = reverse('go-to-gateway',kwargs={'price':instance.get_total_price(),'mobile':instance.customer.mobile,'id':instance.id})
        return redirect_url
        
        