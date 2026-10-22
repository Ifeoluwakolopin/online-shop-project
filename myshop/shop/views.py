from django.shortcuts import render, get_object_or_404
from .models import Category, Product
from cart.forms import CartAddProductForm


def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.active_translations().distinct().prefetch_related('translations')
    products = Product.objects.active_translations().filter(available=True).distinct().prefetch_related('translations')
    if category_slug:
        category = get_object_or_404(
            Category.objects.active_translations(slug=category_slug).distinct()
        )
        products = products.filter(category=category)
    categories = sorted(categories, key=lambda item: item.name)
    products = sorted(products, key=lambda item: item.name)
    return render(request,
        'shop/product/list.html',
        {'category':category,
        'categories':categories, 'products':products})
        
def product_detail(request, id, slug):
    product = get_object_or_404(
        Product.objects.active_translations(slug=slug).distinct(),
        id=id, available=True
    )
    cart_product_form = CartAddProductForm()
    return render(request,
        'shop/product/detail.html',
        {'product':product, 'cart_product_form':cart_product_form})