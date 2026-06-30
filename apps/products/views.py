from django.shortcuts import render, get_object_or_404
from .models import Product, Category


def store(request):
    category_slug = request.GET.get('category')
    search = request.GET.get('q', '').strip()

    products = Product.objects.filter(is_active=True).select_related('category')
    categories = Category.objects.all()
    active_category = None

    if category_slug:
        active_category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=active_category)

    if search:
        products = products.filter(name__icontains=search)

    return render(request, 'store/shop.html', {
        'products': products,
        'categories': categories,
        'active_category': active_category,
        'search': search,
    })


def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk, is_active=True)
    related = Product.objects.filter(
        category=product.category, is_active=True
    ).exclude(pk=pk)[:4]
    return render(request, 'store/product_detail.html', {
        'product': product,
        'related': related,
    })
