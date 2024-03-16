from django.urls import path
from . import views

urlpatterns = [
    path('login_with_otp/', views.login_with_otp, name='login_with_otp'),
    path('otp_login_verify/<str:email>/', views.otp_login_verify, name='otp_login_verify'),
    path('forgot_password/', views.forgot_password, name='forgot_password'),
    path('restaurant/<int:restaurant_id>/', views.restaurant_detail, name='restaurant_detail'),
    path('view_cart/', views.view_cart, name='view_cart'),
    path('add_to_cart/<int:item_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove_from_cart/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('clear_cart/', views.clear_cart, name='clear_cart'),
    path('place_order/', views.place_order, name='place_order'),
    path('add_review/<int:restaurant_id>/', views.add_review, name='add_review'),
    path('process_payment/<int:order_id>/', views.process_payment, name='process_payment'),
    path('payment_success/<int:payment_id>/', views.payment_success, name='payment_success'),
    # Define other URL patterns
]