from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from .models import Order, OrderItem
from cart.models import CartItem

@login_required
def create_order(request):
    """Создание заказа из корзины с адресом доставки"""
    cart_items = CartItem.objects.filter(user=request.user)
    
    if not cart_items:
        messages.warning(request, "Ваша корзина пуста")
        return redirect('cart:cart_view')
    
    total = sum(item.total_price for item in cart_items)
    
    if request.method == 'POST':
        # Получаем данные адреса из формы
        address = request.POST.get('address', '')
        phone = request.POST.get('phone', '')
        comments = request.POST.get('comments', '')
        
        # Создаем заказ в транзакции
        with transaction.atomic():
            order = Order.objects.create(
                user=request.user,
                total_amount=total,
                status='pending',
                address=address,
                phone=phone,
                comments=comments
            )
            
            # Создаем элементы заказа
            for cart_item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    product=cart_item.product,
                    quantity=cart_item.quantity,
                    price=cart_item.product.price
                )
            
            # Очищаем корзину
            cart_items.delete()
        
        messages.success(request, f"Заказ #{order.id} успешно оформлен!")
        return redirect('orders:order_detail', order_id=order.id)
    
    # Если GET запрос - показываем форму ввода адреса
    return render(request, 'orders/order_create.html', {
        'cart_items': cart_items,
        'total': total
    })

@login_required
def order_detail(request, order_id):
    """Детальная страница заказа"""
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'orders/order_detail.html', {'order': order})

@login_required
def order_list(request):
    """Список заказов пользователя"""
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'orders/order_list.html', {'orders': orders})