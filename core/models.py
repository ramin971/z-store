from django.db import models
from django.core.validators import MaxValueValidator,MinValueValidator,RegexValidator
from django.conf import settings
from rest_framework.exceptions import NotAcceptable
from uuid import uuid4

# ---------------Category--------------------------------------------------------------------------------
class Category(models.Model):
    name = models.CharField(max_length=50,unique=True)
    slug = models.SlugField(unique=True)
    parent = models.ForeignKey('self',null=True,blank=True,on_delete=models.CASCADE,related_name='childs')

    class Meta:
        constraints =[
            models.UniqueConstraint(fields=['slug','parent'],name='unique_slug_category')
        ]

    def __str__(self) -> str:
        return f'{self.name}'
    # def __str__(self):
    #     fullpath = [self.slug]
    #     parent = self.parent
    #     while parent:
    #         fullpath.append(parent.name)
    #         parent = parent.parent
    #     return '/'.join(fullpath[::-1])


# ---------------Product(related)--------------------------------------------------------------------------------
class Tag(models.Model):
    value = models.CharField(max_length=30,unique=True)
    def __str__(self) -> str:
        return self.value

class Description(models.Model):
    video = models.FileField(upload_to='video')
    text = models.TextField()


class Size(models.Model):
    value = models.CharField(max_length=20,unique=True)
    def __str__(self) -> str:
        return self.value

# ---------------Product--------------------------------------------------------------------------------
class Product(models.Model):
    name = models.CharField(max_length=100,unique=True)
    slug = models.SlugField()
    category = models.ForeignKey(Category,on_delete=models.PROTECT,related_name='products')
    description = models.ForeignKey(Description,on_delete=models.SET_NULL,null=True,blank=True)
    sizes = models.ManyToManyField(Size,related_name='products')
    tags = models.ManyToManyField(Tag,blank=True,related_name='products')
    price = models.PositiveIntegerField()
    stock = models.PositiveSmallIntegerField(validators=[MinValueValidator(0)])
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    def __str__(self) -> str:
        return f'{self.name}'

class ProductImage(models.Model):
    image = models.ImageField(upload_to='image')
    product = models.ForeignKey(Product,on_delete=models.CASCADE,related_name='images')

    def __str__(self) -> str:
        return f'{self.product}'
    
class Rating(models.Model):
    rate = models.PositiveSmallIntegerField(validators=[MinValueValidator(1),MaxValueValidator(5)])
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE,related_name='rates')

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=('user','product'),name='unique_rate')
        ]
    
# ---------------Comment--------------------------------------------------------------------------------
class Comment(models.Model):
    text = models.TextField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='comments')
    product = models.ForeignKey(Product,on_delete=models.CASCADE,related_name='comments')
    # parent = models.ForeignKey('self',on_delete=models.CASCADE,null=True,blank=True,related_name='replis')


    def __str__(self) -> str:
        return f'{self.product}-{self.user}-{self.id}'
    
    # preventing the use of this comment(self) as its parent during update ---------
    # def save(self,*args,**kwargs):
    #     print('#######start...')
    #     if self == self.parent:
    #         raise NotAcceptable('Not Acceptable')
    #     return super().save(*args,**kwargs)
      

class Reaction(models.Model):
    REACTION_OPTIONS = (('L','Like'),('D','Dislike'))
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment,on_delete=models.CASCADE,related_name='reactions')
    reaction_type = models.CharField(max_length=1,choices=REACTION_OPTIONS)
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=('user','comment'),name='unique_reaction')
        ]
  


# ---------------Cart--------------------------------------------------------------------------------
class Coupon(models.Model):
    code = models.CharField(max_length=25,unique=True)
    amount = models.PositiveSmallIntegerField()

    def __str__(self):
        return self.code


class Customer(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,primary_key=True)
    full_name = models.CharField(max_length=50)
    national_code = models.CharField(null=True,blank=True,validators=[RegexValidator(regex='^\d{10}$',message='must be 10 \
        digit',code='invalid_national_code')],max_length=10)
    mobile = models.CharField(validators=[RegexValidator(regex='^[0][9][0-9]{9}$',message='phone number\
         invalid',code='invalid_phone')],max_length=11,unique=True)
    address = models.TextField()
    postal_code = models.CharField(null=True,blank=True,validators=[RegexValidator(regex='^\d{10}$',message='must be 10 \
        digit',code='invalid_postal_code')],max_length=10)


class Cart(models.Model):
    STATUS_CHOICES = (('u','Unpaid'),('q','Queue'),('p','Providing'),('s','Sent'))
    id = models.UUIDField(primary_key=True,default=uuid4,unique=True,editable=False)
    customer = models.ForeignKey(Customer,on_delete=models.CASCADE,related_name='carts')
    ordered_date = models.DateTimeField(null=True,editable=False)
    payment = models.BooleanField(default=False)
    customer = models.ForeignKey(Customer,on_delete=models.PROTECT,related_name='carts')
    status = models.CharField(max_length=1,choices=STATUS_CHOICES,default='u')
    coupon = models.ForeignKey(Coupon,on_delete=models.SET_NULL,null=True,blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['customer','coupon'],name='unique_coupon')
        ]
    def __str__(self):
        return f'{self.customer.full_name},{self.id}'

    def get_total_price(self):
        total = 0
        for order_item in self.order_items.all():
            total += order_item.get_total_product_price()
            if self.coupon:
                total = total - (self.coupon.amount * total // 100)
        return total

    def save(self,*args,**kwargs):
        if not self.payment:
            print('###payment is false')
            try:
                temp_basket = Basket.objects.get(customer=self.customer,payment=False)
            except Basket.DoesNotExist:
                print('######basket doesnot exist therefor create')
                return super(Basket,self).save(*args,**kwargs)
                # raise NotAcceptable('Temporary Basket is already available')
            except Basket.MultipleObjectsReturned:
                raise NotAcceptable('extra temprary basket')
            
            # temp_basket = Basket.objects.filter(user=self.user,payment=False)
            if self !=  temp_basket:
                print('pay=t , temp=e , self =! temp')
                raise NotAcceptable('Temporary Basket is already available')
            return super(Basket,self).save(*args,**kwargs)
        else:
            if self.ordered_date is None:
                print('***fill ordered_date...')
                self.ordered_date = datetime.datetime.now()
        return super(Basket,self).save(*args,**kwargs)

class OrderItem(models.Model):
    customer = models.ForeignKey(Customer,on_delete=models.CASCADE,related_name='order_items')
    product = models.ForeignKey(Product,on_delete=models.CASCADE,related_name='order_items')
    quantity = models.PositiveSmallIntegerField(validators=[MinValueValidator(1)])
    cart = models.ForeignKey(Cart,on_delete=models.CASCADE,related_name='order_items')

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['cart','product'],name='unique_product')
        ]

    def get_total_product_price(self):
        price = self.product.price
        return price * self.quantity