from django.shortcuts import render, get_object_or_404
from .models import Product

def product_list(request):
    """Список товаров с фильтрацией по категориям"""
    category = request.GET.get('category', '')
    
    products = Product.objects.filter(is_active=True)
    
    # Фильтруем только если категория выбрана и существует
    if category in dict(Product.CATEGORY_CHOICES):
        products = products.filter(category=category)
    
    return render(request, 'shop/product_list.html', {
        'products': products,
        'current_category': category
    })

def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id, is_active=True)
    return render(request, 'shop/product_detail.html', {'product': product})