from django.shortcuts import render, get_object_or_404, redirect
from .models import Restaurant, MenuItem, Order, OrderItem, Review, Payment
import random
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.template.loader import render_to_string

def generate_otp():
    return str(random.randint(100000, 999999))

def login_with_otp(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        user, created = User.objects.get_or_create(email=email)
        if created or not user.has_usable_password():
            otp = generate_otp()
            user.set_password(otp)
            user.save()
            # Send OTP to email
            send_mail(
                'Your OTP for login',
                f'Your OTP is: {otp}',
                'your@example.com',  # Replace with your email
                [email],
                fail_silently=False,
            )
            return redirect('otp_login_verify', email=email)
        else:
            # User already has password, redirect to login with password
            return redirect('login')
    else:
        return render(request, 'login_with_otp.html')

def otp_login_verify(request, email):
    if request.method == 'POST':
        entered_otp = request.POST.get('otp')
        user = User.objects.get(email=email)
        if user.check_password(entered_otp):
            login(request, user)
            return redirect('home')  # Redirect to the home page after successful login
        else:
            return render(request, 'otp_login_verify.html', {'email': email, 'error': 'Invalid OTP'})
    else:
        return render(request, 'otp_login_verify.html', {'email': email, 'error': None})

def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            user = None
        if user:
            # Generate OTP for password reset
            otp = generate_otp()
            user.set_password(otp)
            user.save()
            # Send OTP to email
            send_mail(
                'Your OTP for password reset',
                f'Your OTP is: {otp}',
                'your@example.com',  # Replace with your email
                [email],
                fail_silently=False,
            )
            return redirect('password_reset_confirm', email=email)
        else:
            return redirect('forgot_password')  # Redirect to the forgot password page
    else:
        return render(request, 'forgot_password.html')


def restaurant_detail(request, restaurant_id):
    restaurant = get_object_or_404(Restaurant, pk=restaurant_id)
    menu_items = MenuItem.objects.filter(restaurant=restaurant)
    return render(request, 'restaurant_detail.html', {'restaurant': restaurant, 'menu_items': menu_items})

def view_cart(request):
    cart = request.session.get('cart', {})
    items = MenuItem.objects.filter(id__in=cart.keys())
    total_price = sum(cart[item_id] * item.price for item_id, item in zip(cart.keys(), items))
    return render(request, 'cart.html', {'items': items, 'cart': cart, 'total_price': total_price})

def add_to_cart(request, item_id):
    if 'cart' not in request.session:
        request.session['cart'] = {}
    cart = request.session['cart']
    cart[item_id] = cart.get(item_id, 0) + 1
    request.session['cart'] = cart
    return redirect('menu')

def remove_from_cart(request, item_id):
    if 'cart' in request.session:
        cart = request.session['cart']
        if item_id in cart:
            del cart[item_id]
            request.session['cart'] = cart
    return redirect('view_cart')

def clear_cart(request):
    if 'cart' in request.session:
        del request.session['cart']
    return redirect('view_cart')

def place_order(request):
    if request.method == 'POST':
        cart = request.session.get('cart', {})
        if not cart:
            return redirect('view_cart')  # Redirect to cart if cart is empty
        order = Order.objects.create(user=request.user, total_amount=0)
        total_amount = 0
        for item_id, quantity in cart.items():
            menu_item = get_object_or_404(MenuItem, pk=item_id)
            item_price = menu_item.price * quantity
            total_amount += item_price
            OrderItem.objects.create(
                order=order,
                menu_item=menu_item,
                quantity=quantity,
                item_price=item_price
            )
        order.total_amount = total_amount
        order.save()
        request.session['cart'] = {}
        return redirect('order_confirmation', order_id=order.id)
    else:
        return redirect('view_cart')

def add_review(request, restaurant_id):
    if request.method == 'POST':
        restaurant = get_object_or_404(Restaurant, pk=restaurant_id)
        user = request.user
        rating = request.POST.get('rating')
        comment = request.POST.get('comment')
        review = Review.objects.create(restaurant=restaurant, user=user, rating=rating, comment=comment)
        # You can add additional logic here, such as updating the restaurant's average rating
        return redirect('restaurant_detail', restaurant_id=restaurant_id)
    else:
        return render(request, 'add_review.html', {'restaurant_id': restaurant_id})

def process_payment(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    if request.method == 'POST':
        # Process payment logic goes here
        # For simplicity, we'll assume payment was successful
        payment_method = request.POST.get('payment_method')
        amount = order.total_amount
        transaction_id = '1234567890'  # Example transaction ID
        status = 'Success'  # Example payment status
        payment = Payment.objects.create(order=order, payment_method=payment_method, amount=amount, transaction_id=transaction_id, status=status)
        # Additional processing, such as updating order status
        return redirect('payment_success', payment_id=payment.id)
    else:
        return render(request, 'process_payment.html', {'order': order})

def payment_success(request, payment_id):
    payment = get_object_or_404(Payment, pk=payment_id)
    return render(request, 'payment_success.html', {'payment': payment})

