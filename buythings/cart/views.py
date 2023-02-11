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
    product = Product.objects.get(id=pk)
    cart_item, created = CartItem.objects.get_or_create(
        user=request.user, product=product
    )
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    return redirect('index')

def remove_from_cart(request, pk):
    cart_item = CartItem.objects.get(user=request.user, product_id=pk)
    cart_item.delete()
    return redirect('cart')