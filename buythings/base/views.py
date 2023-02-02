from django.shortcuts import HttpResponse, render

from .models import Product, Category

def index(request):
	products = Product.objects.all()
	return render(request, 'base/index.html', {'products': products})

def categories(request):
	category_list = Category.objects.all()
	return render(request, 'base/categories.html', {'categories': category_list})
