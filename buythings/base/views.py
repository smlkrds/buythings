from django.shortcuts import render, get_object_or_404

from .models import Product, Category

def index(request):
	products = Product.objects.all()
	return render(request, 'base/index.html', {'products': products})

def categories(request):
	category_list = Category.objects.all()
	return render(request, 'base/categories.html', {'categories': category_list})

def product_list(request, pk):
	category = get_object_or_404(Category, pk=pk)
	products = Product.objects.filter(category=category)
	return render(request, 'base/product_list.html', {'category': category, 'products': products})

def details(request, pk):
	products = Product.objects.get(pk=pk)
	return render(request, 'base/details.html', {'product': products})