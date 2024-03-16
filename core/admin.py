from django.contrib import admin
from .models import Address, UserProfile, Restaurant, MenuItem, Order, OrderItem, Review, Payment

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('email', 'phone')
    search_fields = ('email', 'phone')

@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ('user', 'address_line1', 'city', 'state', 'country')
    search_fields = ('user__email', 'address_line1', 'city', 'state', 'country')

@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'city', 'state', 'zipcode', 'contact_number', 'owner')
    search_fields = ('name', 'address', 'city', 'state', 'zipcode', 'contact_number', 'owner__email')

@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'price', 'restaurant')
    search_fields = ('name', 'description', 'restaurant__name')

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'restaurant', 'total_amount', 'order_date', 'status')
    search_fields = ('user__email', 'restaurant__name')
    list_filter = ('status',)

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'menu_item', 'quantity', 'item_price')
    search_fields = ('order__user__email', 'menu_item__name')

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'restaurant', 'rating', 'comment', 'review_date', 'is_featured')
    search_fields = ('user__email', 'restaurant__name', 'comment')
    list_filter = ('rating', 'is_featured')

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('order', 'payment_method', 'amount', 'payment_date', 'status')
    search_fields = ('order__user__email', 'payment_method', 'transaction_id')
    list_filter = ('status',)
