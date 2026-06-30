from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views.decorators.http import require_POST
from apps.products.models import Product
from .cart import Cart
from .models import Order, OrderItem


def cart_detail(request):
    cart = Cart(request)
    return render(request, 'store/cart.html', {'cart': cart})


@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, pk=product_id, is_active=True)
    quantity = int(request.POST.get('quantity', 1))
    if quantity > product.stock:
        messages.error(request, f'Only {product.stock} units available.')
    else:
        cart.add(product, quantity)
        messages.success(request, f'"{product.name}" added to cart.')
    return redirect(request.POST.get('next', 'store'))


@require_POST
def cart_remove(request, product_id):
    cart = Cart(request)
    cart.remove(product_id)
    return redirect('cart_detail')


@require_POST
def cart_update(request, product_id):
    cart = Cart(request)
    quantity = int(request.POST.get('quantity', 1))
    cart.update(product_id, quantity)
    return redirect('cart_detail')


def checkout(request):
    cart = Cart(request)
    if len(cart) == 0:
        return redirect('store')

    if request.method == 'POST':
        full_name = request.POST.get('full_name', '').strip()
        phone = request.POST.get('phone', '').strip()
        email = request.POST.get('email', '').strip()
        address = request.POST.get('address', '').strip()
        notes = request.POST.get('notes', '').strip()

        if not full_name or not phone or not address:
            messages.error(request, 'Please fill in all required fields.')
            return render(request, 'store/checkout.html', {'cart': cart})

        order = Order.objects.create(
            full_name=full_name,
            phone=phone,
            email=email,
            delivery_address=address,
            notes=notes,
        )

        for item in cart:
            product = item['product']
            qty = item['quantity']
            OrderItem.objects.create(
                order=order,
                product=product,
                product_name=product.name,
                price=item['price'],
                quantity=qty,
            )
            # Deduct stock
            product.stock -= qty
            product.save()

        order.calculate_total()
        cart.clear()
        return redirect('order_confirmation', pk=order.pk)

    return render(request, 'store/checkout.html', {'cart': cart})


def order_confirmation(request, pk):
    order = get_object_or_404(Order, pk=pk)
    return render(request, 'store/confirmation.html', {'order': order})
