from django.db import models
from ckeditor.fields import RichTextField
from django.contrib.auth.models import User

# Create your models here.
class Category(models.Model):
     name = models.CharField(max_length=200)
     logo = models.CharField(max_length=200)
     slug = models.CharField(max_length=500,unique=True)
     def __str__(self):
         return self.name

class SubCategory(models.Model):
    name = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    slug = models.CharField(max_length=500,unique=True)

    def __str__(self):
        return self.name

class Slider(models.Model):
    name = models.CharField(max_length=200)
    image = models.ImageField(upload_to='media')
    url = models.URLField(max_length=500, blank= True)
    description = models.TextField(blank= True)

    def __str__(self):
        return self.name

class Ad(models.Model):
    name = models.CharField(max_length=200)
    image = models.ImageField(upload_to='media')
    description = models.TextField(blank=True)
    rank = models.IntegerField()

    def __str__(self):
        return self.name

class Brand(models.Model):
    name = models.CharField(max_length=500)
    image = models.ImageField(upload_to='media')
    slug = models.CharField(max_length=500, unique=True)

    def __str__(self):
        return self.name

STATUS = (('Active', 'Active'), ('Inactive', 'Inactive'))
LABELS = (('new', 'new'), ('hot', 'hot'), ('sale', 'sale'), ('', 'default'))
class Product(models.Model):
    name = models.CharField(max_length=300)
    price = models.IntegerField()
    discounted_price = models.IntegerField()
    image = models.ImageField(upload_to='media')
    description = RichTextField()
    specification = RichTextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    subcategory = models.ForeignKey(SubCategory, on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    slug = models.CharField(max_length=500, unique=True)
    status = models.CharField(choices=STATUS, max_length=50)
    labels = models.CharField(choices=LABELS, max_length=50)
    def __str__(self):
        return self.name

class Review(models.Model):
    name = models.CharField(max_length=300)
    image = models.ImageField(upload_to='media')
    post = models.CharField(max_length=500)
    comment = models.TextField()
    star = models.IntegerField()
    def __str__(self):
        return self.name

class ProductImage(models.Model):
    name = models.CharField(max_length=300)
    image = models.ImageField(upload_to='media')
    product = models.ForeignKey(Product,on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class ProductReview(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField(max_length=300)
    date = models.DateTimeField(auto_now_add=True)
    star = models.IntegerField()
    comment = models.TextField()
    slug = models.CharField(max_length=500)

    def __str__(self):
        return self.name

class Cart(models.Model):
    username = models.CharField(max_length=300)
    slug = models.CharField(max_length=300)
    quantity = models.IntegerField()
    total = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)
    checkout = models.BooleanField(default=False)
    items = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return self.username

class Wishlist(models.Model):
    username = models.CharField(max_length=300)
    slug = models.CharField(max_length=300)
    date = models.DateTimeField(auto_now_add=True)
    items = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return self.username

class Newsletter(models.Model):
    email = models.EmailField(max_length=500)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email
#
# class Order(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     first_name = models.CharField(max_length=300, null=False)
#     last_name = models.CharField(max_length=300,null=False)
#     email = models.EmailField(max_length=300,null=False)
#     phone = models.CharField(max_length=300,null=False)
#     address = models.TextField(null=False)
#     country = models.CharField(max_length=300,null=False)
#     city = models.CharField(max_length=300,null=False)
#     state = models.CharField(max_length=300,null=False)
#     zip_code = models.CharField(max_length=300,null=False)
#     total_price = models.FloatField(null=False)
#     payment_mode = models.CharField(max_length=150, null=False)
#     payment_id = models.CharField(max_length=250, null=True)
#     orderstatuses = (
#         ('Pending', 'Pending'),
#         ('Out For Shipping', 'Out For Shipping'),
#         ('Completed', 'Completed'),
#     )
#     status = models.CharField(max_length=150, choices=orderstatuses,default='Pending')
#     message = models.TextField(null=True)
#     tracking_no = models.CharField(max_length=150, null=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#
#     def __str__(self):
#         return '{} - {}'.format(self.id, self.tracking_no)
#
# class OrderItem(models.Model):
#     order = models.ForeignKey(Order, on_delete=models.CASCADE)
#     product = models.ForeignKey(Product, on_delete=models.CASCADE)
#     price = models.FloatField(null=False)
#     quantity = models.FloatField(null=False)
#
#     def __str__(self):
#         return '{} - {}'.format(self.order.id, self.order.tracking_no)
