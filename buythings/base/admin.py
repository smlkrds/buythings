from django.contrib import admin

from .models import Product, Comment, Category, CartItem

admin.site.register(Product)
admin.site.register(Comment)
admin.site.register(Category)
admin.site.register(CartItem)