from django.db import models
from django.contrib.auth.models import User

class Product(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=200)
    price = models.IntegerField(default=0)
    active = models.BooleanField(default=True)
    seller = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name

class Comment(models.Model):
    content = models.CharField(max_length=200)
    commented_product = models.ForeignKey(Product, on_delete=models.CASCADE)
    commentator = models.ForeignKey(User, on_delete=models.CASCADE)
    def __str__(self):
        return self.content