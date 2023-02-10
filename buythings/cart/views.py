from django.shortcuts import render, redirect
from base.models import CartItem, Product

def cart(request):
    cart_items = CartItem.objects.filter(user=request.user)
    products = [item.product for item in cart_items]
    invoice = 0
    for product in products:
        invoice += product.price
    return render(request, 'cart/cart.html', {'products': products, 'invoice': invoice})

def add_to_cart(request, pk):
    try:
        cart_item = CartItem.objects.get(user=request.user)
    except CartItem.DoesNotExist:
        cart_item = CartItem.objects.create(user=request.user)
    product = Product.objects.get(id=pk)
    cart_item.product = product
    cart_item.save()
    return redirect('index')