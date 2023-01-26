from django.shortcuts import HttpResponse, render

from .models import Product
def index(request):
	products = Product.objects.all()
	return render(request, 'base/index.html', {'products': products})
