from django.db import models
from django.core.validators import MaxValueValidator,MinValueValidator
from django.conf import settings

# ---------------Category--------------------------------------------------------------------------------
class Category(models.Model):
    name = models.CharField(max_length=50,unique=True)
    slug = models.SlugField(unique=True)
    parent = models.ForeignKey('self',null=True,blank=True,on_delete=models.CASCADE,related_name='childs')

    class Meta:
        constraints =[
            models.UniqueConstraint(fields=['slug','parent__slug'],name='unique_slug_category')
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

class Description(models.Model):
    video = models.FileField(upload_to='upload/video')
    text = models.TextField()


class Size(models.Model):
    value = models.CharField(max_length=20,unique=True)

# ---------------Product--------------------------------------------------------------------------------
class Product(models.Model):
    name = models.CharField(max_length=100,unique=True)
    slug = models.SlugField()
    category = models.ForeignKey(Category,on_delete=models.PROTECT,related_name='products')
    description = models.OneToOneField(Description,on_delete=models.SET_NULL,null=True,blank=True)
    sizes = models.ManyToManyField(Size,related_name='products')
    tags = models.ManyToManyField(Tag,related_name='products')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    def __str__(self) -> str:
        return f'{self.name}'

class ProductImage(models.Model):
    image = models.ImageField(upload_to='upload/image')
    product = models.ForeignKey(Product,on_delete=models.CASCADE,related_name='images')

    def __str__(self) -> str:
        return f'{self.product}'
    
class Rating(models.Model):
    rate = models.PositiveSmallIntegerField(validators=[MinValueValidator(1),MaxValueValidator(5)])
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE,related_name='rates')
    
# ---------------Comment--------------------------------------------------------------------------------
class Comment(models.Model):
    text = models.TextField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='comments')
    product = models.ForeignKey(Product,on_delete=models.CASCADE,related_name='comments')
    parent = models.ForeignKey('self',on_delete=models.CASCADE,null=True,blank=True,related_name='replis')

    class Meta:
        ordering = ['-id']

    def __str__(self) -> str:
        return f'{self.product}'

# class Reply(models.Model):
#     pass

class Reaction(models.Model):
    FEEDBACK_OPTIONS = (('L','Like'),('D','Dislike'))
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    comment = models.ForeignKey(Product,on_delete=models.CASCADE)
    feedback = models.CharField(max_length=1,choices=FEEDBACK_OPTIONS)
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=('user','comment'),name='unique_reaction')
        ]
  


# ---------------Cart--------------------------------------------------------------------------------
class Coupon(models.Model):
    pass

class ReceiverInfo(models.Model):
    #user
    pass

class Cart(models.Model):
    pass

class OrderItem(models.Model):
    pass