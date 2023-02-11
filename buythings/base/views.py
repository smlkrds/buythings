from django.contrib.auth import logout
from django.shortcuts import render, get_object_or_404, redirect

from .forms import CommentForm, ProductForm
from .models import Product, Category, Comment


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
    product = get_object_or_404(Product, id=pk)
    comments = Comment.objects.filter(commented_product=product)
    form = CommentForm()

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.commented_product = product
            comment.commentator = request.user
            comment.save()
            form = CommentForm()

    context = {
        'product': product,
        'comments': comments,
        'form': form,
    }

    return render(request, 'base/details.html', context)

def search(request):
    query = request.GET.get('q')
    if query:
        results = Product.objects.filter(name__icontains=query)
    else:
        results = []
    return render(request, 'base/search.html', {'products': results})

def logout_view(request):
    logout(request)
    return redirect('index')


def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.seller = request.user
            product.active = True
            product.save()
            return redirect('index')
    else:
        form = ProductForm()
    return render(request, 'base/sell_stuff.html', {'form': form})


def my_stuff(request):
    products = Product.objects.filter(seller=request.user)
    return render(request, 'base/my_stuff.html', {'products': products})