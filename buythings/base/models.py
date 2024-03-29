from django.db import models
from django.contrib.auth.models import User, AbstractUser


class Category(models.Model):
    name = models.CharField(max_length=50, default="null")
    def __str__(self):
        return self.name
class Product(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=200)
    price = models.IntegerField(default=0)
    active = models.BooleanField(default=True)
    seller = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    contact_number = models.CharField(max_length=12, default='')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
    image = models.ImageField(upload_to='products/', null=True, blank=True)

    def __str__(self):
        return self.name

class Comment(models.Model):
    text = models.TextField(default='')
    commented_product = models.ForeignKey(Product, on_delete=models.CASCADE)
    commentator = models.ForeignKey(User, on_delete=models.CASCADE)
    def __str__(self):
        return self.text

class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.product.name
