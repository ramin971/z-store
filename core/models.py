from django.db import models
from django.core.validators import MaxValueValidator,MinValueValidator


class Category(models.Model):
    name = models.CharField(max_length=50,unique=True)
    slug = models.SlugField(unique=True)
    parent = models.ForeignKey('self',null=True,blank=True,on_delete=models.CASCADE,related_name='childs')

    class Meta:
        constraints =[
            models.UniqueConstraint(fields=['slug','parent__slug'],name='unique_slug_category')
        ]

    def __str__(self) -> str:
        return f'{self.slug}'
    # def __str__(self):
    #     fullpath = [self.slug]
    #     parent = self.parent
    #     while parent:
    #         fullpath.append(parent.name)
    #         parent = parent.parent
    #     return '/'.join(fullpath[::-1])



class Tag(models.Model):
    value = models.CharField(max_length=30,unique=True)

class Description(models.Model):
    video = models.FileField(upload_to='video')
    text = models.TextField()



class Size(models.Model):
    value = models.CharField(max_length=20,unique=True)





class Product(models.Model):
    name = models.CharField(max_lengh=100,unique=True)
    slug = models.SlugField()
    category = models.ForeignKey(Category,one_delete=models.PROTECT,related_name='products')
    description = models.OneToOneField(Description,one_delete=models.SET_NULL,null=True,blank=True)
    sizes = models.ManyToManyField(Size,related_name='products')
    tags = models.ManyToManyField(Tag,related_name='products')
    pass

class ProductImage(models.Model):
    image = models.ImageField(upload_to='image')
    product = models.ForeignKey(Product,on_delete=models.CASCADE,related_name='images')

    def __str__(self) -> str:
        return f'{self.product}'
    

class Comment(models.Model):
    text = models.TextField()
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='comments')
    product = models.ForeignKey(Product,on_delete=models.CASCADE,related_name='comments')

    class Meta:
        ordering = ['-id']

    def __str__(self) -> str:
        return f'{self.product}'

class Reaction(models.Model):
    #like
    #dislike
    pass

class Rating(models.Model):
    rate = models.PositiveSmallIntegerField(validators=[MinValueValidator(1),MaxValueValidator(5)])
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE,related_name='rates')

#-------------------------------------

class Coupon(models.Model):
    pass

class ReceiverInfo(models.Model):
    #user
    pass

class Cart(models.Model):
    pass

class OrderItem(models.Model):
    pass